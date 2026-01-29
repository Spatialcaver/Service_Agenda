from rest_framework import serializers
from .models import User, Funcionario

class UserSerializer(serializers.ModelSerializer):
    funcionario = serializers.SlugRelatedField('full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'funcionario', 'full_name', 'tipo_usuario', 'estabelecimento']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['id', 'user', 'estabelecimento']
        read_only_fields = ['id']