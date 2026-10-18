import os

from dotenv import load_dotenv

load_dotenv()

HYDROTECH_API_URL = os.getenv("HYDROTECH_API_URL", "http://127.0.0.1:8000").rstrip("/")

# Sem chave do ORS a rota sai pelo OSRM, que não desvia das zonas (só avisa se cruzar)
ORS_API_KEY = os.getenv("ORS_API_KEY", "").strip()

RAIO_ZONA_RISCO_M = float(os.getenv("RAIO_ZONA_RISCO_M", "300"))
MARGEM_DESTINO_M = float(os.getenv("MARGEM_DESTINO_M", "200"))      # destino fica pelo menos isso fora da zona
DISTANCIA_MAX_ZONA_M = float(os.getenv("DISTANCIA_MAX_ZONA_M", "20000"))  # zonas mais longe são ignoradas

# Quantos destinos tentar até achar uma rota boa. Sem ORS tentamos mais, porque não há desvio forçado
CANDIDATOS_ROTA = int(os.getenv("CANDIDATOS_ROTA", "3"))
CANDIDATOS_ROTA_SEM_DESVIO = int(os.getenv("CANDIDATOS_ROTA_SEM_DESVIO", "5"))

TIMEOUT_ROTA_S = float(os.getenv("TIMEOUT_ROTA_S", "10"))      # cada chamada ao ORS/OSRM
TIMEOUT_PEDIDO_S = float(os.getenv("TIMEOUT_PEDIDO_S", "40"))  # o pedido inteiro

CACHE_ZONAS_S = int(os.getenv("CACHE_ZONAS_S", "60"))

# Pré-carga de altitude: pessoas a ~1,5 km da zona + destinos até 2 km delas
RAIO_PREAQUECER_ALTITUDE_M = float(os.getenv("RAIO_PREAQUECER_ALTITUDE_M", "3500"))
MAX_PONTOS_PREAQUECER = int(os.getenv("MAX_PONTOS_PREAQUECER", "20000"))
INTERVALO_PREAQUECER_S = int(os.getenv("INTERVALO_PREAQUECER_S", "300"))

USER_AGENT = "hydrotech-rota-fuga/1.0"

OSRM_URLS = {
    "pe": "https://routing.openstreetmap.de/routed-foot/route/v1/driving",
    "carro": "https://routing.openstreetmap.de/routed-car/route/v1/driving",
}
ORS_PERFIS = {"pe": "foot-walking", "carro": "driving-car"}
