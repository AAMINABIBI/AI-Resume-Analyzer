import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Try loading from local .env file (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If dotenv is missing (like on Vercel), we pass gracefully
    pass

# Securely grab the database URL directly from Vercel's environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

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
