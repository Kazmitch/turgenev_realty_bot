from realty_bot.realty.models import News


async def make_news_text(news: News) -> str:
    """Делаем текст для новости."""
    if news.telegraph_url is not None:
        text = f'<b>{news.title}</b>\n\n{news.text}\n\n{news.telegraph_url}'
    else:
        text = f'<b>{news.title}</b>\n\n{news.text}'
    return text
