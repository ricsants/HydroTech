from datetime import date

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from usuarios.models import Usuario
from .models import Sensor, SensorGroup, Leitura


class CompositeSensorTests(TestCase):
    """Testes do padrão Composite aplicado aos sensores."""

    def setUp(self):
        self.grupo_raiz = SensorGroup.objects.create(
            nome='Estação Bacia do Tietê', descricao='Raiz da árvore'
        )
        self.sensor_nivel = Sensor.objects.create(
            nome='Sensor nível Tietê', tipo='nivel_agua', unidade='m'
        )
        self.sensor_vazao = Sensor.objects.create(
            nome='Sensor vazão tributário', tipo='vazao', unidade='m³/s'
        )

    def test_leaf_nao_aceita_filhos(self):
        """Sensor é uma folha e não pode conter filhos."""
        with self.assertRaises(TypeError):
            self.sensor_nivel.adicionar(self.sensor_vazao)
        with self.assertRaises(TypeError):
            self.sensor_nivel.remover(self.sensor_vazao)

    def test_folha_retorna_apenas_si_mesma(self):
        self.assertEqual(self.sensor_nivel.get_sensores(), [self.sensor_nivel])
        self.assertEqual(self.sensor_nivel.get_tipo(), 'sensor')

    def test_grupo_agrega_sensores_diretos(self):
        self.grupo_raiz.adicionar(self.sensor_nivel)
        self.grupo_raiz.adicionar(self.sensor_vazao)
        sensores = self.grupo_raiz.get_sensores()
        self.assertEqual(len(sensores), 2)
        self.assertIn(self.sensor_nivel, sensores)
        self.assertIn(self.sensor_vazao, sensores)
        self.assertEqual(self.grupo_raiz.get_total_sensores(), 2)

    def test_grupo_agrega_recursivamente_subgrupos(self):
        subgrupo = SensorGroup.objects.create(nome='Subgrupo Afluente')
        sensor_profundidade = Sensor.objects.create(
            nome='Sensor profundidade', tipo='outro', unidade='m'
        )
        subgrupo.adicionar(sensor_profundidade)
        self.grupo_raiz.adicionar(subgrupo)
        self.grupo_raiz.adicionar(self.sensor_nivel)

        sensores = self.grupo_raiz.get_sensores()
        self.assertEqual(len(sensores), 2)
        self.assertIn(sensor_profundidade, sensores)
        self.assertIn(self.sensor_nivel, sensores)
        self.assertEqual(self.grupo_raiz.get_total_sensores(), 2)

    def test_grupo_remover_componente(self):
        self.grupo_raiz.adicionar(self.sensor_nivel)
        self.grupo_raiz.remover(self.sensor_nivel)
        self.assertIsNone(self.sensor_nivel.grupo)
        self.assertEqual(self.grupo_raiz.get_total_sensores(), 0)

    def test_sensor_fora_de_rio(self):
        """Sensores podem existir fora de um rio (rio=None)."""
        sensor_clima = Sensor.objects.create(
            nome='Pluviômetro urbano', tipo='pluviometria', unidade='mm',
            latitude=-23.55, longitude=-46.63,
        )
        self.assertIsNone(sensor_clima.rio)
        self.assertEqual(sensor_clima.get_tipo(), 'sensor')

    def test_leituras_agregadas_percorrem_subarvore(self):
        subgrupo = SensorGroup.objects.create(nome='Subgrupo')
        subgrupo.adicionar(self.sensor_nivel)
        self.grupo_raiz.adicionar(self.sensor_vazao)
        self.grupo_raiz.adicionar(subgrupo)

        Leitura.objects.create(sensor=self.sensor_nivel, valor=4.2)
        Leitura.objects.create(sensor=self.sensor_vazao, valor=120.5)

        leituras = self.grupo_raiz.get_leituras_agregadas()
        self.assertEqual(len(leituras), 2)


class SensorAPICompositeTests(TestCase):
    """Testes da API REST (Composite via endpoints)."""

    def setUp(self):
        self.client = APIClient()
        self.usuario = Usuario.objects.create(
            nome='Usuário Comum',
            email='sensor-test-1@example.org',
            senha='senha123',
            data_nascimento=date(1990, 1, 1),
        )
        self.defesa_civil = Usuario.objects.create(
            nome='Defesa Civil',
            email='sensor-test-2@example.org',
            senha='defesa123',
            data_nascimento=date(1985, 5, 5),
            is_defesa_civil=True,
        )

    def _auth(self, user):
        self.client.force_authenticate(user=user)

    def test_criar_grupo_e_sensor_requer_defesa_civil(self):
        url_grupo = '/sensores/grupos/'

        self._auth(self.usuario)
        resposta = self.client.post(url_grupo, {'nome': 'Estação Rio'}, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_403_FORBIDDEN)

        self._auth(self.defesa_civil)
        resposta = self.client.post(url_grupo, {'nome': 'Estação Rio'}, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        grupo_id = resposta.data['id']

        resposta = self.client.post(
            '/sensores/',
            {
                'nome': 'Sensor de Nível',
                'tipo': 'nivel_agua',
                'unidade': 'm',
                'grupo': grupo_id,
            },
            format='json',
        )
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resposta.data['grupo'], grupo_id)
        self.assertEqual(resposta.data['grupo_nome'], 'Estação Rio')

    def test_detalhe_do_grupo_retorna_arvore_composta(self):
        self._auth(self.defesa_civil)

        resposta = self.client.post(
            '/sensores/grupos/', {'nome': 'Estação Principal'}, format='json'
        )
        grupo_id = resposta.data['id']
        resposta = self.client.post(
            '/sensores/grupos/',
            {'nome': 'Subgrupo Afluente', 'parent': grupo_id},
            format='json',
        )
        subgrupo_id = resposta.data['id']
        self.client.post(
            '/sensores/',
            {
                'nome': 'Sensor Nível Afluente',
                'tipo': 'nivel_agua',
                'unidade': 'm',
                'grupo': subgrupo_id,
            },
            format='json',
        )

        resposta = self.client.get(f'/sensores/grupos/{grupo_id}/')
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data['subgrupos']), 1)
        self.assertEqual(resposta.data['subgrupos'][0]['sensores'][0]['nome'],
                         'Sensor Nível Afluente')
        self.assertEqual(resposta.data['total_sensores'], 1)

    def test_get_sem_autenticacao_retorna_permission_denied(self):
        resposta = self.client.get('/sensores/')
        self.assertIn(resposta.status_code,
                      (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_criar_leitura(self):
        self._auth(self.defesa_civil)
        resposta = self.client.post(
            '/sensores/',
            {
                'nome': 'Sensor de Chuva',
                'tipo': 'pluviometria',
                'unidade': 'mm',
            },
            format='json',
        )
        sensor_id = resposta.data['id']

        resposta = self.client.post(
            f'/sensores/{sensor_id}/leituras/',
            {'valor': 25.4},
            format='json',
        )
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resposta.data['sensor'], sensor_id)