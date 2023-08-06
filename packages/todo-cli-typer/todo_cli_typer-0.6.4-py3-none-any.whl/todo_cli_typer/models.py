# #!/usr/bin/env python3


# from sqlmodel import Field, Relationship, SQLModel

# class TodoBase(SQLModel):
# 	description: str
#     priority: str
#     status = Column(Enum(Status))
#     project = Column(String)
#     tags = Column(String)
#     due_date = Column('Due Date', DateTime, nullable=True)

# class Todo(SQLModel, table=True):

# # class Team(SQLModel, table=True):
# #     id: Optional[int] = Field(default=None, primary_key=True)
# #     name: str = Field(index=True)
# #     headquarters: str

# #     heroes: List["Hero"] = Relationship(back_populates="team")


# # class Hero(SQLModel, table=True):
# #     id: Optional[int] = Field(default=None, primary_key=True)
# #     name: str = Field(index=True)
# #     secret_name: str
# #     age: Optional[int] = Field(default=None, index=True)

# #     team_id: Optional[int] = Field(default=None, foreign_key="team.id")
# #     team: Optional[Team] = Relationship(back_populates="heroes")
