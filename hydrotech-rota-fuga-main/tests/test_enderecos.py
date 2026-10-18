import asyncio
import time

import pytest

from app import enderecos
from tests.conftest import rodar
from tests.falsos import RespostaFalsa, cliente_falso


@pytest.fixture(autouse=True)
def estado_limpo(monkeypatch):
    monkeypatch.setattr(enderecos, "_cache", {})
    monkeypatch.setattr(enderecos, "_fila", asyncio.Lock())
    monkeypatch.setattr(enderecos, "_ultimo_pedido", {"quando": 0.0})


def test_monta_rua_e_bairro(monkeypatch):
    resposta = RespostaFalsa({"address": {"road": "Rua das Flores", "suburb": "Cambuí"}})
    monkeypatch.setattr(enderecos.httpx, "AsyncClient", cliente_falso(get=lambda url, **k: resposta))
    assert rodar(enderecos.nome_do_local(-22.9, -47.06)) == "Rua das Flores, Cambuí"


def test_usa_cache(monkeypatch):
    chamadas = []

    async def pedir(lat, lng):
        chamadas.append(1)
        return "Rua A, Centro"

    monkeypatch.setattr(enderecos, "_pedir_na_fila", pedir)
    assert rodar(enderecos.nome_do_local(-22.9, -47.06)) == "Rua A, Centro"
    assert rodar(enderecos.nome_do_local(-22.9, -47.06)) == "Rua A, Centro"
    assert len(chamadas) == 1


def test_lento_nao_segura_a_rota(monkeypatch):
    async def lento(lat, lng):
        await asyncio.sleep(5)

    monkeypatch.setattr(enderecos, "_pedir_na_fila", lento)
    inicio = time.monotonic()
    assert rodar(enderecos.nome_do_local(-22.9, -47.06, limite_s=0.2)) is None
    assert time.monotonic() - inicio < 1


def test_erro_devolve_none(monkeypatch):
    async def recusado(lat, lng):
        raise enderecos.httpx.HTTPStatusError("429", request=None, response=None)

    monkeypatch.setattr(enderecos, "_pedir_na_fila", recusado)
    assert rodar(enderecos.nome_do_local(-22.9, -47.06)) is None


def test_respeita_1_pedido_por_segundo(monkeypatch):
    momentos = []

    async def pedir(lat, lng):
        momentos.append(time.monotonic())
        return "Rua"

    monkeypatch.setattr(enderecos, "_pedir", pedir)

    async def tres_ao_mesmo_tempo():
        await asyncio.gather(*(enderecos._pedir_na_fila(-22.9, -47.06 + i) for i in range(3)))

    rodar(tres_ao_mesmo_tempo())
    intervalos = [b - a for a, b in zip(momentos, momentos[1:])]
    assert all(i >= 1.05 for i in intervalos), intervalos
