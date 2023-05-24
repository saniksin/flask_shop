from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from src.apps.api import views


schema_view = get_schema_view(
    openapi.Info(
        title="FlaskShop API",
        default_version='v1',
        description="FlaskShop",
        contact=openapi.Contact(email="rbkrutoi@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)


router = DefaultRouter()
router.register("user", views.UserGetViewSet, basename="user")


urlpatterns = [
    path('docs/', schema_view.with_ui("swagger")),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


urlpatterns += router.urls