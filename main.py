"""
Тестирование подключения к PostgreSQL
и ORM-моделей SQLAlchemy.

Файл для проверки подключения в бдшке;
 получения данных через ORM;
"""

from app.database.db import SessionLocal
from app.database.models import (
    User,
    Category,
    Transaction,
    DailyLimit
)

# Создаем сессию подключения к БД
session = SessionLocal()

try:
    # Получаем пользователей
    users = session.query(User).all()

    print("=== Пользователи ===")

    for user in users:
        print(
            f"ID: {user.id}, "
            f"Username: {user.username}, "
            f"Email: {user.email}"
        )

    # Получаем категории
    categories = session.query(Category).all()

    print("\n=== Категории ===")

    for category in categories:
        print(
            f"ID: {category.id}, "
            f"Название: {category.name}, "
            f"Тип: {category.type}"
        )

    # Получаем транзакции
    transactions = session.query(Transaction).all()

    print("\n=== Финансовые операции ===")

    for transaction in transactions:
        print(
            f"ID: {transaction.id}, "
            f"Сумма: {transaction.amount}, "
            f"Комментарий: {transaction.comment}, "
            f"Дата: {transaction.transaction_date}"
        )

    # Получаем лимиты
    limits = session.query(DailyLimit).all()

    print("\n=== Дневные лимиты ===")

    for limit in limits:
        print(
            f"Пользователь ID: {limit.user_id}, "
            f"Лимит: {limit.limit_amount}, "
            f"Активен: {limit.is_active}"
        )

except Exception as e:
    print("Ошибка:")
    print(e)

finally:
    # Закрываем подключение
    session.close()
from app.database.db import SessionLocal
from app.database.models import User, Category, Transaction, DailyLimit


session = SessionLocal()

try:
    users = session.query(User).all()

    print("Пользователи:")
    for user in users:
        print(user.id, user.username, user.email)

    categories = session.query(Category).all()

    print("\nКатегории:")
    for category in categories:
        print(category.id, category.name, category.type)

    transactions = session.query(Transaction).all()

    print("\nОперации:")
    for transaction in transactions:
        print(
            transaction.id,
            transaction.amount,
            transaction.type,
            transaction.comment,
            transaction.transaction_date
        )

finally:
    session.close()