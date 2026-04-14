from django.utils import timezone
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
        
        # Garante que o usuário seja criado como ativo por padrão
        extra_fields.setdefault('is_active', True)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Campos obrigatórios para o Django Admin
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('tipo_usuario', TypeUser.ADMINISTRADOR)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    full_name = models.CharField(max_length=100, blank=False, null=False)
    tipo_usuario = models.CharField(max_length=20, choices=TypeUser.CHOICES, default=TypeUser.CLIENTE)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id},{self.email}, {self.full_name}'


class Funcionario(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey('estabelecimento.Estabelecimento', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id}, {self.user}, {self.estabelecimento}'
    
    
    
class Pausas:
    ALMOCO = 'Almoço'
    FIM_EXPEDIENTE = 'Fim do Expediente'
    INDISPONIVEL = 'Indisponível'

    CHOICES = [
        (ALMOCO, 'Almoço'),
        (FIM_EXPEDIENTE, 'Fim do Expediente'),
        (INDISPONIVEL, 'Indisponível')
    ]
    
            
class AusenciaFuncionario(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField(default=timezone.now)
    hora_fim = models.TimeField(blank= True, null=True)
    motivo = models.CharField(max_length=50, choices=Pausas.CHOICES)

    def __str__(self):
        return f'{self.id}, {self.funcionario}, {self.data}, {self.hora_inicio}, {self.hora_fim}, {self.motivo}'