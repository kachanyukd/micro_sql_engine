# Architecture — Micro-SQL Engine

## Project Overview

Micro-SQL Engine is a command-line utility that executes simplified
SQL-like queries against CSV files.

The program accepts:
- a data file (CSV)
- a query file (SQL)

And performs:
- column selection (SELECT)
- row filtering (WHERE)
- result sorting (ORDER BY)

---

## Changes from Original Architecture (Lab 1)

The original architecture described in Lab 1 was updated during
implementation. Below are the changes and their reasons.

### 1. `Query` class split into `QueryAST` and `Condition`

**Original:** a single `Query` class containing all query data.

**New:** two separate classes in `expression_tree.py`:
- `QueryAST` — holds the full query structure
- `Condition` — represents a single WHERE condition

**Reason:** a single class mixed query structure with filtering logic.
Splitting them makes each class focused on one responsibility and
allows multiple conditions (AND) to be stored as a list.

### 2. `CSVLoader` moved to `src/utils/` instead of standalone module

**Original:** `CSVLoader` described as an independent top-level module.

**New:** `CsvLoader` lives in `src/utils/csv_loader.py`.

**Reason:** the loader is a utility — it reads a file and returns a
model. It does not belong in `parser/` or `engine/`. Placing it in
`utils/` better reflects its role.

### 3. `Table` and `Row` combined in `src/model/table.py`

**Original:** only `Table` was described; `Row` was not a separate
class.

**New:** both `Table` and `Row` are defined in `src/model/table.py`.

**Reason:** during implementation it became clear that returning raw
dictionaries from the loader made the executor harder to read. A
dedicated `Row` class with a `.get(column)` method makes the code
cleaner and more explicit.

### 4. `ResultFormatter` renamed to `OutputFormatter`

**Original:** `ResultFormatter` as a top-level component.

**New:** `OutputFormatter` in `src/utils/output_formatter.py`.

**Reason:** naming consistency — all utility classes follow the
`*Formatter`, `*Loader` pattern and live in `utils/`.

### 5. Entry point is `cli.py`, not `main.py`

**Original:** entry point not explicitly named.

**New:** `cli.py` in the project root handles CLI argument parsing
and orchestrates all modules.

**Reason:** the name `cli.py` better communicates the file's purpose
as a command-line interface entry point.

---

---

## Data Structures

### List
Used for storing table rows, query results, and column names.

### Dictionary (Hash Map)
Used internally by `Row` to store column-value pairs.

Example:
```python
{"id": "101", "name": "John Doe", "salary": "5000"}
```

### Expression Tree (Condition List)
WHERE conditions are stored as a flat list of `Condition` objects
joined by implicit AND logic.

Example for `WHERE department = 'Engineering' AND is_active = true`:

conditions = [
Condition(column="department", operator="=", value="Engineering"),
Condition(column="is_active",  operator="=", value="true"),
]

The executor evaluates all conditions with `all()` — equivalent to
AND logic.

---

## Module Structure

## Data Flow

cli.py receives path to .sql file via sys.argv
QueryParser reads .sql → builds QueryAST
CsvLoader reads .csv from query.table_name → builds Table
Executor applies WHERE, ORDER BY, SELECT → returns list[Row]
OutputFormatter prints results to stdout

---

## Separation of Concerns

| Module             | Responsibility                          |
|--------------------|-----------------------------------------|
| `cli.py`           | Entry point, argument handling only     |
| `QueryParser`      | Parsing SQL text into a model           |
| `CsvLoader`        | Reading CSV into memory                 |
| `Executor`         | Query logic: filter, sort, project      |
| `OutputFormatter`  | Printing results to stdout              |
| `QueryAST`         | Data structure for query representation |
| `Table` / `Row`    | Data structure for CSV representation   |

No module crosses into another's responsibility.
A class that reads a file does not execute queries.
A class that executes queries does not print results.

---

## Coding Standards

- Language: Python 3.12
- Linter: flake8 (0 errors, 0 warnings)
- Style: PEP 8, max line length 79 characters
- Naming: snake_case for variables and functions,
  PascalCase for classes