import asyncio

import httpx
import pytest

from app import config, zonas
from tests.conftest import rodar

RIOS = [{"id": 1, "nome": "Rio A", "cidade": "Campinas"}, {"id": 2, "nome": "Rio B", "cidade": "Manaus"}]
PONTOS = {
    1: [{"id": 10, "rio": 1, "descricao": "Ponte", "latitude": -22.9, "longitude": -47.06}],
    2: [{"id": 20, "rio": 2, "descricao": "Porto", "latitude": "-3.1", "longitude": "-60.0"}],
}


@pytest.fixture(autouse=True)
def limpar_cache(monkeypatch):
    zonas._cache.update(quando=0.0, zonas=None)
    monkeypatch.setattr(zonas, "_trava", asyncio.Lock())
    yield
    zonas._cache.update(quando=0.0, zonas=None)


def api_falsa(chamadas, falhar_rio=None):
    async def get_json(cliente, caminho):
        chamadas.append(caminho)
        if caminho == "/publico/rios/":
            return RIOS
        rio_id = int(caminho.split("/")[3])
        if rio_id == falhar_rio:
            raise httpx.ConnectError("caiu")
        return PONTOS[rio_id]
    return get_json


def test_monta_zonas_de_todos_os_rios(monkeypatch):
    monkeypatch.setattr(zonas, "_get_json", api_falsa([]))
    resultado = rodar(zonas.carregar_zonas())
    assert {z["id"] for z in resultado} == {10, 20}
    porto = next(z for z in resultado if z["id"] == 20)
    assert porto["lat"] == -3.1 and porto["lng"] == -60.0  # a API às vezes manda como texto
    assert porto["rio"] == "Rio B" and porto["cidade"] == "Manaus"
    assert porto["raio_m"] == config.RAIO_ZONA_RISCO_M


def test_rio_com_falha_e_ignorado(monkeypatch):
    monkeypatch.setattr(zonas, "_get_json", api_falsa([], falhar_rio=2))
    assert [z["id"] for z in rodar(zonas.carregar_zonas())] == [10]


def test_usa_cache_dentro_da_validade(monkeypatch):
    chamadas = []
    monkeypatch.setattr(zonas, "_get_json", api_falsa(chamadas))
    rodar(zonas.carregar_zonas())
    rodar(zonas.carregar_zonas())
    assert chamadas.count("/publico/rios/") == 1


def test_forcar_ignora_cache(monkeypatch):
    chamadas = []
    monkeypatch.setattr(zonas, "_get_json", api_falsa(chamadas))
    rodar(zonas.carregar_zonas())
    rodar(zonas.carregar_zonas(forcar=True))
    assert chamadas.count("/publico/rios/") == 2


def test_hydrotech_fora_do_ar_propaga_erro(monkeypatch):
    async def fora(cliente, caminho):
        raise httpx.ConnectError("recusado")
    monkeypatch.setattr(zonas, "_get_json", fora)
    with pytest.raises(httpx.ConnectError):
        rodar(zonas.carregar_zonas())


def test_pedidos_simultaneos_fazem_uma_consulta_so(monkeypatch):
    chamadas = []
    falsa = api_falsa(chamadas)

    async def lenta(cliente, caminho):
        await asyncio.sleep(0.05)
        return await falsa(cliente, caminho)

    monkeypatch.setattr(zonas, "_get_json", lenta)

    async def muitos():
        return await asyncio.gather(*(zonas.carregar_zonas() for _ in range(25)))

    resultados = rodar(muitos())
    assert chamadas.count("/publico/rios/") == 1
    assert all(r == resultados[0] for r in resultados)
