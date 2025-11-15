from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from database.database import engine


# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency-style generator para ser usado com FastAPI:

    def endpoint(db: Session = Depends(get_db)):
        ...
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def db_session():
    """
    Helper para uso fora das dependências do FastAPI.

    Exemplo:
        with db_session() as db:
            result = db.query(Model).all()
    """
    db = SessionLocal()
    try:
        yield db
        # commit explícito fica sob responsabilidade de quem usa
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


