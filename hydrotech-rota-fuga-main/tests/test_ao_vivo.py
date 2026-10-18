"""
Testes contra os serviços de verdade. Antes de rodar (pytest --ao-vivo):
- HydroTech no ar, com o ponto de teste de conftest.ZONA_CENTRO cadastrado;
- este serviço rodando em http://127.0.0.1:8100;
- internet e ORS_API_KEY no .env.
"""
import asyncio
import random
import time

import httpx
import pytest

from app import config, geo
from tests.conftest import ZONA_CENTRO

pytestmark = pytest.mark.ao_vivo
SERVICO = "http://127.0.0.1:8100"


def pedir(lat, lng, modo="pe"):
    inicio = time.monotonic()
    r = httpx.get(f"{SERVICO}/rota-fuga", params={"lat": lat, "lng": lng, "modo": modo}, timeout=60)
    return r, time.monotonic() - inicio


def conferir_rota_segura(d, zonas):
    destino, rota = d["destino"], d["rota"]
    for z in zonas:
        borda = geo.distancia_m(destino["lat"], destino["lng"], z["lat"], z["lng"]) - z["raio_m"]
        assert borda >= config.MARGEM_DESTINO_M - 1, f"destino a {borda:.0f} m da zona {z['id']}"
    if rota is None:
        # sem serviço de rota a resposta ainda tem que dizer para onde ir
        assert any("Google Maps" in a for a in d["avisos"]) and d["links"]["google_maps"], d["avisos"]
        return
    # a rota não pode atravessar zona nenhuma, fora a que a pessoa já está dentro
    origem = (d["origem"]["lat"], d["origem"]["lng"])
    for z in zonas:
        if geo.distancia_m(*origem, z["lat"], z["lng"]) <= z["raio_m"]:
            continue
        assert not geo.linha_cruza_circulo(rota["geometria"]["coordinates"], z["lat"], z["lng"], z["raio_m"]), \
            f"rota cruza a zona {z['id']}"
    assert rota["zonas_cruzadas"] == []
    # se não veio do ORS, a tela precisa avisar que o desvio automático não está valendo
    if rota["provedor"] != "openrouteservice":
        assert any("Desvio automático indisponível" in a for a in d["avisos"]), d["avisos"]
    assert "acima_do_risco_m" in destino, d["avisos"]
    assert not any("Altitude indisponível" in a for a in d["avisos"]), d["avisos"]
    assert rota["passos"] and rota["distancia_m"] > 0 and rota["duracao_s"] > 0
    assert len(rota["geometria"]["coordinates"]) >= 2
    if "acima_do_risco_m" in destino:
        assert destino["acima_do_risco_m"] >= 0 or any("Não é possível avaliar a segurança" in a for a in d["avisos"])


@pytest.fixture(scope="module")
def zonas_reais():
    zonas = httpx.get(f"{SERVICO}/zonas-risco", timeout=30).json()
    assert any(z["lat"] == ZONA_CENTRO["lat"] and z["lng"] == ZONA_CENTRO["lng"] for z in zonas), \
        "cadastre o ponto de teste no HydroTech antes"
    return zonas


def test_status_usa_openrouteservice():
    assert httpx.get(f"{SERVICO}/status").json()["desvio_de_zonas"] == "openrouteservice"


def test_openrouteservice_desvia_de_verdade(zonas_reais):
    # Sem cota no ORS o teste é pulado, e não marcado como aprovado
    lat, lng = geo.deslocar(ZONA_CENTRO["lat"], ZONA_CENTRO["lng"], 90, 380)
    d = pedir(lat, lng)[0].json()
    if d["rota"]["provedor"] != "openrouteservice":
        pytest.skip("cota diária do OpenRouteService esgotada: " + "; ".join(d["avisos"]))
    conferir_rota_segura(d, zonas_reais)


def test_dez_pessoas_ao_mesmo_tempo(zonas_reais):
    random.seed(3)
    pessoas = [geo.deslocar(ZONA_CENTRO["lat"], ZONA_CENTRO["lng"], random.uniform(0, 360), random.uniform(0, 1500))
               for _ in range(10)]

    async def todos():
        async with httpx.AsyncClient(timeout=90) as c:
            async def um(lat, lng):
                inicio = time.monotonic()
                r = await c.get(f"{SERVICO}/rota-fuga", params={"lat": lat, "lng": lng})
                return r, time.monotonic() - inicio
            return await asyncio.gather(*(um(*p) for p in pessoas))

    resultados = asyncio.run(todos())
    for r, _ in resultados:
        assert r.status_code == 200, r.text
        conferir_rota_segura(r.json(), zonas_reais)
    tempos = sorted(t for _, t in resultados)
    assert tempos[len(tempos) // 2] < 15, tempos  # mediana


@pytest.mark.parametrize("rumo", [0, 45, 90, 135, 180, 225, 270, 315])
def test_em_volta_da_zona(rumo, zonas_reais):
    # pessoa a 80 m da borda da zona, em 8 direções
    lat, lng = geo.deslocar(ZONA_CENTRO["lat"], ZONA_CENTRO["lng"], rumo, 380)
    r, segundos = pedir(lat, lng)
    assert r.status_code == 200, r.text
    d = r.json()
    assert d["dentro_de_zona_risco"] is False
    conferir_rota_segura(d, zonas_reais)
    assert segundos < 20


@pytest.mark.parametrize("rumo,dist", [(0, 0), (90, 150), (225, 250)])
def test_dentro_da_zona(rumo, dist, zonas_reais):
    lat, lng = geo.deslocar(ZONA_CENTRO["lat"], ZONA_CENTRO["lng"], rumo, dist)
    r, _ = pedir(lat, lng)
    assert r.status_code == 200, r.text
    d = r.json()
    assert d["dentro_de_zona_risco"] is True
    assert d["avisos"][0].startswith("Você está DENTRO")
    conferir_rota_segura(d, zonas_reais)


def test_de_carro(zonas_reais):
    r, _ = pedir(-22.9056, -47.0540, "carro")
    assert r.status_code == 200, r.text
    d = r.json()
    assert "travelmode=driving" in d["links"]["google_maps"]
    conferir_rota_segura(d, zonas_reais)


def test_cidade_sem_zona_por_perto():
    r, _ = pedir(-23.5505, -46.6333)  # São Paulo, longe de qualquer zona de teste
    assert r.status_code == 200, r.text
    d = r.json()
    assert d["zonas_risco"] == []
    assert d["rota"]["passos"]


def test_nome_do_destino_e_links(zonas_reais):
    d = pedir(-22.9010, -47.0584)[0].json()
    if d["destino"].get("endereco") is None:
        pytest.skip("Nominatim recusando pedidos agora (o nome da rua é opcional)")
    assert d["destino"]["endereco"]
    assert d["links"]["google_maps"].startswith("https://www.google.com/maps/dir/?api=1")
    assert d["links"]["waze"].startswith("https://waze.com/ul?ll=")


def test_cors_para_o_frontend_do_hydrotech():
    r = httpx.get(f"{SERVICO}/zonas-risco", headers={"Origin": "http://localhost:5173"})
    assert r.headers.get("access-control-allow-origin") == "*"


def test_parametro_invalido_ao_vivo():
    assert httpx.get(f"{SERVICO}/rota-fuga", params={"lat": 200, "lng": 0}).status_code == 422
