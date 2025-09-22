"""
URL configuration for traffic_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from roads.views import RoadSegmentViewSet, SpeedReadingViewSet
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from roads.views import BulkPassageView, PassageByCarView

router = DefaultRouter()
router.register(r"segments", RoadSegmentViewSet)
router.register(r"readings", SpeedReadingViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),

    # API Schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    # Swagger UI
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # Redoc UI (opcional)
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    path("api/", include(router.urls)),

    path("passages/bulk/", BulkPassageView.as_view(), name="bulk_passages"),

    path("passages/by-car/", PassageByCarView.as_view(), name="passages_by_car"),
]
