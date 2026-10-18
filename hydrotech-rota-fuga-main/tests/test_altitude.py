import pytest

from app import altitude, config, geo
from tests.conftest import ZONA_CENTRO, rodar
from tests.falsos import RespostaFalsa, cliente_falso, sem_espera


def meteo_ok(url, params):
    return RespostaFalsa({"elevation": [600.0] * len(params["latitude"].split(","))})


def topo_ok(url, params):
    return RespostaFalsa({"results": [{"elevation": 650.0} for _ in params["locations"].split("|")]})


def apis_falsas(meteo, topo=None, chamadas=None):
    """`meteo` e `topo` são listas de respostas, consumidas em ordem."""
    def get(url, params):
        if "opentopodata" in url:
            assert topo is not None, "não devia ter usado a fonte reserva"
            return topo.pop(0)(url, params)
        if chamadas is not None:
            chamadas.append(params)
        return meteo.pop(0)(url, params)
    return cliente_falso(get=get)


@pytest.fixture(autouse=True)
def cache_limpo(monkeypatch, tmp_path):
    monkeypatch.setattr(altitude, "_cache", {})
    monkeypatch.setattr(altitude, "ARQUIVO_CACHE", tmp_path / "altitudes.json")
    monkeypatch.setattr(altitude.asyncio, "sleep", sem_espera)


def test_segunda_consulta_vem_do_cache(monkeypatch):
    chamadas = []
    monkeypatch.setattr(altitude.httpx, "AsyncClient", apis_falsas([meteo_ok], chamadas=chamadas))
    pontos = [(-22.9, -47.06), (-22.91, -47.07)]
    assert rodar(altitude.altitudes(pontos)) == [600.0, 600.0]
    assert rodar(altitude.altitudes(pontos)) == [600.0, 600.0]
    assert len(chamadas) == 1


def test_vizinhos_dividem_o_cache(monkeypatch):
    chamadas = []
    monkeypatch.setattr(altitude.httpx, "AsyncClient", apis_falsas([meteo_ok], chamadas=chamadas))
    rodar(altitude.altitudes([(-22.90001, -47.06001)]))
    rodar(altitude.altitudes([(-22.90002, -47.06002)]))  # 2 m de distância
    assert len(chamadas) == 1


def test_429_espera_e_tenta_de_novo(monkeypatch):
    chamadas = []
    respostas = [lambda u, p: RespostaFalsa(status=429), meteo_ok]
    monkeypatch.setattr(altitude.httpx, "AsyncClient", apis_falsas(respostas, chamadas=chamadas))
    assert rodar(altitude.altitudes([(-22.9, -47.06)])) == [600.0]
    assert len(chamadas) == 2


def test_open_meteo_fora_usa_opentopodata(monkeypatch):
    respostas = [lambda u, p: RespostaFalsa(status=429)] * 2
    monkeypatch.setattr(altitude.httpx, "AsyncClient", apis_falsas(respostas, topo=[topo_ok]))
    assert rodar(altitude.altitudes([(-22.9, -47.06), (-22.91, -47.07)])) == [650.0, 650.0]


def test_as_duas_fontes_fora_devolve_none(monkeypatch):
    respostas = [lambda u, p: RespostaFalsa(status=429)] * 2
    monkeypatch.setattr(altitude.httpx, "AsyncClient",
                        apis_falsas(respostas, topo=[lambda u, p: RespostaFalsa(status=503)]))
    assert rodar(altitude.altitudes([(-22.9, -47.06)])) is None


def test_mais_de_100_pontos_vai_em_lotes(monkeypatch):
    chamadas = []
    monkeypatch.setattr(altitude.httpx, "AsyncClient", apis_falsas([meteo_ok, meteo_ok], chamadas=chamadas))
    pontos = [(-22.9 + i * 0.002, -47.06) for i in range(150)]
    assert len(rodar(altitude.altitudes(pontos))) == 150
    assert [len(c["latitude"].split(",")) for c in chamadas] == [100, 50]


def test_grade_cobre_o_circulo_e_nada_fora():
    celulas = list(altitude.grade_em_volta(-22.9056, -47.0584, 1000))
    assert all(geo.distancia_m(-22.9056, -47.0584, *c) <= 1000 for c in celulas)
    # área do círculo dividida pela de uma célula (~111 m x ~102 m) dá ~277
    assert 240 < len(celulas) < 320
    assert len(set(celulas)) == len(celulas)


def test_preaquecer_salva_e_nao_repete(monkeypatch):
    lotes = []

    async def meteo(chaves):
        lotes.append(len(chaves))
        return [700.0] * len(chaves)

    monkeypatch.setattr(altitude, "_open_meteo", meteo)
    monkeypatch.setattr(config, "RAIO_PREAQUECER_ALTITUDE_M", 600)
    n = rodar(altitude.preaquecer([ZONA_CENTRO], pausa_s=0))
    assert n == len(altitude._cache) > 0
    assert all(t <= 100 for t in lotes)

    monkeypatch.setattr(altitude, "_cache", {})
    assert altitude.carregar_do_disco() == n

    lotes.clear()
    assert rodar(altitude.preaquecer([ZONA_CENTRO], pausa_s=0)) == 0
    assert lotes == []


def test_preaquecer_para_se_as_duas_fontes_falharem(monkeypatch):
    async def falha(chaves):
        raise altitude.httpx.ConnectError("fora do ar")

    monkeypatch.setattr(altitude, "_open_meteo", falha)
    monkeypatch.setattr(altitude, "_opentopodata", falha)
    monkeypatch.setattr(config, "RAIO_PREAQUECER_ALTITUDE_M", 600)
    assert rodar(altitude.preaquecer([ZONA_CENTRO], pausa_s=0)) == 0


def test_preaquecer_respeita_o_limite_de_pontos(monkeypatch):
    async def meteo(chaves):
        return [700.0] * len(chaves)

    monkeypatch.setattr(altitude, "_open_meteo", meteo)
    monkeypatch.setattr(config, "MAX_PONTOS_PREAQUECER", 150)
    assert rodar(altitude.preaquecer([ZONA_CENTRO], pausa_s=0)) == 150


def test_carregar_sem_arquivo():
    assert altitude.carregar_do_disco() == 0
