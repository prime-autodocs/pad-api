from fastapi import APIRouter
from core.users import Users

router = APIRouter()

@router.get("/")
async def login(login: str, password: str) -> bool:
    """Endpoint that return a list of all vehicles from a customer
    
    Args:
        login (str): login from user
        password (str): password from user  
        
    Returns:
        bool: True if user is valid
    """
    valid = Users.login(login, password)
    return valid