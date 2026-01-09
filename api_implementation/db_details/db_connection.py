from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import PasswordType
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PSWD = os.getenv('DB_PSWD')
DB_NAME = os.getenv('DB_NAME')
DB_ENDPOINT = os.getenv('DB_ENDPOINT')

DB_URL = f"postgresql://{DB_USERNAME}:{DB_PSWD}@{DB_ENDPOINT}/{DB_NAME}"

engine = create_engine(DB_URL)

SessionCreator = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM
class Base(DeclarativeBase):
    pass

class ChatDetails(Base):
    __tablename__ = "ChatDetails"

    chat_id = Column(String, primary_key=True)
    user_id = Column(String)
    chat_name = Column(String)
    chat_msg = Column(String)
    chat_media = Column(String)
    created_on = Column(DateTime, default=datetime.utcnow)


class UserAccount(Base):
    __tablename__ = "UserAccount"

    user_id = Column(String, primary_key=True)
    mail = Column(String)
    pswd = Column(PasswordType(schemes=['pbkdf2_sha512']))
