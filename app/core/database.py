from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_utils import database_exists, create_database

from app.core.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_DB


class Base(DeclarativeBase):
    pass


# host is always 'postgres' cuz we host server and the db in the same container
SYNC_POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:{POSTGRES_PORT}/{POSTGRES_DB}"
ASYNC_POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:{POSTGRES_PORT}/{POSTGRES_DB}"

async_engine = create_async_engine(ASYNC_POSTGRES_URL, echo=True)
sync_engine = create_engine(SYNC_POSTGRES_URL, echo=True)


def create_db_and_tables() -> None:
    Base.metadata.create_all(sync_engine)


def setup_db() -> None:
    if not database_exists(sync_engine.url):
        create_database(sync_engine.url)
    create_db_and_tables()


AsyncSession = async_sessionmaker(async_engine, expire_on_commit=False)


async def default_async_db_request(request):
    """
    Функция-обёртка для дефолтных запросов в declarative дб (rollback при ошибке и commit, если всё ок)

    >> default_async_db_request(UserBase(id=str(uuid.uuid4()), name = "sample").create_user)

    ВАЖНО: Прокидывает ошибку наверх
    """
    async with AsyncSession() as session:
        try:
            result = request(session)
            if hasattr(result, '__await__'):
                result = await result
            await session.commit()
            return result
        except Exception as e:
            await session.rollback()
            # logging.error(e)
            raise
