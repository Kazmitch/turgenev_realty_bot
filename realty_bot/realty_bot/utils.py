import base64


def user_directory_path(instance, filename):
    """Сохраняет файл по заданному пути."""
    return f'{instance.building.latin_name}/{instance.directory}/{filename}'


def about_project_path(instance, filename):
    """Сохраняет фото О Проекте по заданному пути"""
    return f'{instance.developer.latin_name}/{instance.directory}/{filename}'


def encode_decode_values(value: str):
    """Кодируем и декодируем значение."""
    try:
        return base64.b64encode(value.encode('UTF-8')).decode('UTF-8')
    except AttributeError:
        return None
