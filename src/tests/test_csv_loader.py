import pytest
from unittest.mock import mock_open, patch

from src.exceptions import FileSystemException
from src.utils.csv_loader import CsvLoader


@pytest.fixture
def loader():
    return CsvLoader()


class TestCsvLoaderPositive:

    def test_loads_headers(self, loader):
        csv_data = "name,salary\nJohn,5000\n"
        with patch("builtins.open", mock_open(read_data=csv_data)):
            table = loader.load("users.csv")
        assert table.headers == ["name", "salary"]

    def test_loads_correct_row_count(self, loader):
        csv_data = "name,salary\nJohn,5000\nJane,3000\n"
        with patch("builtins.open", mock_open(read_data=csv_data)):
            table = loader.load("users.csv")
        assert len(table.rows) == 2

    def test_row_values_accessible(self, loader):
        csv_data = "name,salary\nJohn,5000\n"
        with patch("builtins.open", mock_open(read_data=csv_data)):
            table = loader.load("users.csv")
        assert table.rows[0].get("name") == "John"


class TestCsvLoaderNegative:

    def test_missing_file_raises_filesystem_exception(self, loader):
        with pytest.raises(FileSystemException):
            loader.load("nonexistent.csv")

    def test_empty_file_raises_filesystem_exception(self, loader):
        with patch("builtins.open", mock_open(read_data="")):
            with pytest.raises(FileSystemException):
                loader.load("empty.csv")