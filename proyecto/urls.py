from django.contrib import admin
from django.urls import path, include
from django.conf import settings
urlpatterns = [
    path('', include("app.urls")),
]

if settings.DEBUG:
    urlpatterns.append(path('admin/', admin.site.urls))

handler404='app.views.custom_error_404'
handler500='app.views.custom_error_500'