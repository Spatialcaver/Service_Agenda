from rest_framework import serializers
from .models import Reserva
from user.models import User
from estabelecimento.models import Estabelecimento, Servicos
from reserva.models import Reserva

class ReservaSerializer(serializers.ModelSerializer):
    cliente = serializers.CharField(source='User.full_name', read_only=True)
    estabelecimento = serializers.CharField(source='Estabelecimento.nome', read_only=True)
    funcionario = serializers.CharField(source='Funcionario.user.full_name', read_only=True)
    servico = serializers.CharField(source='Servicos.servico', read_only=True)

    class Meta:
        model = Reserva
        fields = ['data', 'hora', 'cliente', 'telefone', 'servico', 'estabelecimento', 'funcionario']
        read_only_fields = ['id']
        required_fields = ['data', 'hora', 'cliente', 'telefone', 'servico', 'estabelecimento', 'funcionario']
    
    def validate(self, attrs):
        if attrs['data'] < datetime.date.today():
            raise serializers.ValidationError("A data deve ser maior ou igual a hoje.")
        return attrs