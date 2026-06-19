from decimal import Decimal
import os
from app.services.budget_tasks import check_daily_limit

print("--- Сценарий 1: Траты в пределах нормы ---")
# Пользователь ID 1, расход 1500, лимит 5000, уже потрачено сегодня 2000 (итого 3500 из 5000)
check_daily_limit(user_id=1, current_expense=Decimal("1500.00"), daily_limit=Decimal("5000.00"), total_spent_today=Decimal("2000.00"))


print("\n--- Сценарий 2: Превышение лимита ---")
# Пользователь ID 1, расход 2000, лимит 5000, уже потрачено сегодня 4000 (итого 6000 из 5000 -> превышение на 1000)
check_daily_limit(user_id=1, current_expense=Decimal("2000.00"), daily_limit=Decimal("5000.00"), total_spent_today=Decimal("4000.00"))


print("\nПроверяем, создался ли файл логов...")
if os.path.exists("app.log"):
    print("Успех! Файл app.log создан. Вот его содержимое:")
    with open("app.log", "r", encoding="utf-8") as f:
        print(f.read())
else:
    print("Ошибка: Файл логов не найден.")