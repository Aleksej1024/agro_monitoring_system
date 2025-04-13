from pydantic import BaseModel
from datetime import date
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    role: Optional[int] = None

# User schemas
class UserBase(BaseModel):
    login: str
    fio: str
    role: int

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    last_access: Optional[date] = None
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    fio: Optional[str] = None
    password: Optional[str] = None
    role: Optional[int] = None

# Field schemas
class FieldBase(BaseModel):
    location: str
    area: int
    status: int

class FieldCreate(FieldBase):
    pass

class Field(FieldBase):
    id: int
    
    class Config:
        from_attributes = True

class FieldUpdate(BaseModel):
    location: Optional[str] = None
    area: Optional[int] = None
    status: Optional[int] = None

# Task schemas
class TaskBase(BaseModel):
    description: str
    user_id: int
    field_id: int

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    
    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    description: Optional[str] = None
    user_id: Optional[int] = None
    field_id: Optional[int] = None

# Season schemas
class SeasonBase(BaseModel):
    year: int
    culture: str
    field_id: int
    start_date: date
    end_date: date
    start_volume: int
    end_volume: int

class SeasonCreate(SeasonBase):
    pass

class Season(SeasonBase):
    id: int
    
    class Config:
        from_attributes = True

class SeasonUpdate(BaseModel):
    year: Optional[int] = None
    culture: Optional[str] = None
    field_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    start_volume: Optional[int] = None
    end_volume: Optional[int] = None

# Assessment schemas
class AssessmentBase(BaseModel):
    type: int
    user_id: int
    field_id: int
    date: date
    result: str

class AssessmentCreate(AssessmentBase):
    pass

class Assessment(AssessmentBase):
    id: int
    
    class Config:
        from_attributes = True

class AssessmentUpdate(BaseModel):
    type: Optional[int] = None
    user_id: Optional[int] = None
    field_id: Optional[int] = None
    date: Optional[date] = None
    result: Optional[str] = None