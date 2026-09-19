from fastapi import HTTPException
import pytest

from app.auth import verify_token


def test_valid_token():
    result = verify_token("Bearer demo-token")

    assert result == "demo-user"


def test_invalid_token():
    with pytest.raises(HTTPException) as exc_info:
        verify_token("Bearer wrong-token")

    assert exc_info.value.status_code == 401


def test_missing_token():
    with pytest.raises(HTTPException) as exc_info:
        verify_token(None)

    assert exc_info.value.status_code == 401