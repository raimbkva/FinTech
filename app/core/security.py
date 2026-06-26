import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
import bcrypt
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_STRICTLY_CONFIDENTIAL_KEY_12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Токен живет 1 час


# --- РАБОТА С ПАРОЛЯМИ (Чистый bcrypt) ---

def hash_password(password: str) -> str:
    """Хэширует чистый пароль пользователя для сохранения в БД."""
    # Переводим строку пароля в байты
    password_bytes = password.encode('utf-8')
    # Генерируем соль
    salt = bcrypt.gensalt()
    # Хэшируем и переводим обратно в строку для хранения в БД
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, совпадает ли введенный пароль с хэшем из базы данных."""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    # Проверяем соответствие
    return bcrypt.checkpw(password_bytes, hashed_bytes)


# --- РАБОТА С JWT-ТОКЕНАМИ ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Генерирует JWT-токен для авторизованного пользователя."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Декодирует JWT-токен и проверяет его валидность."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        return payload
    except jwt.PyJWTError:
        return None