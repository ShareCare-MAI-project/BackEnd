from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import DATABASE_URL


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables() -> None:
    Base.metadata.create_all(engine)


Session = sessionmaker(engine)


def default_db_request(request):
    """
    Функция-обёртка для дефолтных запросов в declarative дб (rollback при ошибке и commit, если всё ок)

    >> default_db_request(UserBase(id=str(uuid.uuid4()), name = "sample").create_user)

    ВАЖНО: Прокидывает ошибку наверх
    """
    with Session() as session:
        try:
            request(session)
        except:
            session.rollback()
            raise
        else:
            session.commit()
