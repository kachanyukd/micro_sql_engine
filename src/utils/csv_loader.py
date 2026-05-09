import csv

from src.model.table import Row, Table


class CsvLoader:
    """Reads a CSV file and builds a Table object in memory."""

    def load(self, file_path: str) -> Table:
        table_name = file_path.split("/")[-1]

        with open(file_path, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            headers = list(reader.fieldnames or [])
            rows = [Row(dict(record)) for record in reader]

        return Table(name=table_name, headers=headers, rows=rows)
