import logging
import os

# Путь к файлу, куда будут сохраняться логи
LOG_FILE_PATH = "app.log"

# Настраиваем конфигурацию логирования
logging.basicConfig(
    level=logging.INFO,  # Минимальный уровень для записи (INFO, WARNING, ERROR)
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, encoding="utf-8"), # Запись в файл
        logging.StreamHandler()                               # Вывод в консоль VS Code
    ]
)

# Создаем именной логгер для нашего приложения
logger = logging.getLogger("FinTrackApp")