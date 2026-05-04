import sys

from src.engine.executor import Executor
from src.parser.query_parser import QueryParser
from src.utils.csv_loader import CsvLoader
from src.utils.output_formatter import OutputFormatter


def main():
    if len(sys.argv) != 2:
        print("Usage: python cli.py <path_to_query.sql>")
        sys.exit(1)

    sql_file_path = sys.argv[1]

    query_parser = QueryParser()
    query = query_parser.parse(sql_file_path)

    csv_loader = CsvLoader()
    table = csv_loader.load(query.table_name)

    executor = Executor()
    result_rows = executor.execute(table, query)

    formatter = OutputFormatter()
    formatter.print_results(result_rows)


if __name__ == "__main__":
    main()