from django.urls import path
from .views import (
    SensorListCreateView,
    SensorRetrieveUpdateDestroyView,
    SensorGroupListCreateView,
    SensorGroupRetrieveUpdateDestroyView,
    LeituraListCreateView,
    LeituraRetrieveDestroyView,
)


urlpatterns = [
    path('', SensorListCreateView.as_view(), name='sensor-list-create'),
    path('<int:pk>/', SensorRetrieveUpdateDestroyView.as_view(), name='sensor-detail'),
    path(
        '<int:sensor_id>/leituras/',
        LeituraListCreateView.as_view(),
        name='leitura-list-create',
    ),
    path('leituras/<int:pk>/', LeituraRetrieveDestroyView.as_view(), name='leitura-detail'),

    path('grupos/', SensorGroupListCreateView.as_view(), name='grupo-list-create'),
    path('grupos/<int:pk>/', SensorGroupRetrieveUpdateDestroyView.as_view(), name='grupo-detail'),
]