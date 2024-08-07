from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


app_name = "products"
urlpatterns = [
    # token
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # views
    path("import/", views.ImportAPIView.as_view(), name="import"),
    path(
        "detail/<str:model_name>/", views.ModelListAPIView.as_view(), name="object_list"
    ),
    path(
        "detail/<str:model_name>/<int:pk>/",
        views.ModelDetailAPIView.as_view(),
        name="object_detail",
    ),
]
