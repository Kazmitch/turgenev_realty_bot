def user_directory_path(instance, filename):
    """Сохраняет файл по заданному пути."""
    return f'{instance.building.latin_name}/{instance.directory}/{filename}'


def about_project_path(instance, filename):
    """Сохраняет фото О Проекте по заданному пути"""
    return f'{instance.developer.latin_name}/{instance.directory}/{filename}'
