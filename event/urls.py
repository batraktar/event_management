from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from event.views import EventViewSet, UserRegistrationView, EventRegistrationView,\
    UserRegisteredEventsView, EventDetailView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import path, include

# Створюємо роутер
router = DefaultRouter()
router.register(r'events', EventViewSet)

# Налаштовуємо Swagger UI
schema_view = get_schema_view(
    openapi.Info(
        title="Event Management API",
        default_version='v1',
        description="API for managing events",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@eventmanagement.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.as_view(), name='swagger-docs'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('events/<int:event_id>/register/', EventRegistrationView.as_view(), name='event_register'),
    path('user/events/', UserRegisteredEventsView.as_view(), name='user_registered_events'),
    # path('events/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
]
