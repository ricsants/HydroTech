from app import altitude, config, destinos, geo
from tests.conftest import ZONA_CENTRO, rodar

ORIGEM = (-22.9056, -47.0620)  # uns 370 m a oeste do centro da zona


def terreno_por_lado(alt_rio=600.0, alt_leste=620.0, alt_oeste=590.0):
    """Primeiro valor é o rio; a leste da origem o terreno é alto, a oeste é baixo."""
    async def falso(pontos):
        return [alt_rio] + [alt_leste if lng > ORIGEM[1] else alt_oeste for _, lng in pontos[1:]]
    return falso


def terreno_plano(alt=600.0):
    async def falso(pontos):
        return [alt] * len(pontos)
    return falso


def test_candidatos_ficam_fora_das_zonas_com_margem(monkeypatch):
    monkeypatch.setattr(destinos, "altitudes", terreno_por_lado())
    candidatos, _ = rodar(destinos.area_mais_segura(*ORIGEM, [ZONA_CENTRO]))
    assert candidatos
    for c in candidatos:
        borda = geo.distancia_m(c["lat"], c["lng"], ZONA_CENTRO["lat"], ZONA_CENTRO["lng"]) - ZONA_CENTRO["raio_m"]
        assert borda >= config.MARGEM_DESTINO_M


def test_descarta_pontos_mais_baixos_que_o_rio(monkeypatch):
    monkeypatch.setattr(destinos, "altitudes", terreno_por_lado())
    candidatos, avisos = rodar(destinos.area_mais_segura(*ORIGEM, [ZONA_CENTRO]))
    assert all(c["acima_do_risco_m"] >= 0 for c in candidatos)
    assert all(c["lng"] > ORIGEM[1] for c in candidatos)
    assert avisos == []


def test_ordena_pela_nota(monkeypatch):
    monkeypatch.setattr(destinos, "altitudes", terreno_por_lado())
    candidatos, _ = rodar(destinos.area_mais_segura(*ORIGEM, [ZONA_CENTRO]))
    notas = [c["nota"] for c in candidatos]
    assert notas == sorted(notas, reverse=True)


def test_terreno_plano_sem_zona_prefere_o_mais_perto(monkeypatch):
    monkeypatch.setattr(destinos, "altitudes", terreno_plano())
    candidatos, _ = rodar(destinos.area_mais_segura(*ORIGEM, []))
    assert candidatos[0]["distancia_linha_reta_m"] == min(destinos.DISTANCIAS_M)


def test_tudo_mais_baixo_que_o_rio_avisa_e_mantem_candidatos(monkeypatch):
    monkeypatch.setattr(destinos, "altitudes", terreno_por_lado(alt_rio=700, alt_leste=650, alt_oeste=650))
    candidatos, avisos = rodar(destinos.area_mais_segura(*ORIGEM, [ZONA_CENTRO]))
    assert candidatos
    assert any("Não é possível avaliar a segurança" in a for a in avisos)


def test_sem_altitude_avisa_e_decide_pela_distancia(monkeypatch):
    async def fora_do_ar(pontos):
        return None
    monkeypatch.setattr(destinos, "altitudes", fora_do_ar)
    candidatos, avisos = rodar(destinos.area_mais_segura(*ORIGEM, [ZONA_CENTRO]))
    assert candidatos
    assert any("Altitude indisponível" in a for a in avisos)


def test_altitude_faltando_em_alguns_pontos(monkeypatch):
    async def com_buracos(pontos):
        return [600.0] + [None if i % 3 == 0 else 610.0 for i in range(len(pontos) - 1)]
    monkeypatch.setattr(destinos, "altitudes", com_buracos)
    candidatos, _ = rodar(destinos.area_mais_segura(*ORIGEM, [ZONA_CENTRO]))
    assert candidatos
    assert all(c.get("acima_do_risco_m") is not None for c in candidatos)


def test_altitude_faltando_no_rio(monkeypatch):
    async def sem_rio(pontos):
        return [None] + [610.0] * (len(pontos) - 1)
    monkeypatch.setattr(destinos, "altitudes", sem_rio)
    candidatos, avisos = rodar(destinos.area_mais_segura(*ORIGEM, [ZONA_CENTRO]))
    assert candidatos
    assert any("Altitude indisponível" in a for a in avisos)


def test_zona_grande_faz_procurar_mais_longe(monkeypatch):
    monkeypatch.setattr(destinos, "altitudes", terreno_plano())
    zona_grande = {**ZONA_CENTRO, "lat": ORIGEM[0], "lng": ORIGEM[1], "raio_m": 2100.0}
    candidatos, avisos = rodar(destinos.area_mais_segura(*ORIGEM, [zona_grande]))
    assert candidatos
    assert any("extensa" in a for a in avisos)
    for c in candidatos:
        assert geo.distancia_m(c["lat"], c["lng"], *ORIGEM) - 2100 >= config.MARGEM_DESTINO_M


def test_candidatos_caem_na_grade_pre_carregada():
    """Se isso quebrar, a pré-carga de altitude deixa de servir para as rotas de verdade."""
    grade = set(altitude.grade_em_volta(ZONA_CENTRO["lat"], ZONA_CENTRO["lng"], config.RAIO_PREAQUECER_ALTITUDE_M))
    pessoa = geo.deslocar(ZONA_CENTRO["lat"], ZONA_CENTRO["lng"], 60, 1400)
    candidatos = destinos.gerar_candidatos(*pessoa, [ZONA_CENTRO], destinos.DISTANCIAS_M)
    chaves = [altitude.chave(c["lat"], c["lng"]) for c in candidatos]
    chaves.append(altitude.chave(ZONA_CENTRO["lat"], ZONA_CENTRO["lng"]))
    assert sum(k in grade for k in chaves) / len(chaves) > 0.9
