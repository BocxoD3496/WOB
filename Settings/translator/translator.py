from dataclasses import dataclass

@dataclass
class en:
    @dataclass
    class messages:
        nickname_length_error = "Nickname must be between 4 and 24 characters."
        nickname_exists_error = "Nickname already exists."
        registration_success = "Registration successful."
        authentication_success = "Authentication successful."
        authentication_failed = "Authentication failed. Incorrect nickname or password."
        method_id_mismatch = "Authentication failed. Method or Messenger UserID mismatch."

@dataclass
class ru:
    @dataclass
    class messages:
        nickname_length_error = "Никнейм должен быть от 4 до 24 символов."
        nickname_exists_error = "Никнейм уже существует."
        registration_success = "Регистрация прошла успешно."
        authentication_success = "Авторизация прошла успешно."
        authentication_failed = "Авторизация не удалась. Неверный никнейм или пароль."
        method_id_mismatch = "Авторизация не удалась. Несоответствие метода или ID пользователя мессенджера."

def translate(lang, command, phrase):
    """
    Пример:
    translate('en', 'messages', 'nickname_length_error') -> 'Nickname must be between 4 and 24 characters.'
    """
    try:
        return eval(f"{lang}.{command}.{phrase}")
    except:
        return (f"Translation not found [{lang}.{command}.{phrase}]")
