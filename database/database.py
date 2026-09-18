from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine("postgresql+psycopg://localhost/warehouse")


class Base(DeclarativeBase):
    pass


Session = sessionmaker(bind=engine)
