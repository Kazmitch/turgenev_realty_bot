from functools import wraps

from django.http import JsonResponse

from realty_bot.realty_bot.mailing import broadcaster


def async_csrf_exempt(view_func):
    async def wrapped_view(*args, **kwargs):
        return await view_func(*args, **kwargs)

    wrapped_view.csrf_exempt = True
    return wraps(view_func)(wrapped_view)


@async_csrf_exempt
async def mailing_request(request):
    """Получаем данные для рассылки."""
    if request.method == 'POST':
        users = request.POST.get('user_ids_list')
        text = request.POST.get('mailing_text')
        mailing_image = request.POST.get('mailing_image')
        users_list = [int(x) for x in users.split(',')]
        await broadcaster(users_list, text, mailing_image)
    return JsonResponse({'status': '200', 'text': 'Рассылка создана'})
