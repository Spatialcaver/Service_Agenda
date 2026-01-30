from django.urls import path
from .views import ReservaView, DisponibilidadeView

urlpatterns = [
    path('reserva/', ReservaView.as_view(), name='reserva'),
    path('disponibilidade/', DisponibilidadeView.as_view(), name='disponibilidade'),
]

