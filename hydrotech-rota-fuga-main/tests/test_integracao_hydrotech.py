"""
Fluxo completo com o HydroTech de verdade, pela API (o mesmo caminho das telas):
admin cria o rio e o ponto de risco -> o serviço passa a ver a zona -> o link do alerta
mostra só essa zona -> sai uma rota segura.

Precisa do HydroTech e deste serviço rodando, e de um usuário da Defesa Civil para criar o rio:
    HYDROTECH_ADMIN_EMAIL=... HYDROTECH_ADMIN_SENHA=... pytest --ao-vivo tests/test_integracao_hydrotech.py
O rio de teste é apagado no final.
"""
import os
import time
import uuid

import httpx
import pytest

from app import config, geo

pytestmark = pytest.mark.ao_vivo
HYDROTECH = config.HYDROTECH_API_URL
SERVICO = "http://127.0.0.1:8100"
PONTO = (-22.8160, -47.0700)  # Barão Geraldo, longe dos pontos de teste do centro


@pytest.fixture(scope="module")
def admin():
    email, senha = os.getenv("HYDROTECH_ADMIN_EMAIL"), os.getenv("HYDROTECH_ADMIN_SENHA")
    if not email or not senha:
        pytest.skip("defina HYDROTECH_ADMIN_EMAIL e HYDROTECH_ADMIN_SENHA para rodar a integração")
    r = httpx.post(f"{HYDROTECH}/auth/login/", json={"email": email, "senha": senha})
    assert r.status_code == 200, f"login falhou: {r.text}"
    return {"Authorization": f"Bearer {r.json()['access']}"}


@pytest.fixture(scope="module")
def ponto_em_alerta(admin):
    nome = f"Rio Teste Integração {uuid.uuid4().hex[:6]}"
    rio = httpx.post(f"{HYDROTECH}/rios/", headers=admin, json={"nome": nome, "cidade": "Campinas", "estado": "SP"})
    assert rio.status_code == 201, rio.text
    rio = rio.json()
    try:
        ponto = httpx.post(f"{HYDROTECH}/rios/{rio['id']}/pontos-risco/", headers=admin, json={
            "rio": rio["id"], "descricao": "Ponte de teste da integração",
            "latitude": PONTO[0], "longitude": PONTO[1],
            "nivel_base": 1.0, "limite_atencao": 1.5, "limite_alerta": 2.5, "limite_emergencia": 3.5,
        })
        assert ponto.status_code == 201, ponto.text
        yield {"rio": rio, "ponto": ponto.json()}
    finally:
        httpx.delete(f"{HYDROTECH}/rios/{rio['id']}/", headers=admin)  # o ponto vai junto


def test_ponto_aparece_na_api_publica(ponto_em_alerta):
    pontos = httpx.get(f"{HYDROTECH}/publico/rios/{ponto_em_alerta['rio']['id']}/pontos-risco/").json()
    assert [p["id"] for p in pontos] == [ponto_em_alerta["ponto"]["id"]]


def test_servico_passa_a_ver_a_zona_nova(ponto_em_alerta):
    pid = ponto_em_alerta["ponto"]["id"]
    # as zonas ficam em cache por CACHE_ZONAS_S, então pode levar um pouco
    prazo = time.monotonic() + config.CACHE_ZONAS_S + 15
    while time.monotonic() < prazo:
        zonas = httpx.get(f"{SERVICO}/zonas-risco", params={"alerta": pid}).json()
        if [z["id"] for z in zonas] == [pid]:
            break
        time.sleep(3)
    assert [z["id"] for z in zonas] == [pid], "a zona nova não apareceu no serviço"
    assert zonas[0]["rio"] == ponto_em_alerta["rio"]["nome"]


def test_link_do_alerta_da_rota_so_para_a_zona_dele(ponto_em_alerta):
    pid = ponto_em_alerta["ponto"]["id"]
    lat, lng = geo.deslocar(*PONTO, 45, 100)  # 100 m do ponto, dentro da zona
    r = httpx.get(f"{SERVICO}/rota-fuga", params={"lat": lat, "lng": lng, "alerta": pid}, timeout=60)
    assert r.status_code == 200, r.text
    d = r.json()
    assert [z["id"] for z in d["zonas_risco"]] == [pid]
    assert d["dentro_de_zona_risco"] is True
    assert d["avisos"][0].startswith("Você está DENTRO")
    borda = geo.distancia_m(d["destino"]["lat"], d["destino"]["lng"], *PONTO) - config.RAIO_ZONA_RISCO_M
    assert borda >= config.MARGEM_DESTINO_M - 1
    assert d["links"]["google_maps"] and d["links"]["waze"]
    if d["rota"]:
        assert d["rota"]["passos"] and d["rota"]["distancia_m"] > 0


def test_sem_alerta_considera_todas_as_zonas(ponto_em_alerta):
    zonas = httpx.get(f"{SERVICO}/zonas-risco").json()
    assert ponto_em_alerta["ponto"]["id"] in [z["id"] for z in zonas] and len(zonas) >= 2


def test_link_antigo_de_ponto_apagado_evita_todas():
    r = httpx.get(f"{SERVICO}/rota-fuga", params={"lat": PONTO[0], "lng": PONTO[1], "alerta": 999999}, timeout=60)
    assert r.status_code == 200
    assert any("não foi encontrado" in a for a in r.json()["avisos"])
