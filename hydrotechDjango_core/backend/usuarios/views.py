import logging
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario
from .serializers import UsuarioSerializer
from .permissions import IsOwnerOrSelf, IsAdminOnly, IsDefesaCivilOrAdmin
from .authentication import JWTOrAPITokenAuthentication

logger = logging.getLogger(__name__)


class UsuarioCreatedListView(generics.ListCreateAPIView):
    serializer_class = UsuarioSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        if self.request.method == 'POST':
            return [IsDefesaCivilOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_authenticated', False):
            if getattr(user, 'is_staff', False) or getattr(user, 'is_defesa_civil', False):
                return Usuario.objects.all()
            return Usuario.objects.filter(id=user.id)
        return Usuario.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not getattr(user, 'is_staff', False) and not getattr(user, 'is_defesa_civil', False):
            serializer.validated_data.pop('is_defesa_civil', None)
        serializer.save()
        logger.info('Novo usuário criado: %s', serializer.instance.id)


class UsuarioRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UsuarioSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            # Permite que o próprio usuário se edite/delete, ou que um Admin/Defesa Civil o faça
            return [IsAuthenticated()] # A verificação real é feita no get_queryset, onde filtramos. Mas podemos usar permissão tbm se preferir.
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_authenticated', False):
            if getattr(user, 'is_staff', False) or getattr(user, 'is_defesa_civil', False):
                return Usuario.objects.all()
            return Usuario.objects.filter(id=user.id)
        return Usuario.objects.none()

    def perform_update(self, serializer):
        user = self.request.user
        if not getattr(user, 'is_staff', False) and not getattr(user, 'is_defesa_civil', False):
            serializer.validated_data.pop('is_defesa_civil', None)
        serializer.save()
        logger.info('Usuário atualizado: %s', serializer.instance.id)

    def perform_destroy(self, instance):
        user_id = instance.id
        instance.delete()
        logger.warning('Usuário deletado: %s', user_id)


class UsuarioMeView(APIView):
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            serializer = UsuarioSerializer(request.user)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f'Erro ao buscar usuário logado: {str(e)}')
            return Response(
                {'detail': 'Erro ao buscar informações do usuário.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request):
        try:
            serializer = UsuarioSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.validated_data.pop('is_defesa_civil', None)
                serializer.save()
                if request.data.get('senha'):
                    request.user.deve_alterar_senha = False
                    request.user.save(update_fields=['deve_alterar_senha'])
                logger.info(f'Perfil atualizado via /auth/me/: {request.user.id}')
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Erro ao atualizar perfil: {str(e)}')
            return Response(
                {'detail': 'Erro ao atualizar perfil.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AuthLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').lower().strip() if request.data.get('email') else ''
        telefone = request.data.get('telefone', '').strip() if request.data.get('telefone') else ''
        senha = request.data.get('senha', '')

        if (not email and not telefone) or not senha:
            logger.warning(f'Tentativa de login sem credenciais')
            return Response(
                {'detail': 'E-mail/telefone e senha são obrigatórios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if email:
                user = Usuario.objects.get(email=email)
            else:
                import re
                cleaned = re.sub(r'\D', '', telefone)
                user = Usuario.objects.get(telefone=cleaned)
        except Usuario.DoesNotExist:
            logger.warning(f'Tentativa de login com credenciais inválidas')
            return Response(
                {'detail': 'Credenciais inválidas.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(senha):
            logger.warning('Tentativa de login com senha incorreta')
            return Response(
                {'detail': 'Credenciais inválidas.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken.for_user(user)
            serializer = UsuarioSerializer(user)
            logger.info('Login bem-sucedido: usuário %s', user.id)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'usuario': serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Erro ao gerar tokens: {str(e)}')
            return Response(
                {'detail': 'Erro ao processar login.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AuthRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UsuarioSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data.pop('is_defesa_civil', None)
                user = serializer.save()
                
                refresh = RefreshToken.for_user(user)
                response_data = UsuarioSerializer(user).data
                logger.info('Novo usuário registrado: %s', user.id)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'usuario': response_data,
                }, status=status.HTTP_201_CREATED)
            
            logger.warning(f'Erro no registro: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Erro inesperado no registro: {str(e)}')
            return Response(
                {'detail': 'Erro ao registrar usuário.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

