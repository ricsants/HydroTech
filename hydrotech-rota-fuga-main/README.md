# HydroTech · Rota de Fuga

Serviço que calcula uma rota de demonstração da posição de uma pessoa até um ponto estimado fora das áreas de
risco de enchente do HydroTech. Ele roda separado do HydroTech e só lê a API pública dele. Não
grava nada lá.

Junto vem uma tela 3D (`web/index.html`) que serve de referência para o front-end.

## Como funciona

1. Cada ponto de risco cadastrado no HydroTech vira uma zona circular simulada de 300 m considerada no cálculo.
2. Como o HydroTech não tem abrigos cadastrados, o serviço testa 64 pontos em volta da pessoa
   (16 direções, de 0,5 a 2 km) e descarta os que caem dentro ou perto de uma zona.
3. Compara a altitude de cada ponto com a do rio e descarta os que ficam abaixo dele.
4. Dá uma nota para cada ponto. Ganha quem fica mais alto que o rio e mais longe da zona, e perde
   quem fica longe demais da pessoa. Os pesos estão no topo de `app/destinos.py`.
5. Calcula a rota até o melhor ponto. Se ela cruzar uma zona ou der muita volta, tenta o próximo,
   de preferência em outra direção.
6. Devolve a rota, o passo a passo em português, a rua e o bairro do destino e os links para o
   Google Maps e o Waze.

Se a partida está dentro de uma zona, a resposta avisa e procura um destino estimado fora dela.

O desvio de verdade das zonas é feito pelo OpenRouteService (precisa de chave grátis). Sem a
chave, ou quando a cota do dia acaba, a rota sai pelo OSRM público. Ele não sabe desviar, então o
serviço prefere, entre as alternativas, a que cruza menos zonas. Ainda pode haver cruzamentos.

## Rodando

Precisa do HydroTech no ar (padrão `http://127.0.0.1:8000`) e de Python 3.10 ou mais novo.

```bash
python -m venv venv
venv\Scripts\python -m pip install -r requirements.txt
copy .env.example .env
venv\Scripts\python -m uvicorn app.main:app --port 8100
```

No Linux/macOS é `venv/bin/python` e `cp`.

Abra http://127.0.0.1:8100 e use o botão "Encontrar rota segura" (GPS) ou clique no mapa para
marcar onde a pessoa está. A documentação da API fica em http://127.0.0.1:8100/docs.

Para testar sem GPS: `http://127.0.0.1:8100/?lat=-22.8885&lng=-47.0505`.

## Testes

```bash
venv\Scripts\python -m pip install -r requirements-dev.txt
venv\Scripts\python -m pytest
```

Esses rodam sem rede, com os serviços externos simulados.

Há também testes contra os serviços reais, que ficam de fora por padrão. Para rodar, o serviço
precisa estar no ar na porta 8100 e o HydroTech precisa ter o ponto de teste de
`tests/conftest.py` cadastrado:

```bash
venv\Scripts\python -m pytest --ao-vivo
```

O `tests/test_integracao_hydrotech.py` cria um rio e um ponto de verdade no HydroTech e apaga no
fim. Para ele precisa de um usuário da Defesa Civil nas variáveis `HYDROTECH_ADMIN_EMAIL` e
`HYDROTECH_ADMIN_SENHA`.

## API

| Método | Rota | O que faz |
|---|---|---|
| GET | `/rota-fuga?lat=..&lng=..&modo=pe\|carro&alerta=<ids>` | Rota simulada a partir da posição |
| GET | `/zonas-risco?alerta=<ids>` | Zonas de risco lidas do HydroTech |
| GET | `/status` | Configuração atual |
| GET | `/` | Tela 3D |
| GET | `/2d` | Tela 2D, para navegador sem WebGL |

O parâmetro `alerta` recebe os ids dos pontos que dispararam o alerta (por exemplo `7` ou `7,9`).
Na rota de fuga, o ID identifica o alerta, mas o cálculo considera todas as zonas
cadastradas próximas. Em `/zonas-risco?alerta=<ids>`, a resposta é filtrada para
os pontos indicados. Se o ID não existir mais, o serviço avisa e considera todas.
Use `/zonas-risco?atualizar=1` para ignorar o cache após cadastrar um ponto.

Os riscos e alertas do HydroTech são fictícios. O destino é apenas uma estimativa
de menor exposição, não um abrigo nem uma indicação de segurança real.

Resposta de `/rota-fuga`, resumida:

```json
{
  "dentro_de_zona_risco": false,
  "destino": {
    "nome": "Destino estimado", "tipo": "Ponto de demonstração", "endereco": "Rua X, Bairro Y",
    "lat": -22.90, "lng": -47.06, "altitude_m": 704, "acima_do_risco_m": 39.0, "distancia_risco_m": 1200
  },
  "rota": {
    "provedor": "openrouteservice", "distancia_m": 2100, "duracao_s": 1500,
    "passos": [{ "instrucao": "Vire à direita na Rua Y", "distancia_m": 120 }],
    "geometria": { "type": "LineString", "coordinates": [[-47.05, -22.88]] }
  },
  "links": { "google_maps": "https://www.google.com/maps/dir/...", "waze": "https://waze.com/ul?..." },
  "alternativas": [],
  "zonas_risco": [],
  "avisos": []
}
```

`rota` vem `null` quando nenhum serviço de rota responde. Nesse caso o destino continua certo e
os links do Google Maps e do Waze traçam o caminho.

## Usando no HydroTech

- Simulação de alerta no Vue: abrir `https://<site>/rota-de-fuga?alerta=<id do ponto>&auto=1`.
  `auto=1` simula uma partida próxima ao ponto do alerta e calcula a rota sem GPS. O GPS permanece opcional no botão da tela; o frontend não envia mensagens externas.
- Front-end: chamar `GET /rota-fuga` (o CORS está liberado) e desenhar `rota.geometria` no mapa.
  O guia da tela 3D, com componentes, camadas, câmera e cores, está em `docs/TELA-3D.md`.
- Em produção o serviço precisa de HTTPS, porque o celular só libera o GPS em HTTPS.

## Configuração (`.env`)

| Variável | Padrão | Para quê |
|---|---|---|
| `HYDROTECH_API_URL` | `http://127.0.0.1:8000` | API do HydroTech |
| `ORS_API_KEY` | vazio | Chave do openrouteservice.org; liga o desvio das zonas |
| `RAIO_ZONA_RISCO_M` | `300` | Raio evitado em volta de cada ponto de risco |
| `MARGEM_DESTINO_M` | `200` | Quanto o destino fica fora da zona, no mínimo |
| `CANDIDATOS_ROTA` / `CANDIDATOS_ROTA_SEM_DESVIO` | `3` / `5` | Quantos destinos tentar, com e sem ORS |
| `TIMEOUT_ROTA_S` / `TIMEOUT_PEDIDO_S` | `10` / `40` | Limite de cada chamada de rota e do pedido inteiro |
| `RAIO_PREAQUECER_ALTITUDE_M` | `3500` | Raio da pré-carga de altitude em volta das zonas |
| `INTERVALO_PREAQUECER_S` | `300` | De quanto em quanto tempo procura zonas novas |

## Quando os serviços grátis falham

Num alerta muita gente pede rota ao mesmo tempo, e as APIs grátis começam a recusar. O serviço
foi feito para continuar respondendo assim mesmo:

- **Altitude:** a da região em volta de cada zona é baixada com calma em segundo plano e salva em
  `cache/altitudes.json`. Na hora do alerta quase não precisa da API. Se o Open-Meteo recusar,
  usa o OpenTopoData.
- **Zonas:** vários pedidos juntos fazem uma consulta só ao HydroTech.
- **Rota:** cada pessoa gasta em geral uma chamada ao ORS (o plano grátis dá 40 por minuto).
  - Se a cota diária do ORS acaba, ele fica pausado por 10 minutos e a rota sai pelo OSRM.
  - Se o OSRM cai, fica pausado por 1 minuto e a resposta sai na hora, só com o destino e os links.
- **Nome da rua:** o Nominatim aceita no máximo 1 pedido por segundo. Se demorar mais de 2,5 s, a
  rota sai sem o nome.
- **HydroTech fora do ar:** a rota sai sem as zonas, com um aviso.

## Limitações

- O cálculo só considera os pontos de risco fictícios cadastrados. Uma área sem ponto cadastrado não entra na análise.
- O destino é um ponto estimado para a simulação; não é um abrigo cadastrado nem tem segurança verificada.
- A altitude vem de um modelo de terreno de ~90 m. Dá para dizer se um ponto é mais alto ou mais
  baixo que o rio, mas não serve para medir a rua.
- Os servidores públicos (OSRM, Open-Meteo, Nominatim) são de demonstração. Para produção, o ideal
  é ter um servidor próprio do OpenRouteService
  ([imagem Docker oficial](https://giscience.github.io/openrouteservice/run-instance/)).

## Estrutura

```
app/
  main.py         rotas da API e a pré-carga em segundo plano
  servico.py      junta zonas, destino e rota
  destinos.py     escolhe o destino (candidatos e nota)
  roteamento.py   ORS e OSRM, com as pausas quando caem
  altitude.py     altitude do terreno, cache e pré-carga
  enderecos.py    rua e bairro pelo Nominatim
  zonas.py        lê os pontos de risco do HydroTech
  geo.py          contas de distância e direção
  config.py       variáveis do .env
web/
  index.html      tela 3D (MapLibre)
  index-2d.html   tela 2D de reserva (Leaflet)
docs/TELA-3D.md   guia da tela para o front-end
tests/
```
