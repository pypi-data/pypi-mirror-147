"""This module provides the RP To-Do model-controller."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from todo_cli_typer import DB_DELETE_ERROR, DB_READ_ERROR, DB_UPDATE_ERROR, ID_ERROR, SUCCESS
from todo_cli_typer import CurrentTodo, Priority, Status, logger
# from todo_cli_typer.database_json import DatabaseHandler
from todo_cli_typer.database import DatabaseHandler, Todo, TodoItem



class Todoer:
    """called by the cli command to *do the param processing* before interacting with the db with DatabaseHandler"""

    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, description: list[str], priority: Priority = Priority.MEDIUM, status: Status = Status.TODO, project: str = '', tags: list[str] = [], due_date: datetime | None = None) -> CurrentTodo:
        """Add a new to-do to the database."""
        description_text = " ".join(description)
        tags_s = json.dumps(tags)
        insert = self._db_handler.add_todo(description_text, priority.value, status.value, project, tags_s, due_date)
        return CurrentTodo(insert.todo_list[0], insert.error)

    def get_todo(self, todo_id) -> CurrentTodo:
        """Return a to-do from the database, and return a status code,
        with the get_todo method from the DatabaseHandler"""
        read = self._db_handler.get_todo(todo_id)
        if read.todo_list:
            return CurrentTodo(read.todo_list[0], read.error)
        else:
            return CurrentTodo(None, read.error)


    def get_todo_all(self) -> list[TodoItem]:
        """Return the current to-do list."""
        read = self._db_handler.read_todos()
        return read.todo_list

    def modify(self, todo_id: int, description: list[str] | str, priority: Priority = Priority.MEDIUM, status: Status = Status.TODO, project: str = '', tags: list[str] = [], due_date: datetime | None = None) -> CurrentTodo:
        """Modify a to-do in the database, and return a status code"""
        description_text = " ".join(description) if isinstance(description, list) else description
        tags_s = json.dumps(tags)
        modify = self._db_handler.modify_todo(todo_id, description_text, priority.value, status.value, project, tags_s, due_date)
        if modify.todo_list:
            return CurrentTodo(modify.todo_list[0], modify.error)
        else:
            return CurrentTodo(None, DB_UPDATE_ERROR)
        

    def remove(self, todo_id: int) -> CurrentTodo:
        """Remove a to-do from the database, and return a status code"""
        remove = self._db_handler.remove_todo(todo_id)
        logger.info(f"remove: {remove}")
        if remove.error:
            return CurrentTodo(None, DB_DELETE_ERROR)
        else:
            return CurrentTodo(None, SUCCESS)

    def remove_all(self) -> int:
        """Remove all to-dos from the database, and return a status code"""
        remove_all = self._db_handler.remove_all_todos()
        return remove_all.error
        
