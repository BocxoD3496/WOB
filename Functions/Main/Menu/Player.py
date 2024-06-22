import psycopg2
from datetime import datetime
import hashlib
from translator import translate

# Подключение к базе данных
def get_db_connection():
    return psycopg2.connect(
        dbname="mydatabase",
        user="myuser",
        password="mypassword",
        host="localhost"
    )

# Функция для хеширования паролей
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Функция для регистрации пользователя
def register_user(nickname, password, method, bot_user_id, vk_id=None, tg_id=None, lang='ru'):
    if len(nickname) < 4 or len(nickname) > 24:
        return translate(lang, 'messages', 'nickname_length_error')
    
    hashed_password = hash_password(password)
    registration_datetime = datetime.now()

    conn = get_db_connection()
    cur = conn.cursor()

    # Проверка существования никнейма
    cur.execute("SELECT nickname FROM users WHERE nickname = %s", (nickname,))
    if cur.fetchone() is not None:
        cur.close()
        conn.close()
        return translate(lang, 'messages', 'nickname_exists_error')

    # Добавление новой записи в таблицу
    cur.execute(
        "INSERT INTO users (nickname, password, method, bot_user_id, registration_datetime, vk_id, tg_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (nickname, hashed_password, method, bot_user_id, registration_datetime, vk_id, tg_id)
    )
    conn.commit()
    cur.close()
    conn.close()

    log_message = f"Пользователь зарегистрирован: Никнейм: {nickname}, Метод: {method}, VK ID: {vk_id}, TG ID: {tg_id}, Время: {registration_datetime}"
    log_to_channel(log_message)
    return translate(lang, 'messages', 'registration_success')

# Функция для логирования в канал надо спереть с основного бота
def log_to_channel(message):
    print(message)  

# Функция для авторизации пользователя
def authenticate_user(nickname, password, method, messenger_user_id, lang='ru'):
    hashed_password = hash_password(password)
    
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT nickname, password, method, vk_id, tg_id FROM users WHERE nickname = %s AND password = %s", (nickname, hashed_password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        if (method == 'vk' and user[3] == messenger_user_id) or (method == 'tg' and user[4] == messenger_user_id):
            return translate(lang, 'messages', 'authentication_success')
        else:
            log_message = (f"Попытка авторизации с другого профиля/мессенджера: "
                           f"Никнейм: {nickname}, Предыдущий метод: {user[2]}, Текущий метод: {method}, "
                           f"Предыдущий VK ID: {user[3]}, Текущий Messenger UserID: {messenger_user_id}")
            log_to_channel(log_message)
            return translate(lang, 'messages', 'method_id_mismatch')
    
    return translate(lang, 'messages', 'authentication_failed')
