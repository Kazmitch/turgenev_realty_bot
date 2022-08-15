import base64
import urllib.parse


def user_directory_path(instance, filename):
    """Сохраняет файл по заданному пути."""
    return f'{instance.building.latin_name}/{instance.directory}/{filename}'


def about_project_path(instance, filename):
    """Сохраняет фото О Проекте по заданному пути"""
    return f'{instance.developer.latin_name}/{instance.directory}/{filename}'


def encode_decode_values(value: str):
    """Кодируем и декодируем значение."""
    try:
        return urllib.parse.quote(base64.b64encode(value.encode('UTF-8')).decode('UTF-8'))
    except AttributeError:
        return None


def correct_phone(phone: str):
    """Возвращаем телефон в нужном формате."""
    phone_number = ''.join(n for n in phone if n.isdigit())
    if phone_number[0] == '8':
        phone_number = f'7{phone_number[1:]}'
    if len(phone_number) == 10 and phone_number[0] != '7':
        phone_number = f'7{phone_number}'
    if len(phone_number) != 11:
        return None
    return phone_number
