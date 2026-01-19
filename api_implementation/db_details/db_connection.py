from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
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
CURR_ENV = os.getenv('CURR_ENV')

if CURR_ENV=='DEVELOPMENT':
    DB_LOCALHOST_ENDPOINT = os.getenv('DB_LOCALHOST_ENDPOINT')
    DB_LOCALHOST_PORT = os.getenv('DB_LOCALHOST_PORT')
    DB_URL = f"postgresql://{DB_USERNAME}:{DB_PSWD}@{DB_LOCALHOST_ENDPOINT}:{DB_LOCALHOST_PORT}/{DB_NAME}"
else:
    DB_URL = f"postgresql://{DB_USERNAME}:{DB_PSWD}@{DB_ENDPOINT}/{DB_NAME}"

engine = create_engine(DB_URL)

SessionCreator = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM
class Base(DeclarativeBase):
    pass

class ChatDetails(Base):
    __tablename__ = "ChatDetails"

    chat_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(String)
    role = Column(String)
    chat_name = Column(String)
    chat_msg = Column(String)
    media_file_path = Column(ARRAY(String))
    created_on = Column(DateTime, default=datetime.now)


class UserAccount(Base):
    __tablename__ = "UserAccount"

    user_id = Column(String, primary_key=True)
    mail = Column(String)
    pswd = Column(String)
    is_active = Column(String)
