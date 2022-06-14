def user_directory_path(instance, filename):
    """Сохраняет файл по заданному пути."""
    return f'realty_bot/media/{instance.building.latin_name}/{instance.directory}/{filename}'
