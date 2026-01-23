from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid

class User(AbstractBaseUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30, blank=False, null=False)
    full_name = models.CharField(max_length=100, blank=False, null=False)
    estabelecimento = models.ForeignKey('estabelecimento.Estabelecimento', on_delete=models.CASCADE)
    
    
    
    def __str__(self):
        return f'{self.id},{self.email}, {self.full_name}, {self.estabelecimento}'