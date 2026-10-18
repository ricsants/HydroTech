import logging
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Sensor, SensorGroup, Leitura
from .serializers import (
    SensorSerializer,
    SensorGroupSerializer,
    LeituraSerializer,
)
from usuarios.authentication import JWTOrAPITokenAuthentication
from usuarios.permissions import IsDefesaCivilOrAdmin

logger = logging.getLogger(__name__)


class SensoresPermission(IsDefesaCivilOrAdmin):
    """
    Leitura para qualquer usuário autenticado;
    escrita (criar/editar/deletar) apenas para Defesa Civil + Admin.
    """

    def has_permission(self, request, view):
        if not getattr(request.user, 'is_authenticated', False):
            return False
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return super().has_permission(request, view)
        return True


# ---------------------------------------------------------------------------
# Sensores (folhas do Composite)
# ---------------------------------------------------------------------------

class SensorListCreateView(generics.ListCreateAPIView):
    serializer_class = SensorSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [SensoresPermission]

    def get_queryset(self):
        return Sensor.objects.select_related('grupo', 'rio').order_by('-id')

    def perform_create(self, serializer):
        serializer.save()
        logger.info(
            f'Sensor criado: {serializer.instance.nome} '
            f'(tipo={serializer.instance.tipo})'
        )


class SensorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SensorSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [SensoresPermission]

    def get_queryset(self):
        return Sensor.objects.select_related('grupo', 'rio')

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Sensor atualizado: {serializer.instance.nome}')

    def perform_destroy(self, instance):
        nome = instance.nome
        instance.delete()
        logger.info(f'Sensor deletado: {nome}')


# ---------------------------------------------------------------------------
# Grupos de sensores (composites do padrão Composite)
# ---------------------------------------------------------------------------

class SensorGroupListCreateView(generics.ListCreateAPIView):
    serializer_class = SensorGroupSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [SensoresPermission]

    def get_queryset(self):
        return SensorGroup.objects.prefetch_related(
            'sensores', 'subgrupos'
        ).order_by('-id')

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f'Grupo de sensores criado: {serializer.instance.nome}')


class SensorGroupRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SensorGroupSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [SensoresPermission]

    def get_queryset(self):
        return SensorGroup.objects.prefetch_related(
            'sensores', 'subgrupos'
        )

    def perform_update(self, serializer):
        parent = serializer.validated_data.get('parent')
        if parent and parent == serializer.instance:
            raise serializers.ValidationError(
                {'parent': 'Um grupo não pode ser pai de si mesmo.'}
            )
        serializer.save()
        logger.info(f'Grupo de sensores atualizado: {serializer.instance.nome}')

    def perform_destroy(self, instance):
        nome = instance.nome
        instance.delete()
        logger.info(f'Grupo de sensores deletado: {nome}')


# ---------------------------------------------------------------------------
# Leitura (medição de um sensor folha)
# ---------------------------------------------------------------------------

class LeituraListCreateView(generics.ListCreateAPIView):
    serializer_class = LeituraSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sensor_id = self.kwargs.get('sensor_id')
        return Leitura.objects.filter(sensor_id=sensor_id)

    def perform_create(self, serializer):
        sensor_id = self.kwargs.get('sensor_id')
        serializer.save(sensor_id=sensor_id)
        logger.info(f'Leitura registrada para o sensor {sensor_id}')


class LeituraRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = LeituraSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [SensoresPermission]

    def get_queryset(self):
        return Leitura.objects.all()