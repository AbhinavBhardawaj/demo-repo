from fastapi import Header, HTTPException


def verify_token(authorization: str | None = Header(default=None)) -> str:
    """
    Very simple demo authentication.

    Expected header:
        Authorization: Bearer demo-token
    """

    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Authorization header is required",
        )

    if authorization != "Bearer demo-token":
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    return "demo-user"