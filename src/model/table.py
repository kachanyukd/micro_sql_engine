class Row:

    def __init__(self, data: dict):
        self._data = data

    def get(self, column: str):
        return self._data.get(column)

    def columns(self):
        return list(self._data.keys())

    def to_dict(self):
        return dict(self._data)


class Table:

    def __init__(self, name: str, headers: list, rows: list):
        self._name = name
        self._headers = headers
        self._rows = rows

    @property
    def name(self):
        return self._name

    @property
    def headers(self):
        return self._headers

    @property
    def rows(self) -> list:
        return self._rows
