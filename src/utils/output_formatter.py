class OutputFormatter:

    def print_results(self, rows: list) -> None:
        if not rows:
            print("No results found.")
            return

        headers = rows[0].columns()
        col_widths = self._calculate_widths(rows, headers)

        self._print_row(headers, col_widths)
        self._print_separator(col_widths)

        for row in rows:
            values = [str(row.get(col) or "") for col in headers]
            self._print_row(values, col_widths)

    def _calculate_widths(self, rows: list, headers: list) -> list:
        widths = [len(h) for h in headers]
        for row in rows:
            for i, col in enumerate(headers):
                cell_len = len(str(row.get(col) or ""))
                widths[i] = max(widths[i], cell_len)
        return widths

    def _print_row(self, values: list, widths: list) -> None:
        cells = [str(v).ljust(w) for v, w in zip(values, widths)]
        print("| " + " | ".join(cells) + " |")

    def _print_separator(self, widths: list) -> None:
        parts = ["-" * w for w in widths]
        print("|-" + "-|-".join(parts) + "-|")