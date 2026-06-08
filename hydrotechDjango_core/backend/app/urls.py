from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from usuarios.views import (
    UsuarioCreatedListView,
    UsuarioRetriveUpdateDestroyView,
    AuthLoginView,
    AuthRegisterView,
    UsuarioMeView,
)
from rios.views import (
    RiosListCreateView, 
    RiosRetrieveUpdateDestroyView, 
    PontoRiscoFavoriteView,
    PontoRiscoAlertView,
    PontoRiscoListCreateView,
    PontoRiscoRetrieveUpdateDestroyView,
    RiosPublicoListView,
    PontoRiscoPublicoListView,
    RiosGeminiDescriptionView,
    HealthCheckView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', UsuarioCreatedListView.as_view(), name='usuario-list-create'),
    path('usuarios/<int:pk>/', UsuarioRetriveUpdateDestroyView.as_view(), name='usuario-detail-view'),
    path('auth/login/', AuthLoginView.as_view(), name='auth-login'),
    path('auth/register/', AuthRegisterView.as_view(), name='auth-register'),
    path('auth/me/', UsuarioMeView.as_view(), name='auth-me'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth-refresh'),

    path('rios/', RiosListCreateView.as_view(), name='rios-list-create'),
    path('rios/<int:pk>/', RiosRetrieveUpdateDestroyView.as_view(), name='rios-detail-view'),
    path('rios/<int:pk>/descricao-gemini/', RiosGeminiDescriptionView.as_view(), name='rios-gemini-description'),
    path('pontos-risco/<int:pk>/favorite/', PontoRiscoFavoriteView.as_view(), name='pontos-risco-favorite'),
    path('pontos-risco/<int:pk>/alert/', PontoRiscoAlertView.as_view(), name='pontos-risco-alert'),
    
    path('rios/<int:rio_id>/pontos-risco/', PontoRiscoListCreateView.as_view(), name='ponto-risco-list-create'),
    path('pontos-risco/<int:pk>/', PontoRiscoRetrieveUpdateDestroyView.as_view(), name='ponto-risco-detail'),

    # Public Endpoints
    path('publico/rios/', RiosPublicoListView.as_view(), name='rios-publico-list'),
    path('publico/rios/<int:rio_id>/pontos-risco/', PontoRiscoPublicoListView.as_view(), name='ponto-risco-publico-list'),
    path('publico/rios/<int:pk>/descricao-gemini/', RiosGeminiDescriptionView.as_view(), name='rios-gemini-description-publico'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]

