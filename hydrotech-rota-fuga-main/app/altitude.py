"""Altitude do terreno: Open-Meteo, com OpenTopoData de reserva e cache em memória/disco."""
import asyncio
import json
import logging
import math
from pathlib import Path

import httpx

from . import config, geo

logger = logging.getLogger(__name__)

# Grade de ~100 m. O modelo de terreno das duas APIs tem ~90 m de resolução,
# então arredondar a coordenada não perde nada e deixa vizinhos dividirem o cache.
PASSO_GRADE = 0.001
LOTE_MAXIMO = 100  # as duas APIs aceitam até 100 pontos por chamada
ARQUIVO_CACHE = Path(__file__).resolve().parent.parent / "cache" / "altitudes.json"
ERROS_DE_FONTE = (httpx.HTTPError, KeyError, ValueError, TypeError)

_cache = {}


def chave(lat, lng):
    return round(lat, 3), round(lng, 3)


def carregar_do_disco():
    try:
        dados = json.loads(ARQUIVO_CACHE.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        return 0
    for texto, alt in dados.items():
        lat, lng = texto.split(",")
        _cache[(float(lat), float(lng))] = alt
    return len(dados)


def _salvar_no_disco():
    ARQUIVO_CACHE.parent.mkdir(exist_ok=True)
    dados = {f"{lat},{lng}": alt for (lat, lng), alt in _cache.items()}
    ARQUIVO_CACHE.write_text(json.dumps(dados), encoding="utf-8")


async def _open_meteo(chaves):
    async with httpx.AsyncClient(timeout=15) as cliente:
        for tentativa in range(2):
            resp = await cliente.get("https://api.open-meteo.com/v1/elevation", params={
                "latitude": ",".join(f"{lat:.3f}" for lat, _ in chaves),
                "longitude": ",".join(f"{lng:.3f}" for _, lng in chaves),
            })
            # 429 é o limite por minuto; uma segunda tentativa costuma passar
            if resp.status_code == 429 and tentativa == 0:
                await asyncio.sleep(1.5)
                continue
            resp.raise_for_status()
            return resp.json()["elevation"]


async def _opentopodata(chaves):
    async with httpx.AsyncClient(timeout=15) as cliente:
        resp = await cliente.get("https://api.opentopodata.org/v1/srtm90m", params={
            "locations": "|".join(f"{lat:.3f},{lng:.3f}" for lat, lng in chaves),
        })
        resp.raise_for_status()
        return [r["elevation"] for r in resp.json()["results"]]


async def _buscar_lote(chaves):
    """Altitudes de até 100 pontos. Levanta erro se as duas fontes falharem."""
    try:
        return await _open_meteo(chaves)
    except ERROS_DE_FONTE as erro:
        logger.warning("Open-Meteo falhou (%s), tentando OpenTopoData", erro)
        return await _opentopodata(chaves)


def _guardar(chaves, valores):
    novos = 0
    for k, alt in zip(chaves, valores):
        if alt is not None:
            _cache[k] = alt
            novos += 1
    return novos


async def altitudes(pontos):
    """Altitude de cada (lat, lng). Devolve None se nenhuma fonte responder."""
    if not pontos:
        return []
    chaves = [chave(lat, lng) for lat, lng in pontos]
    faltando = list(dict.fromkeys(k for k in chaves if k not in _cache))
    for i in range(0, len(faltando), LOTE_MAXIMO):
        lote = faltando[i:i + LOTE_MAXIMO]
        try:
            _guardar(lote, await _buscar_lote(lote))
        except ERROS_DE_FONTE as erro:
            logger.warning("Sem altitude agora: %s", erro)
            return None
    return [_cache.get(k) for k in chaves]


def grade_em_volta(lat, lng, raio_m):
    passos_lat = int(raio_m / 111_000 / PASSO_GRADE) + 1
    passos_lng = int(raio_m / (111_000 * math.cos(math.radians(lat))) / PASSO_GRADE) + 1
    centro_lat, centro_lng = chave(lat, lng)
    for i in range(-passos_lat, passos_lat + 1):
        for j in range(-passos_lng, passos_lng + 1):
            celula = (round(centro_lat + i * PASSO_GRADE, 3), round(centro_lng + j * PASSO_GRADE, 3))
            if geo.distancia_m(lat, lng, *celula) <= raio_m:
                yield celula


async def preaquecer(zonas, pausa_s=2.0):
    """
    Baixa com calma a altitude da região em volta das zonas de risco. Quando o alerta sai,
    muita gente pede rota ao mesmo tempo e as APIs grátis começam a recusar; com o cache
    pronto a rota nem precisa delas.
    """
    faltando = []
    for z in zonas:
        faltando += [c for c in grade_em_volta(z["lat"], z["lng"], config.RAIO_PREAQUECER_ALTITUDE_M)
                     if c not in _cache]
    faltando = list(dict.fromkeys(faltando))[:config.MAX_PONTOS_PREAQUECER]
    if not faltando:
        return 0

    logger.info("Pré-carregando altitude de %s pontos", len(faltando))
    carregados = 0
    for i in range(0, len(faltando), LOTE_MAXIMO):
        lote = faltando[i:i + LOTE_MAXIMO]
        try:
            carregados += _guardar(lote, await _buscar_lote(lote))
        except ERROS_DE_FONTE as erro:
            logger.warning("Pré-carga interrompida: %s", erro)
            break
        _salvar_no_disco()
        await asyncio.sleep(pausa_s)
    logger.info("Pré-carga terminou: %s pontos", carregados)
    return carregados
