from rest_framework import serializers
from .models import Sensor, SensorGroup, Leitura


class LeituraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leitura
        fields = ['id', 'sensor', 'valor', 'criado_em']
        read_only_fields = ['sensor', 'criado_em']


class SensorSerializer(serializers.ModelSerializer):
    grupo_nome = serializers.CharField(source='grupo.nome', read_only=True)
    rio_nome = serializers.CharField(source='rio.nome', read_only=True)
    ultimo_valor = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        fields = [
            'id', 'nome', 'tipo', 'unidade', 'status', 'modelo',
            'latitude', 'longitude', 'rio', 'rio_nome',
            'grupo', 'grupo_nome',
            'ultimo_valor', 'criado_em', 'atualizado_em',
        ]
        read_only_fields = ['criado_em', 'atualizado_em']

    def validate_nome(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError(
                'Nome do sensor deve ter no mínimo 3 caracteres.'
            )
        return value.strip()

    def get_ultimo_valor(self, obj):
        return obj.get_ultimo_valor()


class SensorGroupSerializer(serializers.ModelSerializer):
    sensores = SensorSerializer(many=True, read_only=True)
    subgrupos = serializers.SerializerMethodField()
    total_sensores = serializers.SerializerMethodField()

    class Meta:
        model = SensorGroup
        fields = [
            'id', 'nome', 'descricao', 'endereco',
            'latitude', 'longitude', 'rio', 'parent',
            'sensores', 'subgrupos', 'total_sensores',
            'criado_em', 'atualizado_em',
        ]
        read_only_fields = ['criado_em', 'atualizado_em']

    def validate_nome(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError(
                'Nome do grupo deve ter no mínimo 3 caracteres.'
            )
        return value.strip()

    def get_subgrupos(self, obj):
        return SensorGroupSerializer(
            obj.subgrupos.all(), many=True, context=self.context
        ).data

    def get_total_sensores(self, obj):
        return obj.get_total_sensores()