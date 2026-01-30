from rest_framework import serializers
from .models import Reserva
from user.models import User
from estabelecimento.models import Estabelecimento, Servicos
from datetime import datetime
from reserva.models import Reserva

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'

    def validate(self, data):
        funcionario = data['funcionario']
        data_res = data['data']
        hora_res = data['hora']
        servico = data['servico']

        # Cálculo do intervalo pretendido
        inicio_pretendido = datetime.combine(data_res, hora_res)
        fim_pretendido = inicio_pretendido + servico.duracao
        hora_fim_pretendida = fim_pretendido.time()

        # Verifica se o funcionário já tem reserva que sobreponha este horário
        # Regra: (Inicio1 < Fim2) E (Fim1 > Inicio2)
        reservas_existentes = Reserva.objects.filter(
            funcionario=funcionario,
            data=data_res
        )

        for reserva in reservas_existentes:
            res_inicio = reserva.hora
            res_fim = (datetime.combine(reserva.data, reserva.hora) + reserva.servico.duracao).time()

            if hora_res < res_fim and hora_fim_pretendida > res_inicio:
                raise serializers.ValidationError(
                    f"O funcionário {funcionario.nome} já possui um agendamento que conflita com este horário."
                )

        return data