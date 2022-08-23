from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def craft_session(func):
    engine = create_engine(f'sqlite:///whoami.db', echo=True)

    def wrapper(*args, **kwargs):
        with Session(engine) as session:
            session.begin()
            try:
                result = func(session, *args, **kwargs)
            except:
                session.rollback()
                raise
            else:
                session.commit()
        return result
    return wrapper