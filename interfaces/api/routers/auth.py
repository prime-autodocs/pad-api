from fastapi import APIRouter, HTTPException
from interfaces.api.schemas.auth import LoginRequest
from core.auth import create_access_token
from datetime import timedelta
from core.users import Users

router = APIRouter()

@router.post("/login")
async def login(request: LoginRequest):
    """Endpoint to authenticate a user and return a JWT token.
    Args:
        request (LoginRequest): The login request containing user credentials.
    Returns:
        dict: A dictionary containing the JWT token if authentication is successful.
    Raises:
        HTTPException: If the login credentials are invalid.
    """
    if not Users.login(request.login, request.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(
        data={"sub": request.login},
        expires_delta=timedelta(minutes=30)
    )

    return {"token": token}