import re

from src.model.expression_tree import Condition, QueryAST


class QueryParser:
    """Parses a simplified SQL query file into a QueryAST."""

    _OPERATORS = [">=", "<=", "!=", "=", ">", "<"]

    def parse(self, file_path: str) -> QueryAST:
        with open(file_path, encoding="utf-8") as sql_file:
            raw = sql_file.read()

        query = " ".join(raw.split())

        columns = self._parse_columns(query)
        table_name = self._parse_table_name(query)
        conditions = self._parse_conditions(query)
        order_by, order_desc = self._parse_order_by(query)

        return QueryAST(
            columns=columns,
            table_name=table_name,
            conditions=conditions,
            order_by=order_by,
            order_desc=order_desc,
        )

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

    def _parse_conditions(self, query: str) -> list:
        match = re.search(
            r"WHERE (.+?)(?:ORDER BY|$)", query, re.IGNORECASE
        )
        if not match:
            return []

        raw = match.group(1).strip()
        parts = re.split(r"\bAND\b", raw, flags=re.IGNORECASE)
        conditions = []

        for part in parts:
            condition = self._parse_single_condition(part.strip())
            if condition:
                conditions.append(condition)

        return conditions

    def _parse_single_condition(self, part: str):
        for operator in self._OPERATORS:
            if operator in part:
                left, right = part.split(operator, 1)
                column = left.strip()
                value = right.strip().strip("'\"")
                return Condition(
                    column=column,
                    operator=operator,
                    value=value,
                )
        return None

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