from fastapi import status, HTTPException

from database.models.users import Users
from database.database import db


class UsersQueries():
    
    table = Users
    
    @classmethod
    def get_user(cls, login: str, password: str):
        """Query to get a user by login and password
        
        Args:
            login (str): login from user
            password (str): password from user
            
        Returns:
            Model Object: User
        """
        user = db.query(Users).filter(Users.login == login).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário não encontrado."
            )
            
        if password != user.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Senha inválida."
            )
        return user