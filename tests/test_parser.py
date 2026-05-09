import pytest
from unittest.mock import mock_open, patch

from src.exceptions import ParserException
from src.parser.query_parser import QueryParser


@pytest.fixture
def parser():
    return QueryParser()


def mock_sql(content):
    return patch("builtins.open", mock_open(read_data=content))


class TestQueryParserPositive:

    def test_parses_select_columns(self, parser):
        sql = "SELECT name, salary FROM data/users.csv"
        with mock_sql(sql):
            ast = parser.parse("query.sql")
        assert ast.columns == ["name", "salary"]

    def test_parses_table_name(self, parser):
        sql = "SELECT name FROM data/users.csv"
        with mock_sql(sql):
            ast = parser.parse("query.sql")
        assert ast.table_name == "data/users.csv"

    def test_parses_where_condition(self, parser):
        sql = (
            "SELECT name FROM data/users.csv "
            "WHERE department = 'Engineering'"
        )
        with mock_sql(sql):
            ast = parser.parse("query.sql")
        assert len(ast.conditions) == 1
        assert ast.conditions[0].column == "department"
        assert ast.conditions[0].operator == "="
        assert ast.conditions[0].value == "Engineering"

    def test_parses_multiple_conditions(self, parser):
        sql = (
            "SELECT name FROM data/users.csv "
            "WHERE department = 'Engineering' AND is_active = true"
        )
        with mock_sql(sql):
            ast = parser.parse("query.sql")
        assert len(ast.conditions) == 2

    def test_parses_order_by_desc(self, parser):
        sql = (
            "SELECT name FROM data/users.csv "
            "ORDER BY salary DESC"
        )
        with mock_sql(sql):
            ast = parser.parse("query.sql")
        assert ast.order_by == "salary"
        assert ast.order_desc is True

    def test_parses_star_select(self, parser):
        sql = "SELECT * FROM data/users.csv"
        with mock_sql(sql):
            ast = parser.parse("query.sql")
        assert ast.columns == ["*"]

    def test_no_where_returns_empty_conditions(self, parser):
        sql = "SELECT name FROM data/users.csv"
        with mock_sql(sql):
            ast = parser.parse("query.sql")
        assert ast.conditions == []


class TestQueryParserNegative:

    def test_missing_select_raises_parser_exception(self, parser):
        sql = "name FROM data/users.csv"
        with mock_sql(sql):
            with pytest.raises(ParserException):
                parser.parse("query.sql")

    def test_missing_from_raises_parser_exception(self, parser):
        sql = "SELECT name WHERE salary > 1000"
        with mock_sql(sql):
            with pytest.raises(ParserException):
                parser.parse("query.sql")

    def test_invalid_condition_raises_parser_exception(self, parser):
        sql = (
            "SELECT name FROM data/users.csv "
            "WHERE department"
        )
        with mock_sql(sql):
            with pytest.raises(ParserException):
                parser.parse("query.sql")