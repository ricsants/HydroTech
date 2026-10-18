"""
Escolhe para onde a pessoa vai. O HydroTech não tem abrigos cadastrados, então testamos pontos
em volta dela e ficamos com o mais seguro que dá para alcançar.
"""
from . import config, geo
from .altitude import altitudes

DIRECOES = 16
DISTANCIAS_M = (500, 1000, 1500, 2000)
DISTANCIAS_EXTRAS_M = (2500, 3000, 4000, 5000)  # só quando os anéis perto estão todos em risco

# Pesos da nota. Ajuste aqui se quiser rotas mais curtas (aumente PESO_CAMINHADA)
PESO_ALTITUDE = 1.5      # 1,5 ponto a cada 30 m acima do rio (conta de -20 m a +30 m)
PESO_LONGE_RISCO = 1.0   # 1 ponto quando fica a 1,5 km ou mais da borda da zona
PESO_CAMINHADA = 0.8     # perde 0,8 ponto a cada 2 km de distância


def _distancia_da_borda(lat, lng, zonas):
    """Negativa quando o ponto está dentro de alguma zona."""
    if not zonas:
        return float("inf")
    return min(geo.distancia_m(lat, lng, z["lat"], z["lng"]) - z["raio_m"] for z in zonas)


def _zona_mais_proxima(lat, lng, zonas):
    return min(zonas, key=lambda z: geo.distancia_m(lat, lng, z["lat"], z["lng"])) if zonas else None


def nota(candidato):
    ganho = max(-20.0, min(30.0, candidato.get("acima_do_risco_m") or 0.0))
    longe = min(candidato["distancia_risco_m"], 1500.0) / 1500.0
    caminhada = candidato["distancia_linha_reta_m"] / 2000.0
    return ganho / 30.0 * PESO_ALTITUDE + longe * PESO_LONGE_RISCO - caminhada * PESO_CAMINHADA


def gerar_candidatos(lat, lng, zonas, distancias):
    candidatos = []
    for i in range(DIRECOES):
        for dist in distancias:
            clat, clng = geo.deslocar(lat, lng, 360 * i / DIRECOES, dist)
            borda = _distancia_da_borda(clat, clng, zonas)
            if borda >= config.MARGEM_DESTINO_M:
                candidatos.append({
                    "lat": clat,
                    "lng": clng,
                    "distancia_linha_reta_m": dist,
                    "distancia_risco_m": min(borda, 99999.0),
                })
    return candidatos


async def area_mais_segura(lat, lng, zonas):
    """Candidatos do melhor para o pior, mais os avisos que a pessoa precisa ver."""
    avisos = []
    candidatos = gerar_candidatos(lat, lng, zonas, DISTANCIAS_M)
    if not candidatos:
        candidatos = gerar_candidatos(lat, lng, zonas, DISTANCIAS_EXTRAS_M)
        if candidatos:
            avisos.append("A área de risco simulada é extensa; o destino estimado fica mais distante.")
    if not candidatos:
        return [], avisos

    # A altitude do rio é a do ponto de risco mais próximo (sem zona, a da própria pessoa)
    zona = _zona_mais_proxima(lat, lng, zonas)
    referencia = (zona["lat"], zona["lng"]) if zona else (lat, lng)
    alts = await altitudes([referencia] + [(c["lat"], c["lng"]) for c in candidatos])

    if alts and alts[0] is not None:
        for c, alt in zip(candidatos, alts[1:]):
            if alt is not None:
                c["altitude_m"] = alt
                c["acima_do_risco_m"] = round(alt - alts[0], 1)

    com_altitude = [c for c in candidatos if "acima_do_risco_m" in c]
    if not com_altitude:
        avisos.append("Altitude indisponível agora; a escolha considerou só a distância das áreas de risco.")
    else:
        acima_do_rio = [c for c in com_altitude if c["acima_do_risco_m"] >= 0]
        if acima_do_rio:
            candidatos = acima_do_rio
        else:
            candidatos = com_altitude
            avisos.append("Não foi encontrado terreno estimado mais alto que o ponto de referência. Não é possível avaliar a segurança do destino.")

    for c in candidatos:
        c.update(nome="Destino estimado", tipo="Ponto de demonstração", nota=round(nota(c), 3))
    candidatos.sort(key=lambda c: c["nota"], reverse=True)
    return candidatos, avisos
