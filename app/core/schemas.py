from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal
from datetime import date
from typing import Optional

# --- Схемы для Аутентификации ---
class UserRegister(BaseModel):
    username: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- Схемы для Категорий ---
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = "expense" # по умолчанию расход
    color: Optional[str] = None
    icon: Optional[str] = None

# --- Схемы для Расходов (Транзакций) ---
class TransactionCreate(BaseModel):
    category_id: int
    amount: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2)
    comment: Optional[str] = None
    transaction_date: date = Field(default_factory=date.today)

# --- Схема для Настройки Лимита ---
class LimitUpdate(BaseModel):
    limit_amount: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2)