from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


METADATA = MetaData(
    naming_convention={
        "all_column_names": lambda constraint, table: "_".join(
            [column.name for column in constraint.columns.values()],
        ),
        # A string mnemonic for primary key.
        "pk": "pk__%(table_name)s",
        # A string mnemonic for index.
        "ix": "ix__%(table_name)s__%(all_column_names)s",
        # A string mnemonic for foreign key.
        "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
        # A string mnemonic for unique constraint.
        "uq": "uq__%(table_name)s__%(all_column_names)s",
        # A string mnemonic for check constraint.
        "ck": "ck__%(table_name)s__%(constraint_name)s",
    },
)

Base = declarative_base(metadata=METADATA)
