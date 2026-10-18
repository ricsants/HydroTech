"""Contas de geografia em metros. Coordenadas como (lat, lng), exceto onde diz GeoJSON."""
import math

RAIO_TERRA_M = 6_371_000.0


def distancia_m(lat1, lng1, lat2, lng2):
    """Haversine."""
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng / 2) ** 2)
    return 2 * RAIO_TERRA_M * math.asin(math.sqrt(a))


def deslocar(lat, lng, rumo_graus, distancia):
    """Ponto a `distancia` metros na direção `rumo_graus` (0 = norte, 90 = leste)."""
    d = distancia / RAIO_TERRA_M
    rumo = math.radians(rumo_graus)
    lat1, lng1 = math.radians(lat), math.radians(lng)
    lat2 = math.asin(math.sin(lat1) * math.cos(d) + math.cos(lat1) * math.sin(d) * math.cos(rumo))
    lng2 = lng1 + math.atan2(math.sin(rumo) * math.sin(d) * math.cos(lat1),
                             math.cos(d) - math.sin(lat1) * math.sin(lat2))
    return math.degrees(lat2), math.degrees(lng2)


def rumo(lat1, lng1, lat2, lng2):
    """Direção de 1 para 2, em graus (0 = norte)."""
    lat1, lat2 = math.radians(lat1), math.radians(lat2)
    dlng = math.radians(lng2 - lng1)
    x = math.sin(dlng) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlng)
    return (math.degrees(math.atan2(x, y)) + 360) % 360


def circulo_poligono(lat, lng, raio_m, vertices=24):
    """Anel GeoJSON ([lng, lat]) fechado, aproximando um círculo."""
    anel = []
    for i in range(vertices):
        plat, plng = deslocar(lat, lng, 360 * i / vertices, raio_m)
        anel.append([round(plng, 6), round(plat, 6)])
    anel.append(anel[0])
    return anel


def _distancia_ponto_segmento_m(plat, plng, alat, alng, blat, blng):
    # Projeção plana local; para trechos de rua o erro é desprezível
    k = math.cos(math.radians(plat))
    ax, ay = (alng - plng) * k, alat - plat
    bx, by = (blng - plng) * k, blat - plat
    dx, dy = bx - ax, by - ay
    comp2 = dx * dx + dy * dy
    t = 0.0 if comp2 == 0 else max(0.0, min(1.0, -(ax * dx + ay * dy) / comp2))
    cx, cy = ax + t * dx, ay + t * dy
    return math.hypot(cx, cy) * (math.pi / 180) * RAIO_TERRA_M


def linha_cruza_circulo(coords_lnglat, lat, lng, raio_m):
    """Se a linha GeoJSON ([lng, lat]) passa a menos de raio_m do centro."""
    for (alng, alat), (blng, blat) in zip(coords_lnglat, coords_lnglat[1:]):
        if _distancia_ponto_segmento_m(lat, lng, alat, alng, blat, blng) < raio_m:
            return True
    return False
