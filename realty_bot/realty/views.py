from functools import wraps

from django.http import JsonResponse

from realty_bot.realty_bot.mailing import broadcaster, broadcaster_edit, broadcaster_delete


def async_csrf_exempt(view_func):
    async def wrapped_view(*args, **kwargs):
        return await view_func(*args, **kwargs)

    wrapped_view.csrf_exempt = True
    return wraps(view_func)(wrapped_view)


@async_csrf_exempt
async def mailing_request(request):
    """Принимаем данные для рассылки."""
    if request.method == 'POST':
        users = request.POST.get('user_ids_list')
        text = request.POST.get('mailing_text')
        mailing_image = request.POST.get('mailing_image')
        mailing_video = request.POST.get('mailing_video')
        mailing_id = request.POST.get('mailing_id')
        users_list = [int(x) for x in users.split(',')]
        await broadcaster(users_list, text, mailing_image, mailing_video, mailing_id)
    return JsonResponse({'status': '200', 'text': 'Рассылка создана'})


@async_csrf_exempt
async def edit_mailing(request):
    """Принимаем данные для редактирования рассылки."""
    if request.method == 'POST':
        mailing_id = request.POST.get('mailing_id')
        text = request.POST.get('mailing_text')
        mailing_image = request.POST.get('mailing_image')
        mailing_video = request.POST.get('mailing_video')
        await broadcaster_edit(mailing_id, text, mailing_image, mailing_video)
    return JsonResponse({'status': '200', 'text': 'Рассылка отредактирована'})


@async_csrf_exempt
async def delete_mailing(request):
    """Принимаем данные для удаления рассылки."""
    if request.method == 'POST':
        mailing_id = request.POST.get('mailing_id')
        await broadcaster_delete(mailing_id)
    return JsonResponse({'status': '200', 'text': 'Рассылка удалена'})
