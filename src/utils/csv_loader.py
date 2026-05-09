import csv

from src.exceptions import FileSystemException
from src.model.table import Row, Table


class CsvLoader:
    """Reads a CSV file and builds a Table object in memory."""

    def load(self, file_path: str) -> Table:
        try:
            with open(
                file_path, newline="", encoding="utf-8"
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                headers = list(reader.fieldnames or [])

                if not headers:
                    raise FileSystemException(
                        f"CSV file '{file_path}' is empty or "
                        "has no headers"
                    )

                rows = [Row(dict(record)) for record in reader]

        except FileNotFoundError:
            raise FileSystemException(
                f"File not found: '{file_path}'"
            )
        except PermissionError:
            raise FileSystemException(
                f"Permission denied when reading: '{file_path}'"
            )

        table_name = file_path.split("/")[-1]
        return Table(name=table_name, headers=headers, rows=rows)