"""Rua e bairro de um ponto, pelo Nominatim (OpenStreetMap)."""
import asyncio
import logging
import time

import httpx

from . import config

logger = logging.getLogger(__name__)

_cache = {}
# O Nominatim público aceita no máximo 1 pedido por segundo; passar disso bloqueia o IP
_fila = asyncio.Lock()
_ultimo_pedido = {"quando": 0.0}


async def _pedir(lat, lng):
    async with httpx.AsyncClient(timeout=10, headers={"User-Agent": config.USER_AGENT}) as cliente:
        resp = await cliente.get("https://nominatim.openstreetmap.org/reverse", params={
            "lat": lat, "lon": lng, "zoom": 17, "addressdetails": 1,
            "format": "jsonv2", "accept-language": "pt-BR",
        })
        resp.raise_for_status()
        end = resp.json().get("address", {})
    partes = [end.get("road"), end.get("suburb") or end.get("neighbourhood") or end.get("city_district")]
    return ", ".join(p for p in partes if p) or None


async def _pedir_na_fila(lat, lng):
    async with _fila:
        espera = 1.1 - (time.monotonic() - _ultimo_pedido["quando"])
        if espera > 0:
            await asyncio.sleep(espera)
        _ultimo_pedido["quando"] = time.monotonic()
        return await _pedir(lat, lng)


async def nome_do_local(lat, lng, limite_s=2.5):
    """O nome é só um detalhe: se demorar ou falhar, a rota sai sem ele."""
    k = (round(lat, 4), round(lng, 4))
    if k in _cache:
        return _cache[k]
    try:
        nome = await asyncio.wait_for(_pedir_na_fila(lat, lng), timeout=limite_s)
    except (httpx.HTTPError, ValueError, asyncio.TimeoutError) as erro:
        logger.warning("Nominatim falhou: %s", erro or "demorou demais")
        return None
    _cache[k] = nome
    return nome
