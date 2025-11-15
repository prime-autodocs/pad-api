import pytest

from database.models.users import Users
from database.session import db_session
from database.queries.users import UsersQueries


def _create_user(login: str = "user@test.com", password: str = "secret") -> Users:
    with db_session() as db:
        user = Users(
            login=login,
            password=password,
            username="Test User",
            email=login,
        )
        db.add(user)
        db.commit()
        return user


def test_users_queries_get_user_ok() -> None:
    user = _create_user()

    found = UsersQueries.get_user(login=user.login, password=user.password)

    assert found.login == user.login


def test_users_queries_invalid_password_raises() -> None:
    user = _create_user(login="other@test.com", password="correct")

    with pytest.raises(Exception):
        UsersQueries.get_user(login=user.login, password="wrong")


