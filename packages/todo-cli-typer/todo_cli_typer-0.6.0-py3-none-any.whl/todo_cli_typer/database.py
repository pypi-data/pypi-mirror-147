from todo_cli_typer import logger
from todo_cli_typer import DB_CONNECTION_ERROR, DB_READ_ERROR, DB_WRITE_ERROR, SUCCESS, DB_DELETE_ERROR, DB_INSERT_ERROR, DB_UPDATE_ERROR
from todo_cli_typer import SessionResponse, DBResponse, TodoItem, Priority, Status
import configparser
from pathlib import Path
from datetime import datetime

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (Column, Integer, String, Enum, DateTime)


Base = declarative_base()
class Todo(Base):
    """Create the to-do table."""

    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    description = Column(String)
    priority = Column(Enum(Priority))
    status = Column(Enum(Status))
    project = Column(String)
    tags = Column(String)
    due_date = Column(DateTime, nullable=True)
    
    # nullable=True image
    # image = Column(String, nullable=True)

# create a database session to db_path
def create_session(db_path: Path) -> SessionResponse:
    """Create a database session to db_path."""
    try:
        engine = create_engine(f"sqlite:///{db_path}")
        Session = sessionmaker(bind=engine)
        session = Session()
    except OSError:
        return SessionResponse(None, DB_CONNECTION_ERROR)
    return SessionResponse(session, SUCCESS)

# sqlalchemy create a function to create a table in the database
# with columns for the to-do list
# id, description, priority, done, project, tags, and due date
def create_table(session, db_path: Path):
    """Create the to-do table in the database."""
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)

# insert a new to-do into the database
def insert_todo(session, description: str, priority: Priority, status: Status, project: str, tags: str, due_date: datetime | None) -> int:
    """Insert a new to-do into the database."""
    todo = Todo(description=description, priority = priority, status=status, project=project, tags=tags, due_date=due_date)
    session.add(todo)
    session.commit()
    # returns the id of the new to-do
    return todo.id # type: ignore

# remove a to-do from the database
def remove_todo(session, id: int) ->int:
    """Remove a to-do from the database."""
    try:
        todo = session.query(Todo).filter(Todo.id == id).first()
        session.delete(todo)
        session.commit()
        return SUCCESS
    except:
        return DB_DELETE_ERROR

# update a to-do in the database
def update_todo(session, id: int, description: str, priority: Priority, status: Status, project: str, tags: str, due_date: datetime | None):
    """Update a to-do in the database."""
    todo = session.query(Todo).filter(Todo.id == id).first()
    todo.description = description
    todo.status = status
    todo.project = project
    todo.tags = tags
    todo.due_date = due_date
    session.commit()

# get all to-dos from the database
def get_todo_list(session):
    """Get all to-dos and the id column from the database."""
    todo_list = session.query(Todo).all()
    return todo_list

# get a to-do from the database
def get_todo(session, id: int):
    """Get a to-do from the database."""
    todo = session.query(Todo).filter(Todo.id == id).first()
    return todo


DEFAULT_DB_FILE_PATH = Path.home() / '.todo-cli-typer.db'


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the to-do database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(session, db_path: Path) -> int:
    """Create the todo table in the to-do database."""
    try:
        db_path.touch(exist_ok=True)
        create_table(session, db_path)
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR




class DatabaseHandler:

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._session = create_session(db_path).session

    def add_todo(self, description: str, priority: Priority, status: Status, project: str, tags: str, due_date: datetime | None) -> DBResponse:
        # add a todo to the db
        try:
            id = insert_todo(self._session, description, priority, status, project, tags, due_date)
            return DBResponse([TodoItem(id, description, priority, status, project, tags, due_date)], SUCCESS)
        except OSError:
            return DBResponse([], DB_INSERT_ERROR)
            
    def get_todo(self, todo_id: int) -> DBResponse:
        # get a todo from the db
        try:
            todo = get_todo(self._session, todo_id)
            return DBResponse([TodoItem(todo.id, todo.description, todo.priority, todo.status, todo.project, todo.tags, todo.due_date)], SUCCESS)
        except OSError:
            return DBResponse([], DB_READ_ERROR)
        except:
            return DBResponse([], DB_READ_ERROR)

    def read_todos(self) -> DBResponse:
        # read all the todos from the db
        try:
            todo_list = get_todo_list(self._session)
            return DBResponse(todo_list, SUCCESS)

        except OSError:  # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)

    def modify_todo(self, id: int, description: str, priority: Priority, status: Status, project: str, tags: str, due_date: datetime | None) -> DBResponse:
        # update a todo in the db
        try:
            update_todo(self._session, id, description, priority, status, project, tags, due_date)
            return DBResponse([TodoItem(id, description, priority, status, project, tags, due_date)], SUCCESS)
        except OSError:
            return DBResponse([], DB_UPDATE_ERROR)
    
    def remove_todo(self, id: int) -> DBResponse:
        # remove a todo from the db
        remove = remove_todo(self._session, id)
        logger.info(f"remove: {remove}")
        if remove:
            return DBResponse([], DB_DELETE_ERROR)
        else:
            return DBResponse([], SUCCESS)
    
    def remove_all_todos(self) -> DBResponse:
        # remove all todos from the db
        try:
            self._session.query(Todo).delete()
            self._session.commit()
            return DBResponse([], SUCCESS)
        except OSError:
            return DBResponse([], DB_DELETE_ERROR)