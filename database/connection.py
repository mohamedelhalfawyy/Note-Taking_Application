from sqlalchemy import create_engine
from urllib.parse import quote_plus
from fastapi import HTTPException
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker


def database_connection():
    try:
        load_dotenv()

        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_USER = os.getenv("DB_USER", "postgres")
        DB_PASS = quote_plus(os.getenv("DB_PASS", "ENTER YOUR PASSWORD HERE"))
        DB_NAME = os.getenv("DB_NAME", "uktob_dev")

        connection_string = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

        engine = create_engine(connection_string)

        print('Connected to Database!')

        return engine
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

def get_db():
    engine = database_connection()

    sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()