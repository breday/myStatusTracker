# models go here models.py
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """
    Create users table
    """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    is_admin = Column(Boolean,default =False)
    f_name = Column(String(250), nullable=False)
    l_name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)



    
class Issue(Base):

    """
    Create issues table
    """
    __tablename__ = 'issues'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(250), nullable = True)
    priority = Column(String(20), nullable= True)
    department = Column(String(250), nullable= True)
    issue_status = Column(String(250), nullable= True)
    comments = Column(String(250), nullable= True)

engine = create_engine('sqlite:///tracker.db')
Base.metadata.create_all(engine)




