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
    proprietario = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='estabelecimentos_gerenciados')
    endereco = models.CharField(max_length=200)
    horario_abertura= models.TimeField(null=False, blank=False)
    horario_fechamento = models.TimeField(null=False, blank=False)
    dia_funcionamento = models.CharField(max_length=30, blank=False)
    
    
    
    
    def __str__(self):
        return f'{self.id},{self.nome}, '
    


class Servicos(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    servico = models.CharField(max_length=50, choices=ServicosChoices.CHOICES)
    responsavel = models.ForeignKey('user.User', on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey('estabelecimento.Estabelecimento', on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    duracao = models.DurationField(blank=False, null=False, default=None)
    
    def __str__(self):
        return f'{self.id},{self.nome}, {self.estabelecimento}'