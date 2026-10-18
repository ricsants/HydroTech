import asyncio

import httpx
import pytest
from fastapi.testclient import TestClient

from app import main
from app.roteamento import RotaIndisponivel

cliente = TestClient(main.app)


@pytest.fixture
def fuga_falsa(monkeypatch):
    recebido = {}

    async def planejar(lat, lng, modo, alertas=None):
        recebido.update(lat=lat, lng=lng, modo=modo, alertas=alertas)
        return {"ok": True}
    monkeypatch.setattr(main, "planejar_fuga", planejar)
    return recebido


def test_tela_3d():
    r = cliente.get("/")
    assert r.status_code == 200
    assert "Rota de Fuga" in r.text and "maplibre-gl" in r.text and "setTerrain" in r.text


def test_tela_2d_de_reserva():
    r = cliente.get("/2d")
    assert r.status_code == 200
    assert "leaflet" in r.text


def test_rota_fuga_repassa_parametros(fuga_falsa):
    r = cliente.get("/rota-fuga", params={"lat": -22.9, "lng": -47.06, "modo": "carro"})
    assert r.status_code == 200 and r.json() == {"ok": True}
    assert fuga_falsa == {"lat": -22.9, "lng": -47.06, "modo": "carro", "alertas": None}


def test_modo_padrao_e_a_pe(fuga_falsa):
    cliente.get("/rota-fuga", params={"lat": -22.9, "lng": -47.06})
    assert fuga_falsa["modo"] == "pe"


@pytest.mark.parametrize("params", [
    {"lat": 91, "lng": 0},
    {"lat": 0, "lng": 181},
    {"lat": "abc", "lng": 0},
    {"lat": "nan", "lng": 0},
    {"lat": 0, "lng": "inf"},
    {"lng": 0},
    {"lat": 0, "lng": 0, "modo": "aviao"},
])
def test_parametros_invalidos(params, fuga_falsa):
    assert cliente.get("/rota-fuga", params=params).status_code == 422


def test_sem_rota_devolve_503(monkeypatch):
    async def falha(*a):
        raise RotaIndisponivel("Nenhum serviço de rotas respondeu.")
    monkeypatch.setattr(main, "planejar_fuga", falha)
    r = cliente.get("/rota-fuga", params={"lat": -22.9, "lng": -47.06})
    assert r.status_code == 503 and "rotas" in r.json()["detail"]


def test_zonas_risco_com_hydrotech_fora(monkeypatch):
    async def fora(*a, **k):
        raise httpx.ConnectError("recusado")
    monkeypatch.setattr(main, "carregar_zonas", fora)
    assert cliente.get("/zonas-risco").status_code == 502


def test_status():
    dados = cliente.get("/status").json()
    assert set(dados) == {"hydrotech_api", "desvio_de_zonas", "raio_zona_risco_m"}


def test_cors_liberado(fuga_falsa):
    r = cliente.get("/rota-fuga", params={"lat": -22.9, "lng": -47.06}, headers={"Origin": "http://localhost:5173"})
    assert r.headers.get("access-control-allow-origin") == "*"


def test_pedido_lento_demais_devolve_503(monkeypatch):
    async def lento(*a):
        await asyncio.sleep(5)

    monkeypatch.setattr(main, "planejar_fuga", lento)
    monkeypatch.setattr(main.config, "TIMEOUT_PEDIDO_S", 0.2)
    r = cliente.get("/rota-fuga", params={"lat": -22.9, "lng": -47.06})
    assert r.status_code == 503 and "Defesa Civil" in r.json()["detail"]


def test_alerta_vira_conjunto_de_ids(fuga_falsa):
    r = cliente.get("/rota-fuga", params={"lat": -22.9, "lng": -47.06, "alerta": "7,9"})
    assert r.status_code == 200 and fuga_falsa["alertas"] == {7, 9}


@pytest.mark.parametrize("alerta", ["abc", "7,", ",7", "7;9", "-1", "7 9"])
def test_alerta_invalido(alerta, fuga_falsa):
    assert cliente.get("/rota-fuga", params={"lat": -22.9, "lng": -47.06, "alerta": alerta}).status_code == 422


def test_zonas_risco_filtra_pelo_alerta(monkeypatch):
    async def zonas(*a, **k):
        return [{"id": 1}, {"id": 2}, {"id": 3}]
    monkeypatch.setattr(main, "carregar_zonas", zonas)
    assert [z["id"] for z in cliente.get("/zonas-risco", params={"alerta": "2"}).json()] == [2]
    assert len(cliente.get("/zonas-risco").json()) == 3


def test_atualizar_zonas_ignora_cache(monkeypatch):
    recebido = []

    async def zonas(*a, **kwargs):
        recebido.append(kwargs.get("forcar"))
        return []

    monkeypatch.setattr(main, "carregar_zonas", zonas)
    assert cliente.get("/zonas-risco", params={"atualizar": "1"}).status_code == 200
    assert recebido == [True]
