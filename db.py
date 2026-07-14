from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Changed '/sys' to '/test' at the end of the URL string
DATABASE_URL = "mysql+pymysql://3Wd4rrDLPhmy8ho.root:y4nVP9NVMYM7FtTF@gateway01.ap-northeast-1.prod.aws.tidbcloud.com:4000/test"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "ssl": {}
    }
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()