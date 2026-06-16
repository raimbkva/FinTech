"""
ORM модели базы данных FinTrack.
"""
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
    Text,
    Date,
    Boolean,
    TIMESTAMP
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.db import Base

# Таблица пользователей системы
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    categories = relationship(
        "Category",
        back_populates="user",
        cascade="all, delete"
    )

    transactions = relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete"
    )

    daily_limit = relationship(
        "DailyLimit",
        back_populates="user",
        uselist=False,
        cascade="all, delete"
    )

# Таблица категорий финансовых операций
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    name = Column(
        String(100),
        nullable=False
    )

    type = Column(
        String(20),
        default="expense",
        nullable=False
    )

    color = Column(String(20))

    icon = Column(String(50))

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="categories"
    )

    transactions = relationship(
        "Transaction",
        back_populates="category"
    )

# Таблица финансовых операций пользователя
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    type = Column(
        String(20),
        default="expense",
        nullable=False
    )

    comment = Column(Text)

    transaction_date = Column(
        Date,
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="transactions"
    )

    category = relationship(
        "Category",
        back_populates="transactions"
    )

# Таблица дневных лимитов пользователя
class DailyLimit(Base):
    __tablename__ = "daily_limits"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    limit_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship(
        "User",
        back_populates="daily_limit"
    )