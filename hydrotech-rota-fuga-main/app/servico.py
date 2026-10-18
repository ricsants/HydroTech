"""Junta zonas simuladas, destino estimado e trajeto até ele."""
import logging

from . import config, geo
from .destinos import PESO_CAMINHADA, area_mais_segura
from .enderecos import nome_do_local
from .roteamento import RotaIndisponivel, calcular_rota, ors_disponivel
from .zonas import carregar_zonas

logger = logging.getLogger(__name__)

AVISO_DENTRO = "A partida está dentro de uma área de risco simulada."


def filtrar_alertas(zonas, alertas):
    """
    Com `alertas` (ids que vêm no link do WhatsApp) só valem as zonas desses pontos.
    Se nenhum id existir mais (ponto apagado, link velho), evita todas por segurança.
    """
    if not alertas:
        return zonas, []
    ativas = [z for z in zonas if z["id"] in alertas]
    if ativas:
        return ativas, []
    return zonas, ["O ponto do alerta não foi encontrado; evitando todas as áreas de risco cadastradas."]


def _links(origem, destino, modo):
    o = f"{origem[0]:.6f},{origem[1]:.6f}"
    d = f"{destino[0]:.6f},{destino[1]:.6f}"
    viagem = "walking" if modo == "pe" else "driving"
    return {
        "google_maps": f"https://www.google.com/maps/dir/?api=1&origin={o}&destination={d}&travelmode={viagem}",
        "waze": f"https://waze.com/ul?ll={d}&navigate=yes",
    }


def _volta_extra_m(rota, destino):
    return max(0, rota["distancia_m"] - destino["distancia_linha_reta_m"])


def _rota_aceitavel(rota, destino):
    # Rua nunca é linha reta; até uns 80% a mais (mínimo 800 m) ainda é um caminho normal
    limite = max(800, 0.8 * destino["distancia_linha_reta_m"])
    return not rota["zonas_cruzadas"] and _volta_extra_m(rota, destino) <= limite


def _nota_final(opcao):
    return opcao["destino"]["nota"] - _volta_extra_m(opcao["rota"], opcao["destino"]) / 2000 * PESO_CAMINHADA


def _ordem_de_tentativa(candidatos, lat, lng):
    """
    Mantém a ordem da nota, mas evita tentar dois destinos na mesma direção seguidos:
    se o primeiro esbarrou numa zona, o vizinho dele provavelmente esbarra também.
    """
    escolhidos, sobra = [], []
    for c in candidatos:
        direcao = geo.rumo(lat, lng, c["lat"], c["lng"])
        mesma_direcao = any(
            abs((direcao - geo.rumo(lat, lng, e["lat"], e["lng"]) + 180) % 360 - 180) < 45
            for e in escolhidos
        )
        (sobra if mesma_direcao else escolhidos).append(c)
    return escolhidos + sobra


async def _calcular_opcoes(lat, lng, modo, candidatos, zonas_desvio):
    """
    Começa pelo melhor candidato e só tenta o próximo se a rota cruzar zona ou der volta demais.
    Assim cada pessoa gasta ~1 chamada ao ORS (o plano grátis dá 40 por minuto).
    """
    tentativas = config.CANDIDATOS_ROTA if ors_disponivel() else config.CANDIDATOS_ROTA_SEM_DESVIO
    opcoes, falhas_seguidas = [], 0
    for c in _ordem_de_tentativa(candidatos, lat, lng)[:tentativas]:
        try:
            rota = await calcular_rota((lat, lng), (c["lat"], c["lng"]), modo, zonas_desvio)
        except Exception as erro:
            logger.warning("Rota até %s falhou: %s", c["nome"], erro)
            falhas_seguidas += 1
            if falhas_seguidas >= 2:
                break  # serviço de rotas fora do ar, não adianta insistir
            continue
        falhas_seguidas = 0
        opcoes.append({"destino": c, "rota": rota})
        if _rota_aceitavel(rota, c):
            break
    return opcoes


def _sem_nota(destino):
    return {k: v for k, v in destino.items() if k != "nota"}


def _resposta(lat, lng, modo, dentro, destino, rota, alternativas, zonas, avisos):
    return {
        "origem": {"lat": lat, "lng": lng},
        "modo": modo,
        "dentro_de_zona_risco": bool(dentro),
        "destino": _sem_nota(destino),
        "rota": rota,
        "links": _links((lat, lng), (destino["lat"], destino["lng"]), modo),
        "alternativas": [
            {
                "destino": _sem_nota(o["destino"]),
                "distancia_m": o["rota"]["distancia_m"],
                "duracao_s": o["rota"]["duracao_s"],
                "cruza_zona_risco": bool(o["rota"]["zonas_cruzadas"]),
            }
            for o in alternativas
        ],
        "zonas_risco": zonas,
        "avisos": avisos,
    }


async def planejar_fuga(lat, lng, modo="pe", alertas=None):
    avisos = []
    try:
        todas = await carregar_zonas()
    except Exception as erro:
        # HydroTech fora do ar não pode impedir ninguém de fugir
        logger.warning("Não deu para ler as zonas do HydroTech: %s", erro)
        todas, avisos = [], ["Não foi possível consultar as áreas de risco do HydroTech agora."]

    # O alerta identifica o ponto que motivou a abertura da tela, mas os demais
    # riscos cadastrados também precisam entrar no cálculo do trajeto.
    _, avisos_alerta = filtrar_alertas(todas, alertas)
    avisos += avisos_alerta
    if not todas:
        avisos.append("Não há pontos de risco disponíveis; a exposição do destino não pode ser avaliada.")
    zonas = [z for z in todas if geo.distancia_m(lat, lng, z["lat"], z["lng"]) <= config.DISTANCIA_MAX_ZONA_M]
    dentro = [z for z in zonas if geo.distancia_m(lat, lng, z["lat"], z["lng"]) <= z["raio_m"]]
    if dentro:
        avisos.insert(0, AVISO_DENTRO)
    # A zona onde a pessoa já está não entra no desvio: ela precisa atravessá-la para sair
    zonas_desvio = [z for z in zonas if z not in dentro]

    candidatos, avisos_destino = await area_mais_segura(lat, lng, zonas)
    avisos += avisos_destino
    if not candidatos:
        raise RotaIndisponivel(
            "Não foi encontrado um destino estimado em até 5 km. A simulação não pode recomendar uma rota.")

    opcoes = await _calcular_opcoes(lat, lng, modo, candidatos, zonas_desvio)
    if not opcoes:
        # Sem serviço de rota, só é possível mostrar um destino de referência.
        destino = candidatos[0]
        destino["endereco"] = await nome_do_local(destino["lat"], destino["lng"])
        avisos.append("Não foi possível traçar o caminho pelas ruas. O destino é apenas uma referência da simulação; "
                      "Google Maps e Waze não consideram as áreas de risco simuladas.")
        return _resposta(lat, lng, modo, dentro, destino, None, [], zonas, avisos)

    opcoes.sort(key=lambda o: (len(o["rota"]["zonas_cruzadas"]), -_nota_final(o)))
    melhor = opcoes[0]
    if melhor["rota"]["zonas_cruzadas"]:
        avisos.append("O trajeto cruza uma área de risco simulada; não o interprete como recomendação de evacuação.")
    if not melhor["rota"]["desvia_zonas"]:
        if config.ORS_API_KEY:
            avisos.append("Desvio automático indisponível agora (limite do OpenRouteService); "
                          "a rota foi escolhida entre alternativas, sem garantia de evitar as áreas simuladas.")
        else:
            avisos.append("Rota calculada sem desvio automático (configure ORS_API_KEY para ativar).")

    destino = melhor["destino"]
    destino["endereco"] = await nome_do_local(destino["lat"], destino["lng"])
    return _resposta(lat, lng, modo, dentro, destino, melhor["rota"], opcoes[1:], zonas, avisos)
