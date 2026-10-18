from .models import Rios, PontoRisco
from rest_framework import serializers


class RiosSerializer(serializers.ModelSerializer):
    criado_por = serializers.PrimaryKeyRelatedField(read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.nome', read_only=True)

    class Meta:
        model = Rios
        fields = ['id', 'nome', 'cidade', 'estado', 'criado_por', 'criado_por_nome']
        read_only_fields = ['criado_por', 'criado_por_nome']

    def validate_nome(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError('Nome do rio deve ter no mínimo 3 caracteres.')
        return value.strip()

    def validate_cidade(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError('Cidade deve ser informada.')
        return value.strip()

    def validate_estado(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError('Estado deve ser informado.')
        return value.strip()






class PontoRiscoSerializer(serializers.ModelSerializer):
    favorito = serializers.SerializerMethodField()
    criado_por_nome = serializers.CharField(source='criado_por.nome', read_only=True)
    rio_nome = serializers.CharField(source='rio.nome', read_only=True)
    
    class Meta:
        model = PontoRisco
        fields = ['id', 'rio', 'rio_nome', 'latitude', 'longitude', 'descricao', 'nivel_base', 'limite_atencao', 'limite_alerta', 'limite_emergencia', 'favorito', 'criado_por', 'criado_por_nome', 'criado_em', 'atualizado_em']
        read_only_fields = ['criado_por', 'criado_por_nome', 'criado_em', 'atualizado_em']

    def get_favorito(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and getattr(user, 'is_authenticated', False):
            return user.favoritos.filter(pk=obj.pk).exists()
        return False

    def validate_latitude(self, value):
        if not (-90 <= value <= 90):
            raise serializers.ValidationError('Latitude deve estar entre -90 e 90.')
        return value

    def validate_longitude(self, value):
        if not (-180 <= value <= 180):
            raise serializers.ValidationError('Longitude deve estar entre -180 e 180.')
        return value

    def validate_descricao(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('A descrição (nome do ponto) não pode ficar em branco.')
        return value.strip()



    def validate_nivel_base(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError('Nível base deve ser um valor positivo.')
        return value

    def validate(self, data):
        atencao = data.get('limite_atencao', 1.5)
        alerta = data.get('limite_alerta', 2.5)
        emergencia = data.get('limite_emergencia', 3.5)
        if not (atencao < alerta < emergencia):
            raise serializers.ValidationError('Os limites devem seguir a ordem: Atenção < Alerta < Emergência.')
        return data

