
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from reserva.views import ReservaView, DisponibilidadeView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', include('user.urls')),
    
    # Rotas manuais para as APIViews de reserva
    path('api/reserva/', ReservaView.as_view(), name='reserva'),
    path('api/disponibilidade/', DisponibilidadeView.as_view(), name='disponibilidade'),
]