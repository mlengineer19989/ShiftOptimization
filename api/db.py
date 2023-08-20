import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "3306")

#DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8"
ASYNC_DB_URL = (
    f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/demo?charset=utf8"
)



# db_engine = create_engine(DB_URL, echo=True)
# db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

Base = declarative_base()

# def get_db():
#     with db_session() as session:
#         yield session

async def get_db():
    async with async_session() as session:
        yield session