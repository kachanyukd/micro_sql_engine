class MicroSqlException(Exception):
    """Base exception for all Micro-SQL Engine errors."""

    def __init__(self, message: str, line: int = None):
        self.line = line
        prefix = f" at line {line}" if line else ""
        super().__init__(f"{message}{prefix}")


class FileSystemException(MicroSqlException):
    """Raised when a file cannot be found or read."""
    pass


class ParserException(MicroSqlException):
    """Raised when a SQL query has syntax errors."""
    pass


class ValidationException(MicroSqlException):
    """Raised when query logic is invalid against the table."""
    pass


class TypeConflictException(ValidationException):
    """Raised when incompatible types are compared in WHERE."""
    pass