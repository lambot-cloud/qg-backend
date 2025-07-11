import functools
import traceback
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from quality_gates.settings import settings
from quality_gates.utils.logger import logger


engine = create_async_engine(settings.db_dsn)


class BaseRepository:
    def __init__(self):
        self.engine = engine
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)

    @staticmethod
    def handler(error_text: str):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(self, *args, **kwargs):
                try:
                    async with self.async_session() as session:
                        return await func(self, session, *args, **kwargs)
                except SQLAlchemyError:
                    logger.error(traceback.format_exc())
                    raise Exception(error_text)

            return wrapper
        return decorator
