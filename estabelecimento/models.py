from django.db import models
import uuid 

class ServicosChoices:
    CABELO = 'Cabelo'
    BARBA = 'Barba'
    MANICURE = 'Manicure'
    PEDICURE = 'Pedicure'
    MAQUILAGEM = 'Maquiagem'
    
    CHOICES = [
        (CABELO, 'Cabelo'),
        (BARBA, 'Barba'),
        (MANICURE, 'Manicure'),
        (PEDICURE, 'Pedicure'),
        (MAQUILAGEM, 'Maquiagem')
    ]
    

class Estabelecimento (models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    nome = models.CharField(max_length=50)
    funcionario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    endereco = models.CharField(max_length=200)
    horario_funcionamento = models.DateTimeField(null=True, blank=True)
    dia_funcionamento = models.CharField(max_length=30, blank=True)
    servicos = models.CharField(max_length=200, null=True, blank=True, choices=ServicosChoices.CHOICES)
    
    
    
    def __str__(self):
        return f'{self.id},{self.nome}, '
    