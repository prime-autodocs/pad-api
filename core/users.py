from database.queries.users import UsersQueries
from database.models.users import Users

class Users:
    
    @classmethod
    def login(cls, login: str, password: str) -> bool:
        """function to login
        
        Args:
            login (str): login from user
            password (str): password from user
            
        Returns:
            bool: True if user is valid
        """
        user = UsersQueries.get_user(login=login, password=password)
        if user:
            return True