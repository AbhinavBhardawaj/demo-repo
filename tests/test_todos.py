import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.todos import todos


client = TestClient(app)

AUTH_HEADERS = {
    "Authorization": "Bearer demo-token",
}


@pytest.fixture(autouse=True)
def reset_todos():
    """
    Reset the in-memory database before every test.
    """
    todos.clear()

    todos.extend(
        [
            {
                "id": 1,
                "title": "Learn FastAPI",
                "completed": False,
            },
            {
                "id": 2,
                "title": "Build IssueMatch",
                "completed": False,
            },
            {
                "id": 3,
                "title": "Write tests",
                "completed": False,
            },
        ]
    )

    yield


def test_list_todos():
    response = client.get(
        "/todos/",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_existing_todo():
    response = client.get(
        "/todos/1",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Learn FastAPI"


def test_get_missing_todo():
    response = client.get(
        "/todos/999",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 404


def test_create_todo():
    response = client.post(
        "/todos/",
        headers=AUTH_HEADERS,
        json={
            "title": "Test IssueMatch",
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Test IssueMatch"


def test_update_todo():
    response = client.put(
        "/todos/1",
        headers=AUTH_HEADERS,
        json={
            "title": "Learn FastAPI properly",
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Learn FastAPI properly"


def test_delete_todo():
    response = client.delete(
        "/todos/1",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200


def test_complete_todo():
    response = client.patch(
        "/todos/1/complete",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["completed"] is True


# INTENTIONAL FAILING TEST
#
# This represents the requirement in the GitHub issue:
# "The endpoint should return 404 if the todo does not exist."
def test_complete_missing_todo_returns_404():
    response = client.patch(
        "/todos/999/complete",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 404