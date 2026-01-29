from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FuncionarioViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'funcionarios', FuncionarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
