from sqlalchemy import Column, String, Integer, Boolean
from database import Base

class TodoModel(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String(16), index=True)
    description = Column(String(255), index = True, nullable = True)
    completed = Column (Boolean, default = False)