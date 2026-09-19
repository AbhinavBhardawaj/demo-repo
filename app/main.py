from fastapi import FastAPI

from .todos import router as todo_router


app = FastAPI(
    title="IssueMatch Demo API",
    version="1.0.0",
)


@app.get("/")
def health_check():
    return {
        "message": "IssueMatch demo API is running",
    }


app.include_router(todo_router)