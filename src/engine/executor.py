from src.exceptions import TypeConflictException, ValidationException
from src.model.expression_tree import Condition, QueryAST
from src.model.table import Row, Table


class Executor:
    """Executes a QueryAST against a Table and returns result rows."""

    def execute(self, table: Table, query: QueryAST) -> list:
        self._validate_columns(table, query)
        rows = self._apply_where(table.rows, query.conditions)
        rows = self._apply_order_by(
            rows, query.order_by, query.order_desc
        )
        rows = self._apply_select(rows, query.columns, table.headers)
        return rows

    def _validate_columns(
        self, table: Table, query: QueryAST
    ) -> None:
        if query.columns != ["*"]:
            for col in query.columns:
                if col not in table.headers:
                    raise ValidationException(
                        f"Column '{col}' not found in table. "
                        f"Available: {table.headers}"
                    )

        for condition in query.conditions:
            if condition.column not in table.headers:
                raise ValidationException(
                    f"Column '{condition.column}' used in WHERE "
                    f"not found in table. "
                    f"Available: {table.headers}"
                )

    def _apply_where(self, rows: list, conditions: list) -> list:
        result = []
        for row in rows:
            if all(self._matches(row, cond) for cond in conditions):
                result.append(row)
        return result

    def _matches(self, row: Row, condition: Condition) -> bool:
        raw_value = row.get(condition.column)
        if raw_value is None:
            return False

        cell = raw_value.strip().lower()
        target = condition.value.strip().lower()

        numeric_operators = [">", "<", ">=", "<="]
        cell_is_numeric = self._is_numeric(cell)
        target_is_numeric = self._is_numeric(target)

        if condition.operator in numeric_operators:
            if not cell_is_numeric or not target_is_numeric:
                raise TypeConflictException(
                    f"Cannot use '{condition.operator}' to compare "
                    f"'{raw_value}' and '{condition.value}': "
                    "both must be numeric"
                )

        if cell_is_numeric and target_is_numeric:
            return self._compare_numeric(
                float(cell), condition.operator, float(target)
            )

        return self._compare_string(cell, condition.operator, target)

    def _compare_numeric(
        self, left: float, operator: str, right: float
    ) -> bool:
        operations = {
            "=": left == right,
            "!=": left != right,
            ">": left > right,
            "<": left < right,
            ">=": left >= right,
            "<=": left <= right,
        }
        return operations.get(operator, False)

    def _compare_string(
        self, left: str, operator: str, right: str
    ) -> bool:
        if operator == "=":
            return left == right
        if operator == "!=":
            return left != right
        return False

    def _apply_order_by(
        self, rows: list, column: str, descending: bool
    ) -> list:
        if not column:
            return rows

        def sort_key(row: Row):
            value = row.get(column) or ""
            if self._is_numeric(value):
                return float(value)
            return value.lower()

        return sorted(rows, key=sort_key, reverse=descending)

    def _apply_select(
        self, rows: list, columns: list, all_headers: list
    ) -> list:
        target_columns = (
            all_headers if columns == ["*"] else columns
        )
        result = []
        for row in rows:
            projected = {
                col: row.get(col) for col in target_columns
            }
            result.append(Row(projected))
        return result

    @staticmethod
    def _is_numeric(value: str) -> bool:
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False