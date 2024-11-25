from fastapi import FastAPI, Depends
from pydantic import BaseModel
from database import engine, Sessionlocal
from sqlalchemy.orm import Session
from typing import Optional, List
from models import TodoModel

app = FastAPI()


TodoModel.metadata.create_all(bind=engine)

class TodoItem(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoItem):
    pass

class TodoUpdate(TodoItem):
    pass

class TodoResponse(TodoItem): 
    id: int

    class Config:
        orm_mode = True

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/todos", response_model = List[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoModel).all()
    return todos

@app.get("/todo/{id}", response_model = TodoResponse)
def get_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == id).first()
    return todo


@app.post("/todo", response_model = TodoResponse)
def add_todo(todo: TodoItem, db: Session = Depends(get_db)):
    todo_item = TodoModel(title = todo.title, description= todo.description, completed= todo.completed)
    db.add(todo_item)
    db.commit()
    db.refresh(todo_item)
    return todo_item
    

@app.delete("/todo/{id}", response_model = TodoResponse)
def delete_todo(id: int, db: Session = Depends(get_db)):
     todo = db.query(TodoModel).filter(TodoModel.id == id).first()
     db.delete(todo)
     db.commit()
     return todo
    