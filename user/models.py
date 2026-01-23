from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid


class TypeUser:
    CLIENTE = 'Cliente'
    FUNCIONARIO = 'Funcionário'
    ADMINISTRADOR = 'Administrador'

    CHOICES = [
        (CLIENTE, 'Cliente'),
        (FUNCIONARIO, 'Funcionário'),
        (ADMINISTRADOR, 'Administrador')
    ]


class User(AbstractBaseUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30, blank=False, null=False)
    full_name = models.CharField(max_length=100, blank=False, null=False)
    tipo_usuario = models.CharField(max_length=20, choices=TypeUser.CHOICES, default=TypeUser.CLIENTE)
    estabelecimento = models.ForeignKey('estabelecimento.Estabelecimento', on_delete=models.CASCADE, related_name='equipe_funcionarios')
    
    
    
    def __str__(self):
        return f'{self.id},{self.email}, {self.full_name}, {self.estabelecimento}'
    


class Funcionario(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey('estabelecimento.Estabelecimento', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id}, {self.user}, {self.estabelecimento}'