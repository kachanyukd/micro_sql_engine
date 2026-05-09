import re

from src.exceptions import ParserException
from src.model.expression_tree import Condition, QueryAST


class QueryParser:
    """Parses a simplified SQL query file into a QueryAST."""

    _OPERATORS = [">=", "<=", "!=", "=", ">", "<"]

    def parse(self, file_path: str) -> QueryAST:
        with open(file_path, encoding="utf-8") as sql_file:
            lines = sql_file.readlines()

        raw = " ".join(line.strip() for line in lines)
        query = " ".join(raw.split())

        self._validate_keywords(query, lines)

        columns = self._parse_columns(query)
        table_name = self._parse_table_name(query)
        conditions = self._parse_conditions(query, lines)
        order_by, order_desc = self._parse_order_by(query)

        return QueryAST(
            columns=columns,
            table_name=table_name,
            conditions=conditions,
            order_by=order_by,
            order_desc=order_desc,
        )

    def _validate_keywords(self, query: str, lines: list) -> None:
        upper = query.upper()

        if "SELECT" not in upper:
            raise ParserException(
                "Missing keyword SELECT in query", line=1
            )

        if "FROM" not in upper:
            select_line = self._find_line(lines, "SELECT")
            raise ParserException(
                "Missing keyword FROM in query",
                line=select_line,
            )

        select_pos = upper.index("SELECT")
        from_pos = upper.index("FROM")
        if select_pos > from_pos:
            raise ParserException(
                "SELECT must appear before FROM", line=1
            )

    def _find_line(self, lines: list, keyword: str) -> int:
        for i, line in enumerate(lines, start=1):
            if keyword.upper() in line.upper():
                return i
        return None

    def _parse_columns(self, query: str) -> list:
        match = re.search(r"SELECT (.+?) FROM", query, re.IGNORECASE)
        if not match:
            return []
        raw = match.group(1).strip()
        if raw == "*":
            return ["*"]
        return [col.strip() for col in raw.split(",")]

    def _parse_table_name(self, query: str) -> str:
        match = re.search(r"FROM (\S+)", query, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def _parse_conditions(self, query: str, lines: list) -> list:
        match = re.search(
            r"WHERE (.+?)(?:ORDER BY|$)", query, re.IGNORECASE
        )
        if not match:
            return []

        raw = match.group(1).strip()
        parts = re.split(r"\bAND\b", raw, flags=re.IGNORECASE)
        conditions = []

        for part in parts:
            condition = self._parse_single_condition(
                part.strip(), lines
            )
            if condition:
                conditions.append(condition)

        return conditions

    def _parse_single_condition(self, part: str, lines: list):
        for operator in self._OPERATORS:
            if operator in part:
                left, right = part.split(operator, 1)
                column = left.strip()
                value = right.strip().strip("'\"")

                if not column:
                    where_line = self._find_line(lines, "WHERE")
                    raise ParserException(
                        "Empty column name in WHERE condition",
                        line=where_line,
                    )

                return Condition(
                    column=column,
                    operator=operator,
                    value=value,
                )

        where_line = self._find_line(lines, "WHERE")
        raise ParserException(
            f"Cannot parse condition: '{part}'",
            line=where_line,
        )

    def _parse_order_by(self, query: str):
        match = re.search(
            r"ORDER BY (\S+)(?:\s+(ASC|DESC))?",
            query,
            re.IGNORECASE,
        )
        if not match:
            return None, False
        column = match.group(1).strip()
        direction = match.group(2) or "ASC"
        return column, direction.upper() == "DESC"