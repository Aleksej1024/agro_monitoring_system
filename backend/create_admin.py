import os; from database import engine; from models import Base; Base.metadata.create_all(bind=engine)
from sqlalchemy import create_engine;
from sqlalchemy.orm import sessionmaker;
from models import User;
from auth import get_password_hash;

engine = create_engine("postgresql://admin:admin@localhost:5432/database");
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine);
db = SessionLocal();

# Check if default user already exists
user = db.query(User).filter(User.login == "admin").first();
if not user:
    hashed_password = get_password_hash("admin123");
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