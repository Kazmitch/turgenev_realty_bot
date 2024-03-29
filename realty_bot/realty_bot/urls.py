"""realty_bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from realty_bot.realty import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/mailing', views.mailing_request),
    path('api/edit_mailing', views.edit_mailing),
    path('api/delete_mailing', views.delete_mailing)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Статика работает при выключенном DEBUG
if settings.DEBUG is False:
    urlpatterns += [#path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT, }),
        re_path('static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}), ]
