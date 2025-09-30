from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CategoryViewSet, TaskViewSet
from . import views

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"tasks", TaskViewSet, basename="tasks")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/auth/register/", views.register_user, name="auth-register"),
    path("api/auth/login/", views.login_user, name="auth-login"),
    path("api/auth/logout/", views.logout_user, name="auth-logout"),
]
