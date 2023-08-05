"""Top-level package for todo-cli-typer."""

__app_name__ = 'todo'
__version__ = '0.5.1'

from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Any
# Place this in your library's uppermost `__init__.py`
# Nothing else!

import logging
# https://stackoverflow.com/questions/7016056/python-logging-not-outputting-anything
logging.basicConfig(level=logging.NOTSET)

# logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)

# func is in the LogRecord doc, but results in logging error.
# formatter = logging.Formatter('%(levelname)s:%(name)s:%(pathname)s:%(func)s:%(message)s')
# formatter = logging.Formatter('%(levelname)s:%(name)s:%(pathname)s:%(message)s')
formatter = logging.Formatter('%(levelname)s:%(name)s:%(pathname)s:%(funcName)s:%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_CONNECTION_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    DB_DELETE_ERROR,
    DB_INSERT_ERROR,
    DB_UPDATE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(11)

ERRORS = {
    DIR_ERROR: 'config directory error',
    FILE_ERROR: 'config file error',
    DB_CONNECTION_ERROR: 'database connection error',
    DB_READ_ERROR: 'database read error',
    DB_WRITE_ERROR: 'database write error',
    ID_ERROR: 'to-do id error',
    DB_DELETE_ERROR: 'database delete error',
    DB_INSERT_ERROR: 'database insert error',
    DB_UPDATE_ERROR: 'database update error',
}
class Priority(str, Enum):
    """Priority levels for to-dos."""

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class Status(str, Enum):
    """Status of a to-do."""
    TODO = 'todo'
    DONE = 'done'
    DELETED = 'deleted'
    CANCELLED = 'cancelled'
    WIP = 'wip'

@dataclass
class TodoItem:
    """Create a to-do item."""
    id: int
    description: str
    priority: Priority
    status: Status
    project: str
    tags: str
    due_date: datetime | None
    # image: str

@dataclass
class DBResponse:
    todo_list: list[TodoItem]
    error: int

@dataclass
class SessionResponse:
    session: Any
    error: int

@dataclass
class CurrentTodo:
    todo: TodoItem | None
    error: int
