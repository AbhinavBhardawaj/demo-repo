# IssueMatch Demo Repository

A small FastAPI Todo API used to demonstrate the IssueMatch GitHub App.

The repository intentionally contains a bug so that IssueMatch can analyze
a contributor's proposed solution against the actual repository context.

## Project Structure

```text
app/
├── __init__.py
├── main.py
├── auth.py
├── todos.py
└── models.py

tests/
├── test_auth.py
└── test_todos.py

README.md
requirements.txt