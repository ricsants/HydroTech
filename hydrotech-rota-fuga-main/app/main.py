"""API da rota de fuga. Roda separada do HydroTech e só lê a API pública dele."""
import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from . import altitude, config
from .roteamento import RotaIndisponivel
from .servico import filtrar_alertas, planejar_fuga
from .zonas import carregar_zonas

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

PASTA_WEB = Path(__file__).resolve().parent.parent / "web"
IDS_DE_ALERTA = r"^\d+(,\d+)*$"


async def _manter_altitudes_em_dia():
    # Zona nova cadastrada no HydroTech aparece aqui em até INTERVALO_PREAQUECER_S
    while True:
        try:
            await altitude.preaquecer(await carregar_zonas(forcar=True))
        except Exception as erro:
            logger.warning("Pré-carga de altitude falhou, tento de novo depois: %s", erro)
        await asyncio.sleep(config.INTERVALO_PREAQUECER_S)


@asynccontextmanager
async def ciclo_de_vida(app):
    logger.info("Altitudes carregadas do disco: %s", altitude.carregar_do_disco())
    tarefa = asyncio.create_task(_manter_altitudes_em_dia())
    yield
    tarefa.cancel()


app = FastAPI(
    title="HydroTech · Rota de Fuga",
    description="Protótipo acadêmico: rotas estimadas a partir de pontos de risco simulados, sem garantia de segurança.",
    version="1.0.0",
    lifespan=ciclo_de_vida,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"])


def _ids(alerta):
    return {int(i) for i in alerta.split(",")} if alerta else None


@app.get("/", include_in_schema=False)
def tela_3d():
    return FileResponse(PASTA_WEB / "index.html")


@app.get("/2d", include_in_schema=False)
def tela_2d():
    # Para navegador sem WebGL
    return FileResponse(PASTA_WEB / "index-2d.html")


@app.get("/rota-fuga")
async def rota_fuga(
    lat: float = Query(..., ge=-90, le=90, description="Latitude da pessoa"),
    lng: float = Query(..., ge=-180, le=180, description="Longitude da pessoa"),
    modo: Literal["pe", "carro"] = Query("pe", description="A pé ou de carro"),
    alerta: str | None = Query(None, pattern=IDS_DE_ALERTA,
                               description="Ids dos pontos em alerta (ex.: 7 ou 7,9). Sem isso, evita todos."),
):
    try:
        return await asyncio.wait_for(planejar_fuga(lat, lng, modo, _ids(alerta)), timeout=config.TIMEOUT_PEDIDO_S)
    except RotaIndisponivel as erro:
        raise HTTPException(status_code=503, detail=str(erro))
    except asyncio.TimeoutError:
        raise HTTPException(status_code=503, detail="Os serviços de mapa estão lentos demais agora. "
                                                    "Siga as orientações da Defesa Civil.")


@app.get("/zonas-risco")
async def zonas_risco(
    alerta: str | None = Query(None, pattern=IDS_DE_ALERTA),
    atualizar: bool = Query(False, description="Ignora o cache para mostrar pontos recém-cadastrados"),
):
    try:
        zonas = await carregar_zonas(forcar=atualizar)
    except Exception as erro:
        raise HTTPException(status_code=502, detail=f"HydroTech indisponível: {erro}")
    return filtrar_alertas(zonas, _ids(alerta))[0]


@app.get("/status")
def status():
    return {
        "hydrotech_api": config.HYDROTECH_API_URL,
        "desvio_de_zonas": "openrouteservice" if config.ORS_API_KEY else "desativado (sem ORS_API_KEY, usando OSRM)",
        "raio_zona_risco_m": config.RAIO_ZONA_RISCO_M,
    }
