from django.contrib import admin
from django.urls import path, include

# Основний файл маршрутів
urlpatterns = [
    path('admin/', admin.site.urls),  # Адміністративний інтерфейс
    path('api/', include('event.urls')),  # Включає маршрути з файлу events/urls.py
]
