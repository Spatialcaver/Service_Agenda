from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
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

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser informado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('tipo_usuario', TypeUser.ADMINISTRADOR)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    full_name = models.CharField(max_length=100, blank=False, null=False)
    tipo_usuario = models.CharField(max_length=20, choices=TypeUser.CHOICES, default=TypeUser.CLIENTE)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f'{self.id},{self.email}, {self.full_name}'


class Funcionario(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey('estabelecimento.Estabelecimento', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id}, {self.user}, {self.estabelecimento}'