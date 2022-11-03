from sqlalchemy import (Column, Integer, String,
                        create_engine)
from sqlalchemy.orm import sessionmaker, declarative_base

base = declarative_base()

class DBUser(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50))
    password = Column(String(50))
    rank = Column(Integer)

class DatabaseManager:
    def __init__(self, database_url):
        db = create_engine(database_url, echo=True)
        self.create_session = sessionmaker(db)
        base.metadata.create_all(db)
        self.create_initial_data()

    def create_initial_data(self):
        with self.create_session() as session:
            session.add(DBUser(
                id=None,
                email="admin@example.de",
                password="admin",
                rank=0,
            ))
            session.commit()
