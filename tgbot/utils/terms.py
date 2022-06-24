from tgbot.utils.dp_api.db_commands import get_terms


async def make_term_text(building_name: str, term: str) -> str:
    """Формируем текст для вывода условий."""
    terms = await get_terms(building_name, term)

    terms_list = []

    for term in terms:
        title = term.title
        description = term.description

        terms_list.append(f'<b>{title}</b>\n{description}')

    text = '\n\n\n'.join(terms_list)
    return text
