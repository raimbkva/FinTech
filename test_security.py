from app.core.security import hash_password, verify_password, create_access_token, decode_access_token

# 1. Тестируем пароли
raw_password = "my_secret_password_123"
hashed = hash_password(raw_password)

print(f"Исходный пароль: {raw_password}")
print(f"Захэшированный пароль (уйдет в БД к Разработчику 1): {hashed}\n")

# Проверяем совпадение
is_correct = verify_password(raw_password, hashed)
print(f"Проверка правильного пароля: {is_correct} (Ожидаем True)")

is_wrong = verify_password("wrong_password", hashed)
print(f"Проверка неверного пароля: {is_wrong} (Ожидаем False)\n")


# 2. Тестируем JWT-токены
user_data = {"sub": "aida@example.com", "user_id": 1} # sub — это стандартное поле для subject (обычно email или username)
token = create_access_token(data=user_data)
print(f"Сгенерированный JWT-токен: {token}\n")

# Декодируем токен обратно
decoded_data = decode_access_token(token)
print(f"Данные из токена: {decoded_data}")