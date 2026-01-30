from django.urls import path
from .views import ReservaView, DisponibilidadeView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reserva', ReservaView)
router.register(r'disponibilidade', DisponibilidadeView)

urlpatterns = [
    path('', include(router.urls)),
]

