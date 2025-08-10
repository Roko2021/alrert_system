from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlertViewSet, TriggeredAlertViewSet, register_user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"alerts", AlertViewSet, basename="alert")
router.register(r"triggered-alerts", TriggeredAlertViewSet, basename="triggeredalert")

urlpatterns = [
    path("register/", register_user, name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
