import pytest

from src.engine.executor import Executor
from src.exceptions import TypeConflictException, ValidationException
from src.model.expression_tree import Condition, QueryAST
from src.model.table import Row, Table


@pytest.fixture
def sample_table():
    headers = ["name", "department", "salary", "is_active"]
    rows = [
        Row({"name": "John", "department": "Engineering",
             "salary": "5000", "is_active": "true"}),
        Row({"name": "Jane", "department": "Marketing",
             "salary": "3000", "is_active": "true"}),
        Row({"name": "Alice", "department": "Engineering",
             "salary": "4500", "is_active": "false"}),
    ]
    return Table(name="users.csv", headers=headers, rows=rows)


@pytest.fixture
def executor():
    return Executor()


class TestExecutorPositive:

    def test_filters_by_department(self, executor, sample_table):
        query = QueryAST(
            columns=["name"],
            table_name="users.csv",
            conditions=[Condition("department", "=", "Engineering")],
        )
        result = executor.execute(sample_table, query)
        assert len(result) == 2

    def test_filters_by_multiple_conditions(
        self, executor, sample_table
    ):
        query = QueryAST(
            columns=["name"],
            table_name="users.csv",
            conditions=[
                Condition("department", "=", "Engineering"),
                Condition("is_active", "=", "true"),
            ],
        )
        result = executor.execute(sample_table, query)
        assert len(result) == 1
        assert result[0].get("name") == "John"

    def test_sorts_by_salary_desc(self, executor, sample_table):
        query = QueryAST(
            columns=["name", "salary"],
            table_name="users.csv",
            conditions=[],
            order_by="salary",
            order_desc=True,
        )
        result = executor.execute(sample_table, query)
        assert result[0].get("salary") == "5000"
        assert result[-1].get("salary") == "3000"

    def test_select_projects_columns(self, executor, sample_table):
        query = QueryAST(
            columns=["name"],
            table_name="users.csv",
            conditions=[],
        )
        result = executor.execute(sample_table, query)
        assert result[0].columns() == ["name"]

    def test_select_star_returns_all_columns(
        self, executor, sample_table
    ):
        query = QueryAST(
            columns=["*"],
            table_name="users.csv",
            conditions=[],
        )
        result = executor.execute(sample_table, query)
        assert result[0].columns() == sample_table.headers

    def test_no_results_returns_empty_list(
        self, executor, sample_table
    ):
        query = QueryAST(
            columns=["name"],
            table_name="users.csv",
            conditions=[Condition("department", "=", "HR")],
        )
        result = executor.execute(sample_table, query)
        assert result == []


class TestExecutorNegative:

    def test_unknown_select_column_raises_validation(
        self, executor, sample_table
    ):
        query = QueryAST(
            columns=["nonexistent"],
            table_name="users.csv",
            conditions=[],
        )
        with pytest.raises(ValidationException):
            executor.execute(sample_table, query)

    def test_unknown_where_column_raises_validation(
        self, executor, sample_table
    ):
        query = QueryAST(
            columns=["name"],
            table_name="users.csv",
            conditions=[Condition("ghost_col", "=", "value")],
        )
        with pytest.raises(ValidationException):
            executor.execute(sample_table, query)

    def test_type_conflict_raises_exception(
        self, executor, sample_table
    ):
        query = QueryAST(
            columns=["name"],
            table_name="users.csv",
            conditions=[Condition("salary", ">", "high")],
        )
        with pytest.raises(TypeConflictException):
            executor.execute(sample_table, query)