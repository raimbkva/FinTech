from decimal import Decimal
from app.core.logger import logger

def check_daily_limit(user_id: int, current_expense: Decimal, daily_limit: Decimal, total_spent_today: Decimal):
    """
    Фоновая задача для проверки дневного лимита.
    Вызывается автоматически после добавления нового расхода.
    """
    # Считаем, сколько пользователь потратил с учетом только что добавленного расхода
    new_total = total_spent_today + current_expense
    
    logger.info(f"Проверка лимита для пользователя ID {user_id}. Расход: {current_expense}, Всего за день: {new_total}/{daily_limit}")
    
    # Если текущие траты превысили установленный лимит
    if new_total > daily_limit:
        # Вычисляем сумму превышения
        overdraft = new_total - daily_limit
        # Записываем строгое предупреждение в логи (WARN/WARNING)
        logger.warning(
            f"ПРЕВЫШЕНИЕ ЛИМИТА! Пользователь ID {user_id} превысил дневной лимит ({daily_limit}) на сумму: {overdraft}"
        )