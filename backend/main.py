from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import List
import crud, models, schemas, auth
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from datetime import date
import cv
import json
import os
from minio import Minio
from fastapi.responses import StreamingResponse
import mimetypes
from minio.error import S3Error
import io

models.Base.metadata.create_all(bind=engine)

minio_client = Minio(
    'minio:9000',
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

app = FastAPI()

# Authentication
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(auth.get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": str(user.id), "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_active_user)):
    return current_user

# User routes
@app.post("/users/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_main_agronom_permission(current_user)
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_main_agronom_permission(current_user)
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_main_agronom_permission(current_user)
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int, 
    user_update: schemas.UserUpdate,
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_main_agronom_permission(current_user)
    db_user = crud.update_user(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(
    user_id: int, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_main_agronom_permission(current_user)
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Field routes
@app.post("/fields/", response_model=schemas.Field)
def create_field(
    field: schemas.FieldCreate, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_agronom_permission(current_user)
    return crud.create_field(db=db, field=field)

@app.get("/fields/", response_model=List[schemas.Field])
def read_fields(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    fields = crud.get_fields(db, skip=skip, limit=limit)
    return fields

@app.get("/fields/{field_id}", response_model=schemas.Field)
def read_field(
    field_id: int, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_field = crud.get_field(db, field_id=field_id)
    if db_field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    return db_field

@app.put("/fields/{field_id}", response_model=schemas.Field)
def update_field(
    field_id: int, 
    field_update: schemas.FieldUpdate,
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_agronom_permission(current_user)
    db_field = crud.update_field(db, field_id, field_update)
    if db_field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    return db_field

@app.delete("/fields/{field_id}")
def delete_field(
    field_id: int, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_agronom_permission(current_user)
    success = crud.delete_field(db, field_id)
    if not success:
        raise HTTPException(status_code=404, detail="Field not found")
    return {"message": "Field deleted successfully"}

# Task routes
@app.post("/tasks/", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_agronom_permission(current_user)
    return crud.create_task(db=db, task=task)

@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(
    task_id: int, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int, 
    task_update: schemas.TaskUpdate,
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_agronom_permission(current_user)
    db_task = crud.update_task(db, task_id, task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_agronom_permission(current_user)
    success = crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

# Season routes
@app.post("/seasons/", response_model=schemas.Season)
def create_season(
    season: schemas.SeasonCreate, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_agronom_permission(current_user)
    return crud.create_season(db=db, season=season)

@app.get("/seasons/", response_model=List[schemas.Season])
def read_seasons(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    seasons = crud.get_seasons(db, skip=skip, limit=limit)
    return seasons

@app.get("/seasons/{season_id}", response_model=schemas.Season)
def read_season(
    season_id: int, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_season = crud.get_season(db, season_id=season_id)
    if db_season is None:
        raise HTTPException(status_code=404, detail="Season not found")
    return db_season

@app.put("/seasons/{season_id}", response_model=schemas.Season)
def update_season(
    season_id: int, 
    season_update: schemas.SeasonUpdate,
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_agronom_permission(current_user)
    db_season = crud.update_season(db, season_id, season_update)
    if db_season is None:
        raise HTTPException(status_code=404, detail="Season not found")
    return db_season

@app.delete("/seasons/{season_id}")
def delete_season(
    season_id: int, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_agronom_permission(current_user)
    success = crud.delete_season(db, season_id)
    if not success:
        raise HTTPException(status_code=404, detail="Season not found")
    return {"message": "Season deleted successfully"}

# Assessment routes
@app.post("/assessments/", response_model=schemas.Assessment)
async def create_assessment(
    type: int = Form(...),
    field_id: int = Form(...),
    date: date = Form(...),
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user),
    file: UploadFile = File(...)
):
    predicted_class = cv.predict(await file.read())
    assessment = schemas.AssessmentCreate(
        type=type,
        field_id=field_id,
        date=date,
        result=predicted_class,
        user_id=current_user.id
    )
    db_assessment = crud.create_assessment(db=db, assessment=assessment)

    # 3. Сохранение файла в MinIO
    file_extension = os.path.splitext(file.filename)[1]  # .jpg, .png и т.д.
    object_name = f"{db_assessment.id}{file_extension}"  # Имя файла = ID оценки
    
    try:
        # Перематываем файл (так как file.read() уже вызывался)
        await file.seek(0)
        
        # Загружаем в MinIO
        minio_client.put_object(
            bucket_name='app',
            object_name=object_name,
            data=file.file,
            length=file.size,
            content_type=file.content_type
        )
    except S3Error as e:
        # Если ошибка, можно откатить создание записи или просто залогировать
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при загрузке файла в MinIO: {e}"
        )

    return db_assessment

#Get image
@app.get("/image/{file_name}")
async def get_image(file_name: str):
    bucket_name='app'
    if not minio_client.bucket_exists(bucket_name):
        raise HTTPException(status_code=404, detail="Bucket not found")
    try:
        response = minio_client.get_object(bucket_name, file_name)
        content_type, _ = mimetypes.guess_type(file_name)
        if content_type is None:
            content_type = "application/octet-stream" 
        data = io.BytesIO(response.read())
        response.close()
        response.release_conn()
        return StreamingResponse(data, media_type=content_type)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File not found or error: {str(e)}")


@app.get("/assessments/", response_model=List[schemas.Assessment])
def read_assessments(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    assessments = crud.get_assessments(db, skip=skip, limit=limit)
    return assessments

@app.get("/assessments/{assessment_id}", response_model=schemas.Assessment)
def read_assessment(
    assessment_id: int, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_assessment = crud.get_assessment(db, assessment_id=assessment_id)
    if db_assessment is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return db_assessment

@app.put("/assessments/{assessment_id}", response_model=schemas.Assessment)
def update_assessment(
    assessment_id: int, 
    assessment_update: schemas.AssessmentUpdate,
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_agronom_permission(current_user)
    db_assessment = crud.update_assessment(db, assessment_id, assessment_update)
    if db_assessment is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return db_assessment

@app.delete("/assessments/{assessment_id}")
def delete_assessment(
    assessment_id: int, 
    db: Session = Depends(auth.get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    auth.check_agronom_permission(current_user)
    success = crud.delete_assessment(db, assessment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return {"message": "Assessment deleted successfully"}