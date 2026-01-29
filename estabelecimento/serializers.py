from rest_framework import serializers
from .models import Estabelecimento, Servicos
from user.models import User

class EstabelecimentoSerializer(serializers.ModelSerializer):
    proprietario = serializers.CharField(source='User.full_name', read_only=True)
    
    class Meta:
        model = Estabelecimento
        fields = '__all__'
        read_only_fields = ['id']
        required_fields = ['nome', 'proprietario', 'endereco', 'horario_abertura', 'horario_fechamento', 'dia_funcionamento']

    def validate(self, attrs):
        if attrs['horario_abertura'] >= attrs['horario_fechamento']:
            raise serializers.ValidationError("O horário de fechamento deve ser maior que o horário de abertura.")
        return attrs

    def get_proprietario(self, obj):
        return obj.proprietario.full_name


class ServicosSerializer(serializers.ModelSerializer):
    responsavel = serializers.CharField(source='User.full_name', read_only=True)
    estabelecimento = serializers.CharField(source='Estabelecimento.nome', read_only=True)
    class Meta:
        model = Servicos
        fields = '__all__'
        read_only_fields = ['id']

    def validate(self, attrs):
        if attrs['duracao'] <= 0:
            raise serializers.ValidationError("A duração deve ser maior que 0.")
        return attrs

    def get_estabelecimento(self, obj):
        return obj.estabelecimento.nome