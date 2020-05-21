import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, DateTime, Integer, String

Base = declarative_base()


class TestedURLs(Base):
    __tablename__ = 'tested_urls'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    url = Column(String, nullable=False)


class Success(Base):
    __tablename__ = 'success'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    url = Column(String, nullable=False)
    is_django = Column(Boolean, nullable=False)
    is_wagtail = Column(Boolean, nullable=False)
