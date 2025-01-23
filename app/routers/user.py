from passlib.hash import bcrypt
from fastapi import HTTPException, Body, APIRouter
from db.connection import conn
from middlewares.auth import create_access_token
import datetime

router = APIRouter()
cursor = conn.cursor()

@router.post("/register")
def register_user(username: str = Body(...), password: str = Body(...)):
    cursor.execute("SELECT username FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    password_hash = bcrypt.hash(password)
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
    conn.commit()
    return {"message": "Usuario registrado"}

@router.post("/login")
def login_user(username: str = Body(...), password: str = Body(...)):
    cursor.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    if not result or not bcrypt.verify(password, result[0]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    access_token_expires = datetime.timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}