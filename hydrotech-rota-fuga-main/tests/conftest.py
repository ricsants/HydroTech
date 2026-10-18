import asyncio
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Ponto de risco de teste no centro de Campinas. Os testes ao vivo esperam que ele
# esteja cadastrado no HydroTech local com estas coordenadas.
ZONA_CENTRO = {"id": 1, "descricao": "Ponto de teste - Centro", "rio": "Ribeirão Teste",
               "cidade": "Campinas", "lat": -22.9056, "lng": -47.0584, "raio_m": 300.0}


def rodar(coro):
    return asyncio.run(coro)


def pytest_addoption(parser):
    parser.addoption("--ao-vivo", action="store_true", help="roda também os testes que usam serviços reais")


def pytest_configure(config):
    config.addinivalue_line("markers", "ao_vivo: usa HydroTech, OpenRouteService e as APIs de altitude de verdade")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--ao-vivo"):
        return
    pular = pytest.mark.skip(reason="teste ao vivo, rode com --ao-vivo")
    for item in items:
        if "ao_vivo" in item.keywords:
            item.add_marker(pular)
