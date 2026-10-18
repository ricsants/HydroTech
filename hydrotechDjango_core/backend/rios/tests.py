from django.test import TestCase

from usuarios.models import Usuario

from .models import PontoRisco, Rios


class PontosPublicosParaRotasTest(TestCase):
    def test_ponto_cadastrado_aparece_na_api_publica_com_coordenadas(self):
        usuario = Usuario.objects.create(
            nome="Equipe demo", email="demo@example.com", senha="teste",
            data_nascimento="2000-01-01", is_defesa_civil=True,
        )
        rio = Rios.objects.create(nome="Rio Demonstração", cidade="Campinas", estado="SP", criado_por=usuario)
        ponto = PontoRisco.objects.create(
            rio=rio, latitude=-22.9001, longitude=-47.0602,
            descricao="Ponte simulada", criado_por=usuario,
        )

        rios = self.client.get("/publico/rios/", secure=True)
        pontos = self.client.get(f"/publico/rios/{rio.id}/pontos-risco/", secure=True)

        self.assertEqual(rios.status_code, 200)
        self.assertEqual(pontos.status_code, 200)
        self.assertIn(rio.id, [item["id"] for item in rios.json()])
        self.assertEqual(len(pontos.json()), 1)
        self.assertEqual(pontos.json()[0]["id"], ponto.id)
        self.assertEqual(pontos.json()[0]["latitude"], -22.9001)
        self.assertEqual(pontos.json()[0]["longitude"], -47.0602)
        self.assertEqual(pontos.json()[0]["descricao"], "Ponte simulada")
