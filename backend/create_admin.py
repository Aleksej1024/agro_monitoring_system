import os; from database import engine; from models import Base; Base.metadata.create_all(bind=engine)
from sqlalchemy import create_engine;
from sqlalchemy.orm import sessionmaker;
from models import User;
from passlib.context import CryptContext

engine = create_engine("postgresql://admin:admin@localhost:5432/database");
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine);
db = SessionLocal();

# Check if default user already exists
user = db.query(User).filter(User.login == "admin").first();
if not user:
    #password = password123
    pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("password123")
    default_user = User(
        fio="Главный Агроном",
        role=1,
        password=hashed_password,
        login="admin"
    );
    db.add(default_user);
    db.commit();
    print("Admin Created!")
db.close();
print("End")