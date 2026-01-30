from django.db import models
from estabelecimento.models import Estabelecimento, Servicos 
from user.models import Funcionario
from datetime import datetime, timedelta

class Reserva(models.Model):
    data = models.DateField()
    hora = models.TimeField()
    cliente = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    servico = models.ForeignKey(
        Servicos, 
        on_delete=models.CASCADE, 
        related_name='reservas_do_servico'
    )
    estabelecimento = models.ForeignKey(
        Estabelecimento, 
        on_delete=models.CASCADE, 
        related_name='reservas_do_estabelecimento'
    )
    funcionario = models.ForeignKey(
        Funcionario, 
        on_delete=models.CASCADE, 
        related_name='reservas_do_funcionario'
    )


    @property
    def hora_fim(self):
        inicio = datetime.combine(self.data, self.hora)
        fim = inicio + timedelta(minutes=self.servico.duracao)
        return fim.time()
    def __str__(self):
        return f'{self.id}, {self.data}, {self.hora}, {self.cliente}, {self.telefone}, {self.servico}, {self.estabelecimento}, {self.funcionario}'