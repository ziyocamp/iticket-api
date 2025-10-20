from .database import Base, engine

from . import models


def create_tables():
    Base.metadata.create_all(engine)

