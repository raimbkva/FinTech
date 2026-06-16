Структура базы данных
Таблицы
users — пользователи
categories — категории операций
transactions — финансовые операции
daily_limits — дневные лимиты
Установка проекта
1. Клонировать репозиторий
git clone <repository_url>
cd fintrack
2. Создать виртуальное окружение
python -m venv .venv
Активировать:
Windows
.venv\Scripts\activate
3. Установить зависимости
pip install -r requirements.txt
4. Создать PostgreSQL базу данных
Создать базу данных:
fintrack_db
5. Настроить .env
Создать файл .env в корне проекта.
Пример:
DATABASE_URL=postgresql://postgres:your_password(пароль сюда вводи)@localhost:5432/fintrack_db
6. Применить миграции
alembic upgrade head