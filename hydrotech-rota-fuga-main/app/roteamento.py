"""
Rota até o destino. O OpenRouteService desvia das zonas de verdade (avoid_polygons);
o OSRM público é a reserva, sem desvio: só escolhemos a alternativa que não cruza zona.
"""
import asyncio
import logging
import time

import httpx

from . import config, geo

logger = logging.getLogger(__name__)

# Quando a cota diária do ORS acaba ele responde 403 para tudo, e quando o OSRM público cai
# cada pedido fica esperando o timeout. Nos dois casos paramos de chamar por um tempo.
PAUSA_ORS_SEM_COTA_S = 600
PAUSA_OSRM_FORA_S = 60
_pausas = {"ors": 0.0, "osrm": 0.0}

MANOBRAS = {
    "left": "à esquerda", "right": "à direita",
    "slight left": "levemente à esquerda", "slight right": "levemente à direita",
    "sharp left": "fortemente à esquerda", "sharp right": "fortemente à direita",
    "straight": "em frente", "uturn": "fazendo retorno",
}


class RotaIndisponivel(Exception):
    pass


def _pausar(servico, segundos):
    _pausas[servico] = time.monotonic() + segundos


def _pausado(servico):
    return time.monotonic() < _pausas[servico]


def ors_disponivel():
    return bool(config.ORS_API_KEY) and not _pausado("ors")


def zonas_cruzadas(coords, zonas):
    return [z["id"] for z in zonas if geo.linha_cruza_circulo(coords, z["lat"], z["lng"], z["raio_m"])]


async def _rota_ors(origem, destino, modo, zonas):
    corpo = {
        "coordinates": [[origem[1], origem[0]], [destino[1], destino[0]]],
        "language": "pt",
        "instructions": True,
        "units": "m",
    }
    if zonas:
        corpo["options"] = {"avoid_polygons": {
            "type": "MultiPolygon",
            "coordinates": [[geo.circulo_poligono(z["lat"], z["lng"], z["raio_m"])] for z in zonas],
        }}
    url = f"https://api.openrouteservice.org/v2/directions/{config.ORS_PERFIS[modo]}/geojson"

    async with httpx.AsyncClient(timeout=config.TIMEOUT_ROTA_S) as cliente:
        for espera in (1.2, 2.5, None):
            resp = await cliente.post(url, json=corpo, headers={"Authorization": config.ORS_API_KEY})
            # 429 é o limite por minuto: vale esperar um pouco antes de cair para o OSRM
            if resp.status_code != 429 or espera is None:
                break
            await asyncio.sleep(espera)

    if resp.status_code == 403 and "quota" in resp.text.lower():
        _pausar("ors", PAUSA_ORS_SEM_COTA_S)
        logger.warning("Cota do ORS acabou, usando só OSRM pelos próximos %s min", PAUSA_ORS_SEM_COTA_S // 60)
    if resp.status_code != 200:
        raise RotaIndisponivel(f"OpenRouteService {resp.status_code}: {resp.text[:200]}")

    feature = resp.json()["features"][0]
    resumo = feature["properties"].get("summary", {})
    return {
        "provedor": "openrouteservice",
        "desvia_zonas": True,
        "geometria": {"type": "LineString", "coordinates": feature["geometry"]["coordinates"]},
        "distancia_m": round(resumo.get("distance", 0)),
        "duracao_s": round(resumo.get("duration", 0)),
        "passos": [
            {"instrucao": p["instruction"], "distancia_m": round(p.get("distance", 0))}
            for seg in feature["properties"].get("segments", [])
            for p in seg.get("steps", [])
        ],
    }


def instrucao_osrm(passo):
    """O OSRM devolve a manobra em códigos em inglês; aqui vira frase em português."""
    m = passo.get("maneuver", {})
    tipo, modificador = m.get("type"), m.get("modifier", "")
    rua = passo.get("name") or ""
    na_rua = f" na {rua}" if rua else ""
    if tipo == "depart":
        return f"Siga{na_rua}" if rua else "Comece a seguir"
    if tipo == "arrive":
        return "Você chegou ao destino estimado da simulação"
    if tipo in ("roundabout", "rotary"):
        saida = m.get("exit")
        return f"Na rotatória, pegue a {saida}ª saída{na_rua}" if saida else f"Entre na rotatória{na_rua}"
    if modificador == "straight" or tipo in ("new name", "continue"):
        return f"Continue em frente{na_rua}"
    if modificador == "uturn":
        return f"Faça o retorno{na_rua}"
    if modificador in MANOBRAS:
        return f"Vire {MANOBRAS[modificador]}{na_rua}"
    return f"Siga{na_rua}"


async def _rota_osrm(origem, destino, modo, zonas):
    url = f"{config.OSRM_URLS[modo]}/{origem[1]},{origem[0]};{destino[1]},{destino[0]}"
    params = {"overview": "full", "geometries": "geojson", "steps": "true", "alternatives": "true"}
    async with httpx.AsyncClient(timeout=config.TIMEOUT_ROTA_S, headers={"User-Agent": config.USER_AGENT}) as cliente:
        resp = await cliente.get(url, params=params)
    if resp.status_code != 200 or resp.json().get("code") != "Ok":
        raise RotaIndisponivel(f"OSRM {resp.status_code}: {resp.text[:200]}")

    # Sem desvio de verdade, o melhor que dá é pegar a alternativa que não passa por zona
    rotas = resp.json()["routes"]
    rotas.sort(key=lambda r: (len(zonas_cruzadas(r["geometry"]["coordinates"], zonas)), r["duration"]))
    rota = rotas[0]
    return {
        "provedor": "osrm",
        "desvia_zonas": False,
        "geometria": rota["geometry"],
        "distancia_m": round(rota["distance"]),
        "duracao_s": round(rota["duration"]),
        "passos": [
            {"instrucao": instrucao_osrm(p), "distancia_m": round(p.get("distance", 0))}
            for perna in rota["legs"] for p in perna["steps"]
        ],
    }


async def _rota_osrm_com_pausa(origem, destino, modo, zonas):
    if _pausado("osrm"):
        raise RotaIndisponivel("OSRM em pausa (caiu há pouco)")
    for tentativa in range(2):
        try:
            return await _rota_osrm(origem, destino, modo, zonas)
        except httpx.TimeoutException as erro:
            # Timeout não melhora tentando de novo na hora, só faz a pessoa esperar mais
            _pausar("osrm", PAUSA_OSRM_FORA_S)
            logger.warning("OSRM não respondeu, pausando por %s s", PAUSA_OSRM_FORA_S)
            raise RotaIndisponivel("OSRM não respondeu a tempo") from erro
        except (RotaIndisponivel, httpx.HTTPError) as erro:
            logger.warning("OSRM falhou (tentativa %s): %s", tentativa + 1, erro)
            if tentativa == 1:
                _pausar("osrm", PAUSA_OSRM_FORA_S)
                raise RotaIndisponivel(str(erro)) from erro


async def calcular_rota(origem, destino, modo, zonas):
    """origem e destino em (lat, lng)."""
    rota = None
    if ors_disponivel():
        try:
            rota = await _rota_ors(origem, destino, modo, zonas)
        except (RotaIndisponivel, httpx.HTTPError, KeyError, IndexError) as erro:
            logger.warning("ORS falhou, indo para o OSRM: %s", erro)
    if rota is None:
        rota = await _rota_osrm_com_pausa(origem, destino, modo, zonas)
    rota["zonas_cruzadas"] = zonas_cruzadas(rota["geometria"]["coordinates"], zonas)
    return rota
