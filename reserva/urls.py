from django.urls import path
from .views import ReservaView, DisponibilidadeView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reserva', ReservaView)

urlpatterns = [
    path('', include(router.urls)),
    path('disponibilidade/', DisponibilidadeView.as_view(), name='disponibilidade'),
]

