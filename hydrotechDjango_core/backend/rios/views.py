import logging
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Rios, PontoRisco
from .serializers import RiosSerializer, PontoRiscoSerializer
from usuarios.authentication import JWTOrAPITokenAuthentication
from usuarios.permissions import IsDefesaCivilAdminOrOwner

logger = logging.getLogger(__name__)


class RiosListCreateView(generics.ListCreateAPIView):
    serializer_class = RiosSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_staff', False) or getattr(user, 'is_defesa_civil', False):
            return Rios.objects.all().order_by('-id')
        return Rios.objects.filter(criado_por=user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)
        logger.info(f'Novo rio criado: {serializer.instance.nome} por {self.request.user.email}')


class RiosRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RiosSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_staff', False) or getattr(user, 'is_defesa_civil', False):
            return Rios.objects.all()
        return Rios.objects.filter(criado_por=user)

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Rio atualizado: {serializer.instance.nome}')

    def perform_destroy(self, instance):
        nome = instance.nome
        instance.delete()
        logger.info(f'Rio deletado: {nome}')


class PontoRiscoFavoriteView(APIView):
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            ponto = get_object_or_404(PontoRisco, pk=pk)
            
            if request.user.favoritos.filter(pk=ponto.pk).exists():
                request.user.favoritos.remove(ponto)
                favorito = False
                logger.info(f'Ponto de risco removido de favoritos: {ponto.descricao} por {request.user.email}')
            else:
                request.user.favoritos.add(ponto)
                favorito = True
                logger.info(f'Ponto de risco adicionado a favoritos: {ponto.descricao} por {request.user.email}')
            
            return Response({'favorito': favorito})
        except Exception as e:
            logger.error(f'Erro ao atualizar favorito: {str(e)}')
            return Response(
                {'detail': 'Erro ao atualizar favorito.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PontoRiscoAlertView(APIView):
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            ponto = get_object_or_404(PontoRisco, pk=pk)
            
            if request.user.alertas.filter(pk=ponto.pk).exists():
                request.user.alertas.remove(ponto)
                alerta = False
                logger.info(f'Ponto de risco removido de alertas: {ponto.descricao} por {request.user.email}')
            else:
                request.user.alertas.add(ponto)
                alerta = True
                logger.info(f'Ponto de risco adicionado a alertas: {ponto.descricao} por {request.user.email}')
            
            return Response({'alerta': alerta})
        except Exception as e:
            logger.error(f'Erro ao atualizar alerta: {str(e)}')
            return Response(
                {'detail': 'Erro ao atualizar alerta.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PontoRiscoListCreateView(generics.ListCreateAPIView):
    serializer_class = PontoRiscoSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsDefesaCivilAdminOrOwner]

    def get_queryset(self):
        rio_id = self.kwargs.get('rio_id')
        return PontoRisco.objects.filter(rio_id=rio_id).order_by('-criado_em')

    def perform_create(self, serializer):
        rio_id = self.kwargs.get('rio_id')
        rio = get_object_or_404(Rios, pk=rio_id)
        serializer.save(criado_por=self.request.user, rio=rio)
        logger.info(f'Novo ponto de risco criado: {rio.nome} por {self.request.user.email}')


class PontoRiscoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PontoRiscoSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsDefesaCivilAdminOrOwner]

    def get_queryset(self):
        return PontoRisco.objects.all()

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Ponto de risco atualizado: {serializer.instance.rio.nome}')

    def perform_destroy(self, instance):
        rio_nome = instance.rio.nome
        instance.delete()
        logger.info(f'Ponto de risco deletado: {rio_nome}')

# Public Views
class RiosPublicoListView(generics.ListAPIView):
    serializer_class = RiosSerializer
    permission_classes = []  # No authentication required
    authentication_classes = []
    pagination_class = None  # Return all rios without pagination
    queryset = Rios.objects.all().order_by('-id')

class PontoRiscoPublicoListView(generics.ListAPIView):
    serializer_class = PontoRiscoSerializer
    permission_classes = []  # No authentication required
    authentication_classes = []
    pagination_class = None  # Return all pontos without pagination

    def get_queryset(self):
        rio_id = self.kwargs.get('rio_id')
        return PontoRisco.objects.filter(rio_id=rio_id).order_by('-criado_em')


def generate_fallback_description(nome, cidade, estado):
    nome_lower = nome.lower()
    
    # Rio Amazonas
    if "amazonas" in nome_lower:
        return {
            "comprimento": "6.992 km",
            "areas_risco": "Bairros ribeirinhos de Manaus",
            "foz": "Oceano Atlântico",
            "descricao_historico_enchentes": (
                "O Rio Amazonas possui a maior bacia hidrográfica do mundo. "
                "Suas cheias são marcantes, com destaque para a grande inundação de 2021 em Manaus, "
                "quando atingiu mais de 30 metros."
            ),
            "periodo_critico": "Maio a Julho",
            "using_fallback": True
        }
    
    # Rio São Francisco
    elif "são francisco" in nome_lower or "sao francisco" in nome_lower or "velho chico" in nome_lower:
        return {
            "comprimento": "2.830 km",
            "areas_risco": "Margens do Baixo São Francisco",
            "foz": "Oceano Atlântico",
            "descricao_historico_enchentes": (
                "O 'Velho Chico' é vital para o Nordeste brasileiro. Apesar de barragens controlarem a vazão, "
                "enchentes severas como a de 1979 causaram destruição maciça em dezenas de cidades."
            ),
            "periodo_critico": "Janeiro a Março",
            "using_fallback": True
        }

    # Rio Paraná
    elif "paraná" in nome_lower or "parana" in nome_lower:
        return {
            "comprimento": "4.880 km",
            "areas_risco": "Baixada de Foz do Iguaçu",
            "foz": "Estuário do Rio da Prata",
            "descricao_historico_enchentes": (
                "Alimenta hidrelétricas enormes como Itaipu. Historicamente, "
                "durante os efeitos intensos do El Niño em 1983 e 1992, o rio "
                "causou enchentes catastróficas submergindo diversas áreas ribeirinhas."
            ),
            "periodo_critico": "Outubro a Março",
            "using_fallback": True
        }

    # Rio Tietê
    elif "tietê" in nome_lower or "tiete" in nome_lower:
        return {
            "comprimento": "1.136 km",
            "areas_risco": "Várzeas da Grande SP",
            "foz": "Rio Paraná",
            "descricao_historico_enchentes": (
                "O rio drena a maior megalópole do país. O solo impermeável "
                "resultou em transbordamentos críticos nas cheias de 1999 e 2020."
            ),
            "periodo_critico": "Dezembro a Março",
            "using_fallback": True
        }

    # Rio Paraíba do Sul
    elif "paraíba" in nome_lower or "paraiba" in nome_lower:
        return {
            "comprimento": "1.137 km",
            "areas_risco": "Vale do Paraíba",
            "foz": "Oceano Atlântico",
            "descricao_historico_enchentes": (
                "Interliga São Paulo e Rio de Janeiro. Sofre enchentes violentas "
                "por calhas restritas, como o desastre dos rompimentos de diques no ano 2000."
            ),
            "periodo_critico": "Novembro a Março",
            "using_fallback": True
        }

    # Rio Negro
    elif "negro" in nome_lower:
        return {
            "comprimento": "2.250 km",
            "areas_risco": "Margens de Manaus e municípios do Alto Rio Negro",
            "foz": "Rio Amazonas",
            "descricao_historico_enchentes": (
                "O Rio Negro é o maior afluente da margem esquerda do Amazonas. "
                "Suas cheias históricas, como a de 2021, alagaram vastas áreas da região metropolitana de Manaus, "
                "atingindo níveis recordes acima de 30 metros."
            ),
            "periodo_critico": "Maio a Julho",
            "using_fallback": True
        }

    # Rio Madeira
    elif "madeira" in nome_lower:
        return {
            "comprimento": "3.250 km",
            "areas_risco": "Margens de Porto Velho e municípios ribeirinhos",
            "foz": "Rio Amazonas",
            "descricao_historico_enchentes": (
                "O Rio Madeira é um dos principais formadores do Amazonas. "
                "Enchentes severas como a de 2014 em Porto Velho desabrigaram milhares e "
                "paralisaram a hidrovia por semanas."
            ),
            "periodo_critico": "Janeiro a Abril",
            "using_fallback": True
        }

    # Rio Tocantins
    elif "tocantins" in nome_lower:
        return {
            "comprimento": "2.400 km",
            "areas_risco": "Margens de Marabá e Imperatriz",
            "foz": "Baía do Marajó (Rio Amazonas)",
            "descricao_historico_enchentes": (
                "Banha a região Norte e Centro-Oeste. As cheias sazonais do Tocantins "
                "atingem cidades como Marabá com frequência, com destaque para a enchente histórica de 2023."
            ),
            "periodo_critico": "Janeiro a Maio",
            "using_fallback": True
        }

    # Rio Xingu
    elif "xingu" in nome_lower:
        return {
            "comprimento": "2.200 km",
            "areas_risco": "Volta Grande do Xingu e Altamira",
            "foz": "Rio Amazonas",
            "descricao_historico_enchentes": (
                "Conhecido por suas corredeiras e pela usina de Belo Monte. "
                "Enchentes históricas impactam comunidades ribeirinhas e indígenas "
                "ao longo do curso."
            ),
            "periodo_critico": "Fevereiro a Junho",
            "using_fallback": True
        }

    # Rio Tapajós
    elif "tapajós" in nome_lower or "tapajos" in nome_lower:
        return {
            "comprimento": "1.900 km",
            "areas_risco": "Margens de Santarém e Itaituba",
            "foz": "Rio Amazonas",
            "descricao_historico_enchentes": (
                "Formado pelos rios Teles Pires e Juruena. Suas cheias sazonais "
                "elevam rapidamente o nível em Santarém, afetando bairros ribeirinhos."
            ),
            "periodo_critico": "Março a Junho",
            "using_fallback": True
        }

    # Rio Doce
    elif "doce" in nome_lower:
        return {
            "comprimento": "853 km",
            "areas_risco": "Vale do Rio Doce (MG/ES)",
            "foz": "Oceano Atlântico",
            "descricao_historico_enchentes": (
                "O Rio Doce foi palco da maior tragédia ambiental do Brasil com o rompimento da barragem de Fundão. "
                "Suas enchentes naturais históricas, como a de 1979, também causaram destruição severa."
            ),
            "periodo_critico": "Novembro a Março",
            "using_fallback": True
        }

    # Rio Iguaçu
    elif "iguaçu" in nome_lower or "iguacu" in nome_lower:
        return {
            "comprimento": "1.320 km",
            "areas_risco": "Bacia do Iguaçu e margens de Curitiba",
            "foz": "Rio Paraná",
            "descricao_historico_enchentes": (
                "Conhecido pelas Cataratas do Iguaçu, o rio drena a região Sul. "
                "Enchentes como a de 1983 e 2014 em União da Vitória marcaram sua história."
            ),
            "periodo_critico": "Outubro a Março",
            "using_fallback": True
        }

    # Rio Parnaíba
    elif "parnaíba" in nome_lower or "parnaiba" in nome_lower:
        return {
            "comprimento": "1.400 km",
            "areas_risco": "Planície litorânea do Piauí e Maranhão",
            "foz": "Oceano Atlântico (Delta do Parnaíba)",
            "descricao_historico_enchentes": (
                "O Rio Parnaíba forma a divisa natural entre Piauí e Maranhão. "
                "Suas cheias sazonais beneficiam a agricultura, mas também causam "
                "alagamentos em cidades ribeirinhas como Floriano."
            ),
            "periodo_critico": "Janeiro a Maio",
            "using_fallback": True
        }

    # Rio Genérico — dados determinísticos por nome para evitar repetição
    else:
        seed = sum(ord(c) for c in nome) + len(nome) * 31
        comp = 100 + (seed * 13) % 2400
        areas_map = [
            f"Margens urbanas de {cidade}",
            f"Cotas baixas de {cidade}",
            f"Região central de {cidade}",
            f"Zona ribeirinha de {cidade}",
            f"Várzeas de {cidade}",
        ]
        foz_map = [
            "Rio principal da bacia",
            "Bacia hidrográfica regional",
            "Afluente de destaque",
            "Calha principal do estado",
            "Curso d'água do bioma local",
        ]
        periodo_map = [
            "Novembro a Março",
            "Dezembro a Abril",
            "Outubro a Fevereiro",
            "Janeiro a Maio",
            "Estação chuvosa local",
        ]
        idx = seed % 5
        return {
            "comprimento": f"{comp} km",
            "areas_risco": areas_map[idx],
            "foz": foz_map[idx],
            "descricao_historico_enchentes": (
                f"O rio {nome}, que atravessa {cidade}, "
                "apresenta picos bruscos de vazão durante temporais intensos, "
                "demandando monitoramento contínuo pela Defesa Civil. "
                "Enchentes históricas registradas exigem atenção permanente."
            ),
            "periodo_critico": periodo_map[idx],
            "using_fallback": True
        }


class RiosGeminiDescriptionView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk):
        import os
        import requests
        import json
        
        try:
            rio = get_object_or_404(Rios, pk=pk)
            
            # 1. Verificar cache local no banco de dados
            cached_data = None
            if rio.descricao_gemini:
                try:
                    cached_data = json.loads(rio.descricao_gemini)
                except Exception:
                    pass
            
            api_key = os.getenv('GEMINI_API_KEY')
            
            # Consultar o Gemini se tiver API Key
            if api_key:
                logger.info(f"Consultando o Gemini 2.5 Flash para o rio: {rio.nome}")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
                
                prompt = f"""
Você é um especialista da Defesa Civil focado em relatórios EXTREMAMENTE ENXUTOS.
Forneça dados táticos do rio '{rio.nome}' localizado na região de '{rio.cidade} - {rio.estado}'.
MANTENHA TODOS OS CAMPOS MUITO CURTOS.

Você DEVE retornar a resposta estritamente no formato JSON abaixo. Sem formatação markdown, sem texto fora do JSON.

Estrutura do JSON exigida:
{{
  "comprimento": "Apenas o número e unidade (ex: '6.400 km')",
  "areas_risco": "No máximo 5 palavras citando a área (ex: 'Margens de Manaus')",
  "foz": "No máximo 3 palavras (ex: 'Oceano Atlântico')",
  "descricao_historico_enchentes": "Apenas 1 parágrafo curto (max 3 frases) informando o maior desastre do rio e sua bacia.",
  "periodo_critico": "Apenas os meses (ex: 'Maio a Julho')"
}}
"""
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": prompt
                        }]
                    }],
                    "generationConfig": {
                        "responseMimeType": "application/json"
                    }
                }
                
                try:
                    response = requests.post(url, json=payload, timeout=15)
                    if response.status_code == 200:
                        res_json = response.json()
                        text_response = res_json['candidates'][0]['content']['parts'][0]['text']
                        
                        # Limpeza preventiva caso retorne markdown
                        text_response = text_response.strip()
                        if text_response.startswith("```json"):
                            text_response = text_response[7:]
                        if text_response.endswith("```"):
                            text_response = text_response[:-3]
                        text_response = text_response.strip()
                        
                        data = json.loads(text_response)
                        data['using_fallback'] = False
                        
                        return Response(data)
                    else:
                        logger.error(f"Erro no Gemini API (Status: {response.status_code}): {response.text}")
                except Exception as e:
                    logger.error(f"Erro de conexão com Gemini: {str(e)}")
            
            # 3. Fallback (dados simulados extremamente realistas)
            fallback_data = generate_fallback_description(rio.nome, rio.cidade, rio.estado)
            return Response(fallback_data)
            
        except Exception as e:
            logger.error(f"Erro geral no RiosGeminiDescriptionView: {str(e)}")
            return Response(
                {"detail": "Erro ao obter descrição inteligente do rio."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


from django.db import connections
from django.db.utils import OperationalError

class PublicSummaryView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({
            'total_rios': Rios.objects.count(),
            'total_pontos': PontoRisco.objects.count(),
        })

class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        db_conn = connections['default']
        try:
            c = db_conn.cursor()
            c.execute("SELECT 1")
            db_status = "ok"
        except OperationalError:
            db_status = "error"

        return Response({
            "status": "ok" if db_status == "ok" else "degraded",
            "database": db_status,
            "engine": db_conn.settings_dict['ENGINE'],
        })

