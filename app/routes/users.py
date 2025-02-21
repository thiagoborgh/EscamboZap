from fastapi import APIRouter, HTTPException, Depends
from app.models import User, UserCreate
from app.services.auth import get_password_hash, create_access_token, authenticate_user
from app.database import Database

router = APIRouter()
db = Database()

@router.post("/register", response_model=User)
def register_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    with db.connect() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           (user.username, hashed_password))
            conn.commit()
            user_id = cursor.lastrowid
            return User(id=user_id, username=user.username)
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Username already registered")

@router.post("/login")
def login_user(username: str, password: str):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}