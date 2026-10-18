"""Pontos de risco do HydroTech (só leitura, pela API pública)."""
import asyncio
import time

import httpx

from . import config

_cache = {"quando": 0.0, "zonas": None}
# Num alerta chegam vários pedidos juntos; só o primeiro vai ao HydroTech, os outros esperam
_trava = asyncio.Lock()


def _cache_valido():
    return _cache["zonas"] is not None and time.monotonic() - _cache["quando"] < config.CACHE_ZONAS_S


async def _get_json(cliente, caminho):
    resp = await cliente.get(f"{config.HYDROTECH_API_URL}{caminho}")
    resp.raise_for_status()
    dados = resp.json()
    return dados if isinstance(dados, list) else dados.get("results", [])


async def carregar_zonas(forcar=False):
    """Cada ponto de risco vira uma zona circular de RAIO_ZONA_RISCO_M."""
    if not forcar and _cache_valido():
        return _cache["zonas"]
    async with _trava:
        if not forcar and _cache_valido():
            return _cache["zonas"]
        return await _buscar_zonas()


async def _buscar_zonas():
    agora = time.monotonic()
    async with httpx.AsyncClient(timeout=15) as cliente:
        rios = await _get_json(cliente, "/publico/rios/")
        listas = await asyncio.gather(
            *(_get_json(cliente, f"/publico/rios/{rio['id']}/pontos-risco/") for rio in rios),
            return_exceptions=True,
        )

    rios_por_id = {rio["id"]: rio for rio in rios}
    zonas = []
    for pontos in listas:
        if isinstance(pontos, Exception):
            continue  # um rio com erro não derruba os outros
        for p in pontos:
            rio = rios_por_id.get(p.get("rio"), {})
            zonas.append({
                "id": p["id"],
                "descricao": p.get("descricao", ""),
                "rio": rio.get("nome") or p.get("rio_nome", ""),
                "cidade": rio.get("cidade", ""),
                "lat": float(p["latitude"]),
                "lng": float(p["longitude"]),
                "raio_m": config.RAIO_ZONA_RISCO_M,
            })

    _cache.update(quando=agora, zonas=zonas)
    return zonas
