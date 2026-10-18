import httpx
import pytest

from app import config, roteamento
from tests.conftest import ZONA_CENTRO, rodar
from tests.falsos import RespostaFalsa, cliente_falso, sem_espera

ORIGEM, DESTINO = (-22.9056, -47.0640), (-22.9056, -47.0520)
LINHA_ATRAVESSANDO = {"type": "LineString", "coordinates": [[-47.0640, -22.9056], [-47.0520, -22.9056]]}
LINHA_CONTORNANDO = {"type": "LineString", "coordinates": [
    [-47.0640, -22.9056], [-47.0640, -22.9000], [-47.0520, -22.9000], [-47.0520, -22.9056]]}


def rota_falsa(geometria, provedor="osrm", duracao=600):
    return {"provedor": provedor, "desvia_zonas": provedor == "openrouteservice", "geometria": geometria,
            "distancia_m": 1000, "duracao_s": duracao, "passos": [{"instrucao": "Siga", "distancia_m": 10}]}


def resposta_ors(geometria=LINHA_CONTORNANDO, resumo=None, passos=()):
    return RespostaFalsa({"features": [{"geometry": geometria, "properties": {
        "summary": resumo or {}, "segments": [{"steps": list(passos)}]}}]})


@pytest.fixture(autouse=True)
def sem_pausas(monkeypatch):
    monkeypatch.setattr(roteamento, "_pausas", {"ors": 0.0, "osrm": 0.0})
    monkeypatch.setattr(roteamento.asyncio, "sleep", sem_espera)


@pytest.mark.parametrize("passo,esperado", [
    ({"maneuver": {"type": "depart"}, "name": "Rua A"}, "Siga na Rua A"),
    ({"maneuver": {"type": "depart"}, "name": ""}, "Comece a seguir"),
    ({"maneuver": {"type": "arrive"}}, "Você chegou ao destino estimado da simulação"),
    ({"maneuver": {"type": "turn", "modifier": "left"}, "name": "Rua B"}, "Vire à esquerda na Rua B"),
    ({"maneuver": {"type": "turn", "modifier": "sharp right"}, "name": ""}, "Vire fortemente à direita"),
    ({"maneuver": {"type": "turn", "modifier": "uturn"}}, "Faça o retorno"),
    ({"maneuver": {"type": "continue", "modifier": "straight"}, "name": "Av C"}, "Continue em frente na Av C"),
    ({"maneuver": {"type": "roundabout", "exit": 2}, "name": "Rua D"}, "Na rotatória, pegue a 2ª saída na Rua D"),
    ({"maneuver": {"type": "fork"}, "name": "Rua E"}, "Siga na Rua E"),
])
def test_instrucoes_do_osrm_em_portugues(passo, esperado):
    assert roteamento.instrucao_osrm(passo) == esperado


def test_usa_ors_quando_tem_chave(monkeypatch):
    monkeypatch.setattr(config, "ORS_API_KEY", "chave-teste")
    zonas_enviadas = []

    async def ors(origem, destino, modo, zonas):
        zonas_enviadas.append(zonas)
        return rota_falsa(LINHA_CONTORNANDO, "openrouteservice")

    async def osrm(*args):
        raise AssertionError("não devia chamar o OSRM")

    monkeypatch.setattr(roteamento, "_rota_ors", ors)
    monkeypatch.setattr(roteamento, "_rota_osrm", osrm)
    rota = rodar(roteamento.calcular_rota(ORIGEM, DESTINO, "pe", [ZONA_CENTRO]))
    assert rota["provedor"] == "openrouteservice"
    assert rota["zonas_cruzadas"] == []
    assert zonas_enviadas == [[ZONA_CENTRO]]


def test_cai_para_o_osrm_se_o_ors_falhar(monkeypatch):
    monkeypatch.setattr(config, "ORS_API_KEY", "chave-teste")

    async def ors(*args):
        raise roteamento.RotaIndisponivel("ORS 500")

    async def osrm(*args):
        return rota_falsa(LINHA_CONTORNANDO)

    monkeypatch.setattr(roteamento, "_rota_ors", ors)
    monkeypatch.setattr(roteamento, "_rota_osrm", osrm)
    assert rodar(roteamento.calcular_rota(ORIGEM, DESTINO, "pe", [ZONA_CENTRO]))["provedor"] == "osrm"


def test_osrm_tenta_duas_vezes_e_desiste(monkeypatch):
    monkeypatch.setattr(config, "ORS_API_KEY", "")
    tentativas = []

    async def osrm(*args):
        tentativas.append(1)
        raise httpx.ConnectError("sem rede")

    monkeypatch.setattr(roteamento, "_rota_osrm", osrm)
    with pytest.raises(roteamento.RotaIndisponivel):
        rodar(roteamento.calcular_rota(ORIGEM, DESTINO, "pe", [ZONA_CENTRO]))
    assert len(tentativas) == 2


def test_osrm_segunda_tentativa_funciona(monkeypatch):
    monkeypatch.setattr(config, "ORS_API_KEY", "")
    tentativas = []

    async def osrm(*args):
        tentativas.append(1)
        if len(tentativas) == 1:
            raise httpx.ConnectError("conexão caiu")
        return rota_falsa(LINHA_CONTORNANDO)

    monkeypatch.setattr(roteamento, "_rota_osrm", osrm)
    assert rodar(roteamento.calcular_rota(ORIGEM, DESTINO, "pe", []))["provedor"] == "osrm"


def test_osrm_timeout_nao_repete_e_pausa(monkeypatch):
    monkeypatch.setattr(config, "ORS_API_KEY", "")
    chamadas = []

    async def osrm(*args):
        chamadas.append(1)
        raise httpx.ReadTimeout("lento")

    monkeypatch.setattr(roteamento, "_rota_osrm", osrm)
    for _ in range(3):
        with pytest.raises(roteamento.RotaIndisponivel):
            rodar(roteamento.calcular_rota(ORIGEM, DESTINO, "pe", []))
    assert len(chamadas) == 1  # as outras duas nem chegam a chamar, o OSRM está em pausa


def test_marca_as_zonas_cruzadas(monkeypatch):
    monkeypatch.setattr(config, "ORS_API_KEY", "")

    async def osrm(*args):
        return rota_falsa(LINHA_ATRAVESSANDO)

    monkeypatch.setattr(roteamento, "_rota_osrm", osrm)
    rota = rodar(roteamento.calcular_rota(ORIGEM, DESTINO, "pe", [ZONA_CENTRO]))
    assert rota["zonas_cruzadas"] == [ZONA_CENTRO["id"]]


def test_osrm_prefere_a_alternativa_que_nao_cruza(monkeypatch):
    dados = {"code": "Ok", "routes": [
        {"geometry": LINHA_ATRAVESSANDO, "distance": 1200, "duration": 500, "legs": [{"steps": []}]},
        {"geometry": LINHA_CONTORNANDO, "distance": 1800, "duration": 800, "legs": [{"steps": []}]},
    ]}
    monkeypatch.setattr(roteamento.httpx, "AsyncClient", cliente_falso(get=lambda url, **k: RespostaFalsa(dados)))
    rota = rodar(roteamento._rota_osrm(ORIGEM, DESTINO, "pe", [ZONA_CENTRO]))
    assert rota["geometria"] == LINHA_CONTORNANDO
    assert rota["duracao_s"] == 800


def test_ors_manda_as_zonas_como_poligonos(monkeypatch):
    enviado = {}

    def post(url, json, headers):
        enviado.update(url=url, corpo=json, headers=headers)
        return resposta_ors(resumo={"distance": 1500.4, "duration": 900.6},
                            passos=[{"instruction": "Vire à direita", "distance": 120.2}])

    monkeypatch.setattr(config, "ORS_API_KEY", "chave-teste")
    monkeypatch.setattr(roteamento.httpx, "AsyncClient", cliente_falso(post=post))
    rota = rodar(roteamento._rota_ors(ORIGEM, DESTINO, "carro", [ZONA_CENTRO]))

    poligonos = enviado["corpo"]["options"]["avoid_polygons"]
    assert poligonos["type"] == "MultiPolygon" and len(poligonos["coordinates"]) == 1
    assert enviado["url"].endswith("/driving-car/geojson")
    assert enviado["headers"]["Authorization"] == "chave-teste"
    assert enviado["corpo"]["coordinates"][0] == [ORIGEM[1], ORIGEM[0]]  # GeoJSON é [lng, lat]
    assert rota["distancia_m"] == 1500 and rota["duracao_s"] == 901
    assert rota["passos"] == [{"instrucao": "Vire à direita", "distancia_m": 120}]


def test_ors_sem_zonas_nao_manda_options(monkeypatch):
    enviado = {}

    def post(url, json, headers):
        enviado.update(corpo=json)
        return resposta_ors()

    monkeypatch.setattr(roteamento.httpx, "AsyncClient", cliente_falso(post=post))
    rodar(roteamento._rota_ors(ORIGEM, DESTINO, "pe", []))
    assert "options" not in enviado["corpo"]


def test_ors_429_espera_e_tenta_de_novo(monkeypatch):
    respostas = [RespostaFalsa(status=429), resposta_ors(resumo={"distance": 10, "duration": 5})]
    esperas = []

    async def dormir(segundos):
        esperas.append(segundos)

    monkeypatch.setattr(roteamento.httpx, "AsyncClient", cliente_falso(post=lambda url, **k: respostas.pop(0)))
    monkeypatch.setattr(roteamento.asyncio, "sleep", dormir)
    rota = rodar(roteamento._rota_ors(ORIGEM, DESTINO, "pe", []))
    assert rota["provedor"] == "openrouteservice"
    assert esperas == [1.2]


def test_ors_429_que_nao_passa_vira_erro(monkeypatch):
    sempre_429 = RespostaFalsa({"error": "Rate Limit Exceeded"}, 429)
    monkeypatch.setattr(roteamento.httpx, "AsyncClient", cliente_falso(post=lambda url, **k: sempre_429))
    with pytest.raises(roteamento.RotaIndisponivel, match="429"):
        rodar(roteamento._rota_ors(ORIGEM, DESTINO, "pe", []))


def test_cota_esgotada_pausa_o_ors(monkeypatch):
    monkeypatch.setattr(config, "ORS_API_KEY", "chave-teste")
    posts = []

    def post(url, **kwargs):
        posts.append(1)
        return RespostaFalsa({"error": "Quota exceeded"}, 403)

    async def osrm(*args):
        return rota_falsa(LINHA_CONTORNANDO)

    monkeypatch.setattr(roteamento.httpx, "AsyncClient", cliente_falso(post=post))
    monkeypatch.setattr(roteamento, "_rota_osrm", osrm)
    for _ in range(3):
        assert rodar(roteamento.calcular_rota(ORIGEM, DESTINO, "pe", []))["provedor"] == "osrm"
    assert len(posts) == 1
    assert not roteamento.ors_disponivel()


def test_ors_disponivel_com_chave_e_sem_pausa(monkeypatch):
    monkeypatch.setattr(config, "ORS_API_KEY", "chave-teste")
    assert roteamento.ors_disponivel()
    monkeypatch.setattr(config, "ORS_API_KEY", "")
    assert not roteamento.ors_disponivel()
