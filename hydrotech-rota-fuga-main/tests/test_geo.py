import pytest

from app import geo


def test_distancia_um_grau_de_latitude():
    assert geo.distancia_m(0, 0, 1, 0) == pytest.approx(111_195, rel=1e-3)


def test_distancia_zero():
    assert geo.distancia_m(-22.9, -47.06, -22.9, -47.06) == 0


@pytest.mark.parametrize("rumo", [0, 45, 90, 180, 270, 333])
@pytest.mark.parametrize("dist", [100, 1000, 2000])
def test_deslocar_mantem_distancia_e_rumo(rumo, dist):
    lat, lng = geo.deslocar(-22.9056, -47.0584, rumo, dist)
    assert geo.distancia_m(-22.9056, -47.0584, lat, lng) == pytest.approx(dist, rel=1e-3)
    assert geo.rumo(-22.9056, -47.0584, lat, lng) == pytest.approx(rumo, abs=0.5)


def test_circulo_fechado_e_no_raio():
    anel = geo.circulo_poligono(-22.9056, -47.0584, 300, vertices=24)
    assert len(anel) == 25
    assert anel[0] == anel[-1]
    for lng, lat in anel:
        assert geo.distancia_m(-22.9056, -47.0584, lat, lng) == pytest.approx(300, abs=1)


def test_linha_que_passa_longe_nao_cruza():
    linha = [[-47.07, -22.92], [-47.06, -22.92]]  # ~1,6 km ao sul
    assert not geo.linha_cruza_circulo(linha, -22.9056, -47.0584, 300)


def test_segmento_longo_cruza_mesmo_com_pontas_fora():
    # As duas pontas ficam a ~1 km, mas o segmento atravessa o centro da zona
    linha = [[-47.068, -22.9056], [-47.048, -22.9056]]
    assert geo.linha_cruza_circulo(linha, -22.9056, -47.0584, 300)


def test_linha_tangente_fora_do_raio():
    lat_norte, _ = geo.deslocar(-22.9056, -47.0584, 0, 350)
    linha = [[-47.07, lat_norte], [-47.05, lat_norte]]
    assert not geo.linha_cruza_circulo(linha, -22.9056, -47.0584, 300)
    assert geo.linha_cruza_circulo(linha, -22.9056, -47.0584, 400)


def test_linha_com_um_ponto_so():
    assert not geo.linha_cruza_circulo([[-47.0584, -22.9056]], -22.9056, -47.0584, 300)
