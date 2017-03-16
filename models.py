# models go here models.py
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from models import Base, issues, user

Base = declarative_base()


class User(Base):
    """
    Create users table
    """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_type = Column(String(250), nullable=False)
    f_name = Column(String(250), nullable=False)
    s_name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    
class Issue(Base):

    """
    Create issues table
    """
    __tablename__ = 'issues'

    id = Column(Integer, primary_key=True)
    Title = Column(String(80), nullable=False)
    description = Column(String(250), nullable = True)
    priority = Column(String(20), nullable= True)
    department = Column(String(250), nullable= True)
    issue_status = Column(String(250), nullable= True)
    remarks = Column(String(250), nullable= True)

engine = create_engine('sqlite:///tracker.db')
Base.metadata.create_all(engine)





