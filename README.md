# Micro-SQL Engine

## Project Description

Micro-SQL Engine is a simple **Command Line Interface (CLI)** tool that allows users to run simplified SQL-like queries on CSV files.

The program reads data from CSV files, builds an internal representation of the table in memory, and executes query operations such as selecting columns, filtering rows, and sorting results.

This project was developed as part of the course **Software Construction** at **Taras Shevchenko National University of Kyiv**.

---

## Key Features

* Execute simplified SQL queries on CSV files
* Select specific columns using `SELECT`
* Filter rows using `WHERE`
* Sort results using `ORDER BY`
* Process structured data directly in memory

---

## Tech Stack

* **Language:** Python 3
* **Version Control:** Git
* **Code Style:** PEP8
* **Linter:** flake8

---

## Project Structure

```
micro_sql_engine
│
├── src
│   ├── parser
│   ├── model
│   ├── engine
│   └── utils
│
├── tests
├── ARCHITECTURE.md
├── README.md
├── LICENSE
└── main.py
```

---

## Installation

Clone the repository:

```
git clone <repository-url>
```

Move to the project directory:

```
cd micro_sql_engine
```

Create a virtual environment:

```
python3 -m venv venv
```

Activate the environment:

Mac / Linux

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

---

## Code Quality

The project follows **PEP8 coding standards**.

To run the linter:

```
flake8 .
```

---

## Running the Program

Example command:

```
python main.py query.sql
```

Where `query.sql` contains a SQL-like query.

Example query:

```
SELECT name, salary
FROM users.csv
WHERE salary > 2000
ORDER BY salary DESC
```

---

## Author

Student: **Kachanyuk Dmytro**
Course: **Software Construction**
University: **Taras Shevchenko National University of Kyiv**