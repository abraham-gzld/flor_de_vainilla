from sqlalchemy import create_engine
from sqlalchemy import text

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from dotenv import load_dotenv

import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

try:

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT 1")
        )

        print("Database connected successfully")

except Exception as e:

    print("Database connection error:")
    print(e)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()