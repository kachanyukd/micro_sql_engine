class Condition:

    def __init__(self, column: str, operator: str, value: str):
        self.column = column
        self.operator = operator
        self.value = value


class QueryAST:

    def __init__(
        self,
        columns: list,
        table_name: str,
        conditions: list,
        order_by: str = None,
        order_desc: bool = False,
    ):
        self.columns = columns
        self.table_name = table_name
        self.conditions = conditions
        self.order_by = order_by
        self.order_desc = order_desc