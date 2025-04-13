from sqlalchemy.orm import Session
import models
import schemas
from datetime import date
from auth import get_password_hash

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        login=user.login,
        fio=user.fio,
        role=user.role,
        password=hashed_password,
        last_access=date.today()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    if user_update.fio is not None:
        db_user.fio = user_update.fio
    if user_update.password is not None:
        db_user.password = get_password_hash(user_update.password)
    if user_update.role is not None:
        db_user.role = user_update.role
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

# Field CRUD
def get_field(db: Session, field_id: int):
    return db.query(models.Field).filter(models.Field.id == field_id).first()

def get_fields(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Field).offset(skip).limit(limit).all()

def create_field(db: Session, field: schemas.FieldCreate):
    db_field = models.Field(**field.dict())
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return db_field

def update_field(db: Session, field_id: int, field_update: schemas.FieldUpdate):
    db_field = get_field(db, field_id)
    if not db_field:
        return None
    
    update_data = field_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_field, key, value)
    
    db.commit()
    db.refresh(db_field)
    return db_field

def delete_field(db: Session, field_id: int):
    db_field = get_field(db, field_id)
    if not db_field:
        return False
    db_field.status = 0  # Mark as deleted
    db.commit()
    return True

# Task CRUD
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    update_data = task_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True

# Season CRUD
def get_season(db: Session, season_id: int):
    return db.query(models.Season).filter(models.Season.id == season_id).first()

def get_seasons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Season).offset(skip).limit(limit).all()

def create_season(db: Session, season: schemas.SeasonCreate):
    db_season = models.Season(**season.dict())
    db.add(db_season)
    db.commit()
    db.refresh(db_season)
    return db_season

def update_season(db: Session, season_id: int, season_update: schemas.SeasonUpdate):
    db_season = get_season(db, season_id)
    if not db_season:
        return None
    
    update_data = season_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_season, key, value)
    
    db.commit()
    db.refresh(db_season)
    return db_season

def delete_season(db: Session, season_id: int):
    db_season = get_season(db, season_id)
    if not db_season:
        return False
    db.delete(db_season)
    db.commit()
    return True

# Assessment CRUD
def get_assessment(db: Session, assessment_id: int):
    return db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()

def get_assessments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Assessment).offset(skip).limit(limit).all()

def create_assessment(db: Session, assessment: schemas.AssessmentCreate):
    db_assessment = models.Assessment(**assessment.dict())
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment

def update_assessment(db: Session, assessment_id: int, assessment_update: schemas.AssessmentUpdate):
    db_assessment = get_assessment(db, assessment_id)
    if not db_assessment:
        return None
    
    update_data = assessment_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_assessment, key, value)
    
    db.commit()
    db.refresh(db_assessment)
    return db_assessment

def delete_assessment(db: Session, assessment_id: int):
    db_assessment = get_assessment(db, assessment_id)
    if not db_assessment:
        return False
    db.delete(db_assessment)
    db.commit()
    return True