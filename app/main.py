from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from decimal import Decimal

from app.database.db import get_db
from app.database.models import User, Category, Transaction, DailyLimit
from app.core.schemas import UserRegister, UserLogin, CategoryCreate, TransactionCreate, LimitUpdate
from app.core.security import hash_password, verify_password, create_access_token
from app.core.dependencies import get_current_user
from app.services.budget_tasks import check_daily_limit

app = FastAPI(title="FinTrack API", description="Личный трекер расходов с контролем лимитов")

# --- 1. АВТОРИЗАЦИЯ И РЕГИСТРАЦИЯ ---

@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    # Проверяем, существует ли уже такой email
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    
    # Хэшируем пароль твоей функцией из Роли 3
    hashed = hash_password(data.password)
    
    new_user = User(username=data.username, email=data.email, password_hash=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Создаем дефолтный лимит для пользователя (например, 0 - не активен)
    default_limit = DailyLimit(user_id=new_user.id, limit_amount=Decimal("0.00"), is_active=False)
    db.add(default_limit)
    db.commit()
    
    return {"message": "Пользователь успешно создан", "user_id": new_user.id}


@app.post("/auth/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    
    # Генерируем JWT-токен твоей функцией
    token = create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}


# --- 2. УПРАВЛЕНИЕ КАТЕГОРИЯМИ (CRUD) ---

@app.post("/categories")
def create_category(data: CategoryCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    category = Category(user_id=current_user.id, name=data.name, type=data.type, color=data.color, icon=data.icon)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@app.get("/categories")
def get_categories(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Category).filter(Category.user_id == current_user.id).all()


# --- 3. ДОБАВЛЕНИЕ РАСХОДОВ + ФОНОВАЯ ЗАДАЧА ТВОЕЙ РОЛИ ---

@app.post("/expenses", status_code=status.HTTP_201_CREATED)
def add_expense(
    data: TransactionCreate, 
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Проверяем существование категории
    category = db.query(Category).filter(Category.id == data.category_id, Category.user_id == current_user.id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    # 1. Сохраняем расход в базу (работа Разработчика 1)
    new_transaction = Transaction(
        user_id=current_user.id,
        category_id=data.category_id,
        amount=data.amount,
        comment=data.comment,
        transaction_date=data.transaction_date
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    # Подтягиваем данные по лимитам для нашей фоновой задачи
    user_limit = db.query(DailyLimit).filter(DailyLimit.user_id == current_user.id).first()
    
    if user_limit and user_limit.is_active:
        # Считаем, сколько было потрачено сегодня ДО этой транзакции
        total_today_before = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
            Transaction.user_id == current_user.id,
            Transaction.transaction_date == data.transaction_date,
            Transaction.id != new_transaction.id  # Исключаем текущую транзакцию
        ).scalar()
        
        # 2. Вызываем ТВОЮ фоновую задачу для проверки лимитов
        background_tasks.add_task(
            check_daily_limit,
            user_id=current_user.id,
            current_expense=data.amount,
            daily_limit=user_limit.limit_amount,
            total_spent_today=Decimal(str(total_today_before))
        )
        
    return {"message": "Расход успешно записан", "transaction": new_transaction.id}


# --- 4. УСТАНОВКА ЛИМИТА ---

@app.put("/user/limit")
def update_limit(data: LimitUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    limit = db.query(DailyLimit).filter(DailyLimit.user_id == current_user.id).first()
    if not limit:
        limit = DailyLimit(user_id=current_user.id)
        db.add(limit)
        
    limit.limit_amount = data.limit_amount
    limit.is_active = True
    db.commit()
    return {"message": "Дневной лимит успешно обновлен", "limit": limit.limit_amount}


# --- 5. АНАЛИТИКА (Финальный бизнес-результат) ---

@app.get("/analytics")
def get_analytics(start_date: date, end_date: date, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Возвращает срез данных: траты по дням и распределение по категориям."""
    
    # 1. Общая сумма трат за каждый день периода
    daily_spent = db.query(
        Transaction.transaction_date.label("date"),
        func.sum(Transaction.amount).label("total")
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_date >= start_date,
        Transaction.transaction_date <= end_date
    ).group_by(Transaction.transaction_date).all()
    
    # 2. Распределение расходов по категориям
    category_distribution = db.query(
        Category.name.label("category"),
        func.sum(Transaction.amount).label("total")
    ).join(Transaction, Transaction.category_id == Category.id).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_date >= start_date,
        Transaction.transaction_date <= end_date
    ).group_by(Category.name).all()
    
    return {
        "period": {"start": start_date, "end": end_date},
        "daily_expenses": [{"date": str(d.date), "total_amount": d.total} for d in daily_spent],
        "by_categories": [{"category": c.category, "total_amount": c.total} for c in category_distribution]
    }