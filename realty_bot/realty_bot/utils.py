def user_directory_path(instance, filename):
    """Сохраняет файл по заданному пути."""
    return f'{instance.building.latin_name}/{instance.directory}/{filename}'
