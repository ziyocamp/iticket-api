from sqlalchemy.orm import sessionmaker

from app.db.database import engine

LocalSession = sessionmaker(bind=engine)
