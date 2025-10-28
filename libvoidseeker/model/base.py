from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

URI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg://botUser:botPass@db:5432/voidseeker'

ENGINE = create_engine(URI, isolation_level="READ COMMITTED", pool_pre_ping=True, pool_recycle=3600)

ModelBase = declarative_base()

def get_base():
    return {'base': ModelBase, 'sqlalchemy_url': URI }