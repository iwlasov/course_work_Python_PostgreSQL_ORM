import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = sq.Column(sq.Integer, primary_key=True)
    cid = sq.Column(sq.BigInteger, unique=True)

class User_Word(Base):
    __tablename__ = 'user_word'
    id = sq.Column(sq.Integer, primary_key=True)
    eng = sq.Column(sq.String(length=40), unique=False)
    rus = sq.Column(sq.String(length=40), unique=False)
    users_id = sq.Column(sq.Integer, sq.ForeignKey('users.id'), nullable=False)

    users = relationship(Users, backref='user_word')

class Words(Base):
    __tablename__ = 'words'
    id = sq.Column(sq.Integer, primary_key=True)
    eng = sq.Column(sq.String(length=40), unique=True)
    rus = sq.Column(sq.String(length=40), unique=True)

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)