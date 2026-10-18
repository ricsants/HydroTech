import asyncio
import random
import time

import pytest

from app import destinos, geo, servico
from app.roteamento import RotaIndisponivel
from tests.conftest import ZONA_CENTRO, rodar

FORA = (-22.9056, -47.0640)    # uns 570 m a oeste do centro da zona
DENTRO = (-22.9056, -47.0590)  # uns 60 m do centro
ZONA_OUTRA = {**ZONA_CENTRO, "id": 2, "lat": -22.9100, "lng": -47.0700}
ROTA_QUE_CRUZA = {"distancia_m": 900, "duracao_s": 600, "zonas_cruzadas": [1]}


def candidato(lat, lng, nota, dist=1000):
    return {"lat": lat, "lng": lng, "nota": nota, "nome": "Área segura", "tipo": "Ponto mais seguro ao alcance",
            "distancia_linha_reta_m": dist, "distancia_risco_m": 900.0, "acima_do_risco_m": 20.0}


def rota_osrm_sem_desvio():
    async def rota(origem, destino, modo, zonas_desvio):
        return {"provedor": "osrm", "desvia_zonas": False, "passos": [], "distancia_m": 1000, "duracao_s": 700,
                "geometria": {"type": "LineString", "coordinates": []}, "zonas_cruzadas": []}
    return rota


@pytest.fixture
def ambiente(monkeypatch):
    """HydroTech, destinos, rotas e Nominatim falsos. Os testes mexem no dict que volta."""
    estado = {
        "zonas": [ZONA_CENTRO],
        "candidatos": [candidato(-22.92, -47.07, 2.0), candidato(-22.89, -47.07, 1.5)],
        "avisos_destino": [],
        "rotas": {},            # (lat, lng) do destino -> rota ou exceção
        "chamadas_rota": [],
    }

    async def zonas(forcar=False):
        if isinstance(estado["zonas"], Exception):
            raise estado["zonas"]
        return estado["zonas"]

    async def area_mais_segura(lat, lng, z):
        estado["zonas_destino"] = z
        return [dict(c) for c in estado["candidatos"]], list(estado["avisos_destino"])

    async def calcular_rota(origem, destino, modo, zonas_desvio):
        estado["chamadas_rota"].append((destino, modo, zonas_desvio))
        r = estado["rotas"].get(destino, {"distancia_m": 1000, "duracao_s": 700, "zonas_cruzadas": []})
        if isinstance(r, Exception):
            raise r
        return {"provedor": "openrouteservice", "desvia_zonas": True, "passos": [],
                "geometria": {"type": "LineString", "coordinates": []}, **r}

    async def nome_do_local(lat, lng):
        return "Rua Teste, Bairro Teste"

    monkeypatch.setattr(servico, "carregar_zonas", zonas)
    monkeypatch.setattr(servico, "area_mais_segura", area_mais_segura)
    monkeypatch.setattr(servico, "calcular_rota", calcular_rota)
    monkeypatch.setattr(servico, "nome_do_local", nome_do_local)
    monkeypatch.setattr(servico, "ors_disponivel", lambda: True)
    return estado


def test_fluxo_normal(ambiente):
    r = rodar(servico.planejar_fuga(*FORA, "pe"))
    assert r["dentro_de_zona_risco"] is False
    assert r["destino"]["lat"] == -22.92
    assert r["destino"]["endereco"] == "Rua Teste, Bairro Teste"
    assert "nota" not in r["destino"]
    # a primeira rota já serviu, então não gastou chamada com a segunda
    assert len(ambiente["chamadas_rota"]) == 1 and r["alternativas"] == []
    assert r["zonas_risco"] == [ZONA_CENTRO]
    assert r["avisos"] == []
    assert "travelmode=walking" in r["links"]["google_maps"]
    assert r["links"]["waze"].startswith("https://waze.com/ul?ll=-22.920000,-47.070000")


def test_modo_carro(ambiente):
    r = rodar(servico.planejar_fuga(*FORA, "carro"))
    assert all(modo == "carro" for _, modo, _ in ambiente["chamadas_rota"])
    assert "travelmode=driving" in r["links"]["google_maps"]


def test_dentro_da_zona_avisa_e_nao_desvia_dela(ambiente):
    r = rodar(servico.planejar_fuga(*DENTRO, "pe"))
    assert r["dentro_de_zona_risco"] is True
    assert r["avisos"][0] == servico.AVISO_DENTRO
    assert all(zonas_desvio == [] for _, _, zonas_desvio in ambiente["chamadas_rota"])
    assert ambiente["zonas_destino"] == [ZONA_CENTRO]  # o destino continua fora dela


def test_zona_muito_longe_e_ignorada(ambiente):
    ambiente["zonas"] = [{**ZONA_CENTRO, "id": 99, "lat": -3.1, "lng": -60.0}]  # Manaus
    assert rodar(servico.planejar_fuga(*FORA, "pe"))["zonas_risco"] == []


def test_hydrotech_fora_do_ar_ainda_da_rota(ambiente):
    ambiente["zonas"] = ConnectionError("HydroTech caiu")
    r = rodar(servico.planejar_fuga(*FORA, "pe"))
    assert r["destino"]
    assert any("HydroTech" in a for a in r["avisos"])


def test_prefere_rota_que_nao_cruza_zona(ambiente):
    ambiente["rotas"][(-22.92, -47.07)] = ROTA_QUE_CRUZA
    r = rodar(servico.planejar_fuga(*FORA, "pe"))
    assert r["destino"]["lat"] == -22.89
    assert r["alternativas"][0]["cruza_zona_risco"] is True


def test_todas_cruzam_avisa(ambiente):
    for c in ambiente["candidatos"]:
        ambiente["rotas"][(c["lat"], c["lng"])] = ROTA_QUE_CRUZA
    r = rodar(servico.planejar_fuga(*FORA, "pe"))
    assert any("cruza uma área de risco simulada" in a for a in r["avisos"])


def test_rota_que_da_muita_volta_perde_pontos(ambiente):
    ambiente["rotas"][(-22.92, -47.07)] = {"distancia_m": 5000, "duracao_s": 3600, "zonas_cruzadas": []}
    assert rodar(servico.planejar_fuga(*FORA, "pe"))["destino"]["lat"] == -22.89


def test_uma_rota_falha_usa_a_outra(ambiente):
    ambiente["rotas"][(-22.92, -47.07)] = RotaIndisponivel("ORS caiu")
    assert rodar(servico.planejar_fuga(*FORA, "pe"))["destino"]["lat"] == -22.89


def test_sem_nenhuma_rota_ainda_indica_o_destino(ambiente):
    for c in ambiente["candidatos"]:
        ambiente["rotas"][(c["lat"], c["lng"])] = RotaIndisponivel("sem rede")
    r = rodar(servico.planejar_fuga(*FORA, "pe"))
    assert r["rota"] is None
    assert r["destino"]["lat"] == -22.92 and r["destino"]["endereco"] == "Rua Teste, Bairro Teste"
    assert r["links"]["google_maps"] and r["links"]["waze"]
    assert any("Google Maps" in a for a in r["avisos"])
    assert "nota" not in r["destino"]


def test_servico_de_rota_fora_desiste_rapido(ambiente, monkeypatch):
    monkeypatch.setattr(servico, "ors_disponivel", lambda: False)
    ambiente["candidatos"] = [candidato(-22.92 + i * 0.01, -47.07 - i * 0.01, 2.0 - i * 0.1) for i in range(6)]
    for c in ambiente["candidatos"]:
        ambiente["rotas"][(c["lat"], c["lng"])] = RotaIndisponivel("timeout")
    r = rodar(servico.planejar_fuga(*FORA, "pe"))
    assert len(ambiente["chamadas_rota"]) == 2
    assert r["rota"] is None


def test_sem_candidatos_da_erro_claro(ambiente):
    ambiente["candidatos"] = []
    with pytest.raises(RotaIndisponivel, match="destino estimado"):
        rodar(servico.planejar_fuga(*FORA, "pe"))


def test_repassa_os_avisos_do_destino(ambiente):
    ambiente["avisos_destino"] = ["Altitude indisponível agora"]
    assert "Altitude indisponível agora" in rodar(servico.planejar_fuga(*FORA, "pe"))["avisos"]


def test_sem_chave_do_ors_manda_configurar(ambiente, monkeypatch):
    monkeypatch.setattr(servico.config, "ORS_API_KEY", "")
    monkeypatch.setattr(servico, "calcular_rota", rota_osrm_sem_desvio())
    assert any("ORS_API_KEY" in a for a in rodar(servico.planejar_fuga(*FORA, "pe"))["avisos"])


def test_com_chave_mas_sem_cota_explica_o_motivo(ambiente, monkeypatch):
    monkeypatch.setattr(servico.config, "ORS_API_KEY", "chave")
    monkeypatch.setattr(servico, "calcular_rota", rota_osrm_sem_desvio())
    avisos = rodar(servico.planejar_fuga(*FORA, "pe"))["avisos"]
    assert any("Desvio automático indisponível" in a for a in avisos)
    assert not any("configure" in a for a in avisos)


def test_so_tenta_o_proximo_quando_precisa(ambiente):
    ambiente["candidatos"].append(candidato(-22.88, -47.08, 1.0))
    ambiente["rotas"][(-22.92, -47.07)] = ROTA_QUE_CRUZA
    r = rodar(servico.planejar_fuga(*FORA, "pe"))
    assert len(ambiente["chamadas_rota"]) == 2  # a 1ª cruzou, a 2ª serviu, a 3ª nem foi calculada
    assert r["destino"]["lat"] == -22.89


def test_limite_de_tentativas(ambiente, monkeypatch):
    monkeypatch.setattr(servico.config, "CANDIDATOS_ROTA", 2)
    ambiente["candidatos"].append(candidato(-22.88, -47.08, 1.0))
    for c in ambiente["candidatos"]:
        ambiente["rotas"][(c["lat"], c["lng"])] = ROTA_QUE_CRUZA
    rodar(servico.planejar_fuga(*FORA, "pe"))
    assert len(ambiente["chamadas_rota"]) == 2


def test_tentativas_alternam_a_direcao():
    norte = [candidato(-22.890 + i * 0.001, -47.064, 3.0 - i * 0.1) for i in range(3)]
    sul = candidato(-22.92, -47.064, 1.0)
    ordem = servico._ordem_de_tentativa(norte + [sul], *FORA)
    assert ordem[0] is norte[0] and ordem[1] is sul
    assert len(ordem) == 4


def test_sem_ors_tenta_mais_destinos(ambiente, monkeypatch):
    monkeypatch.setattr(servico, "ors_disponivel", lambda: False)
    monkeypatch.setattr(servico.config, "CANDIDATOS_ROTA", 2)
    monkeypatch.setattr(servico.config, "CANDIDATOS_ROTA_SEM_DESVIO", 4)
    ambiente["candidatos"] = [candidato(-22.92 + i * 0.01, -47.07 - i * 0.01, 2.0 - i * 0.1) for i in range(6)]
    ordem = servico._ordem_de_tentativa(ambiente["candidatos"], *FORA)
    for c in ordem[:3]:
        ambiente["rotas"][(c["lat"], c["lng"])] = ROTA_QUE_CRUZA
    r = rodar(servico.planejar_fuga(*FORA, "pe"))
    # com ORS pararia na 2ª tentativa; sem ele vai até a 4ª, que não cruza
    assert len(ambiente["chamadas_rota"]) == 4
    assert r["rota"]["zonas_cruzadas"] == []
    assert (r["destino"]["lat"], r["destino"]["lng"]) == (ordem[3]["lat"], ordem[3]["lng"])


def test_25_pessoas_juntas_nao_travam_o_servico(monkeypatch):
    """Cada serviço externo leva 0,3 s. Se a gente fosse o gargalo, isso passaria fácil de 3 s."""
    async def depois_de_um_tempo(valor):
        await asyncio.sleep(0.3)
        return valor

    async def zonas(forcar=False):
        return await depois_de_um_tempo([ZONA_CENTRO])

    async def altitudes(pontos):
        return await depois_de_um_tempo([600.0] + [620.0] * (len(pontos) - 1))

    async def rota(origem, destino, modo, zonas_desvio):
        return await depois_de_um_tempo({"provedor": "openrouteservice", "desvia_zonas": True, "passos": [],
                                         "geometria": {"type": "LineString", "coordinates": []},
                                         "distancia_m": 1200, "duracao_s": 900, "zonas_cruzadas": []})

    async def nome(lat, lng):
        return await depois_de_um_tempo("Rua X")

    monkeypatch.setattr(servico, "carregar_zonas", zonas)
    monkeypatch.setattr(destinos, "altitudes", altitudes)
    monkeypatch.setattr(servico, "calcular_rota", rota)
    monkeypatch.setattr(servico, "nome_do_local", nome)
    monkeypatch.setattr(servico, "ors_disponivel", lambda: True)

    random.seed(1)
    pessoas = [geo.deslocar(ZONA_CENTRO["lat"], ZONA_CENTRO["lng"], random.uniform(0, 360), random.uniform(0, 1500))
               for _ in range(25)]

    async def todos():
        return await asyncio.gather(*(servico.planejar_fuga(*p, "pe") for p in pessoas))

    inicio = time.monotonic()
    assert len(rodar(todos())) == 25
    assert time.monotonic() - inicio < 3


def test_filtrar_alertas():
    zonas = [ZONA_CENTRO, ZONA_OUTRA]
    assert servico.filtrar_alertas(zonas, None) == (zonas, [])
    assert servico.filtrar_alertas(zonas, {2}) == ([ZONA_OUTRA], [])
    ativas, avisos = servico.filtrar_alertas(zonas, {99})
    assert ativas == zonas and "não foi encontrado" in avisos[0]


def test_com_alerta_considera_todas_as_zonas_no_trajeto(ambiente):
    ambiente["zonas"] = [ZONA_CENTRO, ZONA_OUTRA]
    r = rodar(servico.planejar_fuga(*FORA, "pe", {2}))
    assert r["zonas_risco"] == [ZONA_CENTRO, ZONA_OUTRA]
    assert ambiente["zonas_destino"] == [ZONA_CENTRO, ZONA_OUTRA]


def test_dentro_de_outra_zona_que_nao_esta_em_alerta(ambiente):
    ambiente["zonas"] = [ZONA_CENTRO, ZONA_OUTRA]
    assert rodar(servico.planejar_fuga(*DENTRO, "pe", {2}))["dentro_de_zona_risco"] is True


def test_alerta_de_ponto_apagado_evita_todas(ambiente):
    ambiente["zonas"] = [ZONA_CENTRO, ZONA_OUTRA]
    r = rodar(servico.planejar_fuga(*FORA, "pe", {99}))
    assert len(r["zonas_risco"]) == 2
    assert any("não foi encontrado" in a for a in r["avisos"])
