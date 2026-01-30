
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'reserva', ReservaView)
router.register(r'disponibilidade', DisponibilidadeView)

urlpatterns = [
    path('api/', include(router.urls)),
]
