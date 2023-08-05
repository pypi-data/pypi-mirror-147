from sqlite3 import Connection, connect

from ...functional import Lender, Producer

ConnectionFactory = Producer[Connection]
ConnectionFactory.__doc__ = """
Function returning a SQLite connection that must be closed by the caller
"""

ConnectionLender = Lender[Connection]
ConnectionLender.__doc__ = """
Function returning a connection that should NOT be closed by the caller
"""


def create_memory_db() -> Connection:
    """
    Returns a connection to an in-memory SQLite db.
    """
    return connect(":memory:")
