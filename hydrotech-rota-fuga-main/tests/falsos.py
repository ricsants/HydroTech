"""Dublês de httpx para os testes não dependerem de rede."""
import httpx


class RespostaFalsa:
    def __init__(self, dados=None, status=200):
        self._dados = dados if dados is not None else {}
        self.status_code = status
        self.text = str(self._dados)

    def json(self):
        return self._dados

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(f"status {self.status_code}", request=None, response=None)


def cliente_falso(get=None, post=None):
    """
    Substitui httpx.AsyncClient. `get` e `post` recebem os mesmos argumentos da chamada
    real e devolvem uma RespostaFalsa.
    """
    class Cliente:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def get(self, url, **kwargs):
            return get(url, **kwargs)

        async def post(self, url, **kwargs):
            return post(url, **kwargs)

    return Cliente


async def sem_espera(*args):
    """Troca o asyncio.sleep para os testes não ficarem esperando de verdade."""
