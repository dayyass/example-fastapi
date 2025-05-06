from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# import psycopg
# from psycopg.rows import dict_row
# import time

# # while True:
# try:
#     conn = psycopg.connect(
#         conninfo="host=localhost port=5432 user=postgres password=postgres dbname=fastapi",
#         row_factory=dict_row,
#     )
#     cursor = conn.cursor()
#     print("Database connection was successful")
#     # break
# except Exception as error:
#     print("Connection to database failed")
#     print(f"Error: {error}")
#     # time.sleep(2)
