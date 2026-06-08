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
        logger.info(f'Novo usuário criado: {serializer.instance.email}')


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
        logger.info(f'Usuário atualizado: {serializer.instance.email}')

    def perform_destroy(self, instance):
        email = instance.email
        instance.delete()
        logger.warning(f'Usuário deletado: {email}')


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
            logger.warning(f'Tentativa de login com senha incorreta: {email or telefone}')
            return Response(
                {'detail': 'Credenciais inválidas.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken.for_user(user)
            serializer = UsuarioSerializer(user)
            logger.info(f'Login bem-sucedido: {email or telefone}')
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
                user = serializer.save()
                
                telefone = user.telefone
                if telefone:
                    import re, os
                    cleaned_tel = re.sub(r'\D', '', telefone)
                    if cleaned_tel:
                        if len(cleaned_tel) <= 11:
                            cleaned_tel = '55' + cleaned_tel
                        elif not cleaned_tel.startswith('55'):
                            cleaned_tel = '55' + cleaned_tel
                            
                        filepath = r'C:\Users\ricardo\Desktop\HydroTech-main\exemplo_whapi_alerta.js'
                        try:
                            if os.path.exists(filepath):
                                with open(filepath, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                if cleaned_tel not in content:
                                    if 'const CONTATOS = [\n' in content:
                                        content = content.replace('const CONTATOS = [\n', f"const CONTATOS = [\n  '{cleaned_tel}',\n")
                                    elif 'const CONTATOS = [\r\n' in content:
                                        content = content.replace('const CONTATOS = [\r\n', f"const CONTATOS = [\r\n  '{cleaned_tel}',\r\n")
                                    with open(filepath, 'w', encoding='utf-8') as f:
                                        f.write(content)
                        except Exception as ex:
                            logger.error(f'Erro ao atualizar whapi_alerta.js: {ex}')

                refresh = RefreshToken.for_user(user)
                response_data = UsuarioSerializer(user).data
                logger.info(f'Novo usuário registrado: {user.email}')
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

