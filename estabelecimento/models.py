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
    

class Funcionamento (models.Model):
    CHOICES = [
    ('SEG', 'Segunda-feira'),
    ('TER', 'Terça-feira'),
    ('QUA', 'Quarta-feira'),
    ('QUI', 'Quinta-feira'),
    ('SEX', 'Sexta-feira'),
    ('SAB', 'Sábado'),
    ('DOM', 'Domingo')
    ]
    dia = models.CharField(max_length=3, choices=CHOICES, unique=True)
    horario_abertura = models.TimeField(null=True, blank=True)
    horario_fechamento = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.get_dia_display()

class Estabelecimento (models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    nome = models.CharField(max_length=50)
    proprietario = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='estabelecimentos_gerenciados')
    endereco = models.CharField(max_length=200)
    dia_funcionamento = models.ManyToManyField(to=Funcionamento, related_name='HorariosFuncionamento')
    servicos_oferecidos = models.ManyToManyField(to='Servicos', related_name='EstabelecimentosOferecem')
    
    def __str__(self):
        return f'{self.id},{self.nome}, {self.proprietario}'
    


class Servicos(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    servico = models.CharField(max_length=50, choices=ServicosChoices.CHOICES)
    responsavel = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=True, null=True, related_name='servicos_responsavel')
    estabelecimento = models.ForeignKey('estabelecimento.Estabelecimento', on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    duracao = models.DurationField(blank=False, null=False, default=None)
    
    def __str__(self):
        return f'{self.id},{self.servico}, {self.estabelecimento}'