from fastapi import APIRouter, Depends, HTTPException

from .auth import verify_token
from .models import Todo, TodoCreate

router = APIRouter(prefix="/todos", tags=["todos"])


# In-memory database for the demo.
todos: list[Todo] = [
    Todo(id=1, title="Learn FastAPI"),
    Todo(id=2, title="Build IssueMatch"),
    Todo(id=3, title="Write tests"),
]


@router.get("/")
def list_todos(user: str = Depends(verify_token)):
    return todos


@router.post("/")
def create_todo(
    todo: TodoCreate,
    user: str = Depends(verify_token),
):
    new_id = max(todo.id for todo in todos) + 1 if todos else 1

    new_todo = Todo(
        id=new_id,
        title=todo.title,
    )

    todos.append(new_todo)

    return new_todo


@router.get("/{todo_id}")
def get_todo(
    todo_id: int,
    user: str = Depends(verify_token),
):
    for todo in todos:
        if todo.id == todo_id:
            return todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found",
    )


@router.put("/{todo_id}")
def update_todo(
    todo_id: int,
    todo: TodoCreate,
    user: str = Depends(verify_token),
):
    for existing_todo in todos:
        if existing_todo.id == todo_id:
            existing_todo.title = todo.title
            return existing_todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found",
    )


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    user: str = Depends(verify_token),
):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {"message": "Todo deleted"}

    raise HTTPException(
        status_code=404,
        detail="Todo not found",
    )


# INTENTIONAL BUG:
# This endpoint is supposed to mark a todo as completed,
# but it currently does not check whether the todo exists correctly.
@router.patch("/{todo_id}/complete")
def complete_todo(
    todo_id: int,
    user: str = Depends(verify_token),
):
    for todo in todos:
        if todo.id == todo_id:
            todo.completed = True
            return todo

    # BUG: wrong status code.
    # The requirement says a missing todo should return 404.
    raise HTTPException(
        status_code=500,
        detail="Todo not found",
    )