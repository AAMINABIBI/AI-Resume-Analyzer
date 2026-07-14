import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Securely grab the database URL directly from Vercel's environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback for local development if DATABASE_URL isn't in system env
if not DATABASE_URL:
    try:
        # Try loading from local .env file only if we have to
        from dotenv import load_dotenv
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
    except ImportError:
        pass

if not DATABASE_URL:
    raise ValueError("Error: DATABASE_URL not found in environment variables!")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "ssl": {}
    }
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
