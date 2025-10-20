# from sqlalchemy import create_engine, URL
# from sqlalchemy.ext.declarative import declarative_base

# from app.core.config import config


# BATABASE_URL = URL.create(
#     drivername='postgresql+psycopg2',
#     host=config.DB_HOST,
#     port=config.DB_PORT,
#     username=config.DB_USER,
#     password=config.DB_PASS,
#     database=config.DB_NAME
# )

# engine = create_engine(url=BATABASE_URL)
# Base = declarative_base()


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
