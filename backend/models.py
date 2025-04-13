from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    fio = Column(String, index=True)
    role = Column(Integer)
    password = Column(String)
    login = Column(String, unique=True, index=True)
    last_access = Column(Date)
    
    tasks = relationship("Task", back_populates="user")
    assessments = relationship("Assessment", back_populates="user")

class Field(Base):
    __tablename__ = "fields"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    area = Column(Integer)
    status = Column(Integer)
    
    tasks = relationship("Task", back_populates="field")
    seasons = relationship("Season", back_populates="field")
    assessments = relationship("Assessment", back_populates="field")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    field_id = Column(Integer, ForeignKey("fields.id"))
    
    user = relationship("User", back_populates="tasks")
    field = relationship("Field", back_populates="tasks")

class Season(Base):
    __tablename__ = "seasons"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    culture = Column(String)
    field_id = Column(Integer, ForeignKey("fields.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    start_volume = Column(Integer)
    end_volume = Column(Integer)
    
    field = relationship("Field", back_populates="seasons")

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    field_id = Column(Integer, ForeignKey("fields.id"))
    date = Column(Date)
    result = Column(String)
    
    user = relationship("User", back_populates="assessments")
    field = relationship("Field", back_populates="assessments")