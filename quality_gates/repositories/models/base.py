from sqlalchemy.orm import DeclarativeBase
from quality_gates.settings import settings

DB_DSN = settings.db_dsn


class Base(DeclarativeBase):
    pass
