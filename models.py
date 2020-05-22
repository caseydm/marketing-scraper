import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, DateTime, Integer, String

Base = declarative_base()


class URLsToTest(Base):
    __tablename__ = 'urls_to_test'
    id = Column(Integer, primary_key=True)
    tested = Column(Boolean)
    url = Column(String)


class TestedURLs(Base):
    __tablename__ = 'tested_urls'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


class Success(Base):
    __tablename__ = 'success'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    is_django = Column(Boolean)
    is_wagtail = Column(Boolean)
    title_text = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
