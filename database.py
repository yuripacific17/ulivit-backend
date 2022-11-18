from sqlalchemy import create_engine, schema
from sqlalchemy_utils import database_exists, create_database

from sqlalchemy.orm import sessionmaker, declarative_base

# set up test database for unit testing
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/ulivit"
SQLALCHEMY_SCHEMA_NAME = "CCC"


# create database if doesn't exist
def validate_database():
    if not database_exists(SQLALCHEMY_DATABASE_URL):
        create_database(SQLALCHEMY_DATABASE_URL)
    return None

validate_database()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# create schema if doesn't exist
if not engine.dialect.has_schema(engine, SQLALCHEMY_SCHEMA_NAME):
    engine.execute(schema.CreateSchema(SQLALCHEMY_SCHEMA_NAME))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base
