# Tela da rota de fuga 3D

Notas para quem for passar a tela para o Vue do HydroTech.

O protótipo é o `web/index.html`, servido em http://127.0.0.1:8100. É um arquivo só, sem build,
com HTML, CSS e JS juntos, para ficar fácil de abrir e copiar. A versão 2D (`web/index-2d.html`,
rota `/2d`) fica de reserva para navegador sem WebGL.

## Como abrir para testar

| URL | O que mostra |
|---|---|
| `/` | Todas as áreas de risco; a pessoa usa o GPS ou toca no mapa |
| `/?alerta=2` | Modo alerta (o link do WhatsApp): destaca o ponto 2, com a faixa vermelha no painel; o cálculo considera todos os riscos próximos |
| `/?alerta=2&lat=-22.8885&lng=-47.0505` | Já calcula a rota a partir dessa posição (bom para testar sem GPS) |
| `/?alerta=2&auto=1` | Pede o GPS assim que abre (é o que o alerta envia) |
| `/?modo=carro` | Começa no modo carro |

## Bibliotecas e dados (todos grátis, sem chave)

| O quê | Fonte | Observação |
|---|---|---|
| Mapa 3D (WebGL) | **MapLibre GL JS 5.6.0** | No Vue: `npm i maplibre-gl@5.6.0` |
| Ruas, prédios com altura, água, bairros | **OpenFreeMap** (`https://tiles.openfreemap.org/planet`) | Esquema OpenMapTiles; a altura dos prédios vem de `render_height` |
| Fontes dos rótulos | `https://tiles.openfreemap.org/fonts/{fontstack}/{range}.pbf` | `Noto Sans Regular` e `Noto Sans Bold` |
| Relevo 3D (altitude) | **AWS Terrain Tiles** (`terrarium`) | Duas fontes `raster-dem`: uma para o 3D, outra para o sombreado |
| Satélite | **Esri World Imagery** | Exige o crédito "Imagens © Esri" |
| Perfil de altitude da rota | **Open-Meteo Elevation** (até 100 pontos por chamada) | Se falhar, usa a altitude do relevo do próprio mapa |
| Rota e áreas de risco | **Este serviço** (`/rota-fuga`, `/zonas-risco`, `/status`) | Veja "Dados usados" abaixo |

Os créditos (atribuições) aparecem no canto do mapa e precisam continuar visíveis.

## Partes da tela (sugestão de componentes Vue)

```
TelaRotaFuga
├── MapaFuga3D                  ← MapLibre, camadas e animações (seção "Camadas do mapa")
│   ├── PinoVoce                ← marcador HTML azul com ondas ("VOCÊ")
│   └── PinoSeguro              ← marcador HTML verde ("ÁREA SEGURA · +39 m acima do rio")
├── BarraTopo
│   ├── Marca                   ← logo 3D + "Rota de Fuga 3D"
│   └── Chips                   ← desvio (ORS ativo/reserva), nº de áreas de risco, hora
├── PainelRota (vidro, à esquerda; no celular vira gaveta embaixo; altura segue o conteúdo)
│   ├── FaixaStatus             ← uma só: "dentro da área de risco" (vermelha), alerta (discreta) ou título
│   ├── Corpo                   ← muda conforme a fase (ver abaixo)
│   │   ├── CartaoDestino       ← "Vá para", métricas e o seletor a pé / de carro
│   │   ├── ListaAvisos         ← só amarelos; o vermelho fica na faixa de status
│   │   ├── PerfilAltitude      ← terreno, nível do rio, trecho alagável e o aviso dele
│   │   └── PassoAPasso         ← <details> fechado, "N instruções"
│   └── Rodape (fixo)           ← ação principal: "Encontrar rota segura" ou "Navegar pelo Google Maps"
│                                  + Waze · Ver em 3D · Minha posição
├── ControlesCamera (coluna à direita)
│   └── 3D↔cima · satélite · percorrer rota · girar · enquadrar · legenda
├── BarraPasseio                ← aparece ao "percorrer": progresso e "faltam X m"
└── RadarCarregando             ← radar girando enquanto calcula
```

### Fases do painel

O painel tem uma fase (`estado.fase`) e o `renderPainel()` redesenha tudo quando ela muda.

| Fase | Corpo | Rodapé |
|---|---|---|
| `inicio` | seletor a pé / de carro | "Encontrar rota segura" + "ou toque no mapa" |
| `localizando` / `calculando` | esqueleto carregando (ou a rota anterior apagadinha, se já tinha uma) | botão desabilitado com o que está fazendo |
| `rota` | cartão do destino, avisos, perfil, passo a passo | "Navegar pelo Google Maps" + Waze, Ver em 3D, Minha posição |
| `erro` | aviso vermelho com o motivo | "Tentar de novo" |

Os botões do painel usam `data-acao` (`gps`, `modo`, `passeio`) e um único ouvinte de clique.

## Camadas do mapa (ordem de baixo para cima)

| id | Tipo | Fonte | Para quê |
|---|---|---|---|
| `fundo` | background | — | Azul-noite `#08101e` |
| `satelite` | raster | Esri | Escondida por padrão; liga no botão de satélite |
| `cobertura`, `parques`, `uso` | fill | OpenFreeMap | Verde-escuro e quarteirões (somem no modo satélite) |
| `relevo-sombra` | hillshade | relevo | Sombra dos morros |
| `agua`, `rios` | fill / line | OpenFreeMap | Água em azul |
| `vias-*`, `trilhos` | line | OpenFreeMap | Largura cresce com o zoom |
| `predios` | **fill-extrusion** | OpenFreeMap | Prédios 3D; cor pela altura |
| `nomes-*` | symbol | OpenFreeMap | Ruas, bairros e cidades |
| `zona-chao` | fill | GeoJSON | Círculo vermelho no chão (passar o mouse mostra o nome) |
| `zona-agua` | **fill-extrusion** | GeoJSON | "Água" azul subindo e descendo dentro da área |
| `zona-parede` | **fill-extrusion** | GeoJSON | Parede vermelha pulsando (é um anel: círculo com furo) |
| `zona-rotulo` | symbol | GeoJSON | "⚠ ÁREA DE RISCO / nome do rio" |
| `rota-brilho`, `rota-base`, `rota-trilha` | line | GeoJSON | Rota com brilho e degradê azul→verde (`line-gradient`) |
| `rota-fluxo` | line | GeoJSON | Tracejado branco "andando" (troca `line-dasharray` em ciclo) |
| `rota-baixa-brilho`, `rota-baixa` | line | GeoJSON | **Trechos abaixo do nível do rio**, em laranja |
| `farol-halo`, `farol-nucleo` | **fill-extrusion** | GeoJSON | Colunas de luz na pessoa (azul) e no destino (verde) |

Animação: um único `requestAnimationFrame` atualiza a altura da água, da parede e dos faróis e o
tracejado da rota.

## Dados usados

`GET /rota-fuga?lat&lng&modo=pe|carro&alerta=<ids>` devolve o que a tela usa:

```jsonc
{
  "dentro_de_zona_risco": true,                 // aviso vermelho
  "destino": { "nome", "tipo", "endereco", "lat", "lng",
               "altitude_m", "acima_do_risco_m",  // métrica "+39 m" e linha "nível do rio"
               "distancia_linha_reta_m" },        // usada quando não há rota
  "rota": { "geometria": { "coordinates": [[lng, lat], ...] },
            "distancia_m", "duracao_s", "passos": [{ "instrucao", "distancia_m" }] },  // pode vir null
  "links": { "google_maps", "waze" },
  "alternativas": [...], "zonas_risco": [{ "id", "rio", "descricao", "lat", "lng", "raio_m" }],
  "avisos": ["..."]
}
```

- **Nível do rio** = `destino.altitude_m - destino.acima_do_risco_m`.
- **Trecho alagável:** são amostrados 60 pontos da rota, com a altitude de cada um. Os pontos
  abaixo do nível do rio formam um `MultiLineString` laranja no mapa e a faixa vermelha no perfil.
- **`rota: null`:** os serviços de mapa estão fora. Esconde `rota-trilha` e mostra só a linha
  reta tracejada e os botões do Google Maps e do Waze.

## Comportamento da câmera

| Ação | Câmera |
|---|---|
| Abrir a página | Voa até as áreas de risco (inclinação de 62°) |
| Calcular rota | Voa até a pessoa e depois enquadra a rota inteira, olhando na direção do destino |
| Percorrer rota | Câmera baixa (inclinação 70°, zoom 17) seguindo a rota, com aceleração e desaceleração; 12 a 32 s |
| Girar | Órbita contínua, que para no segundo clique |
| 3D / de cima | Liga e desliga o relevo e a inclinação |

### Coisas que deram problema

1. **Câmera embaixo do relevo.** Com o relevo exagerado 1,8×, o chão fica a ~1.200 m. Se a câmera
   fica em 0 m, tudo aparece deslocado para cima da tela. Resolvi com três coisas:
   - `centerClampedToGround: true`;
   - `setCenterElevation(queryTerrainElevation(centro))` sempre que **não** houver animação
     acontecendo;
   - depois de cada `flyTo`, encaixar com `jumpTo` na posição pedida. No fim do voo a biblioteca
     recalcula a altitude com o relevo que tiver carregado, e às vezes o enquadramento escorrega.

   Cuidado: mexer na altitude durante um `flyTo` cancela o voo.
2. **Painel cobrindo o mapa.** Passe o `padding` do painel no `flyTo` e mire no meio da rota. O
   `center` que o `cameraForBounds` devolve, com a câmera inclinada, deixa o destino fora da tela.
3. **Popup engole o clique.** Nas áreas de risco o popup abre no `mousemove`. Com popup de clique
   não dá para marcar a pessoa dentro do círculo.
4. **`fill-extrusion-opacity` não aceita valor por feição.** Para opacidades diferentes são duas
   camadas com `filter` (`farol-halo` e `farol-nucleo`).
5. **`line-gradient`** só funciona se a fonte GeoJSON tiver `lineMetrics: true`.
6. **Classe repetida.** O LED do chip usava `.alerta`, mesmo nome da faixa de alerta, e herdava o
   estilo dela. Os estados do LED agora são `ok`, `atencao` e `perigo`.
7. **Nome de rio e de ponto vem do cadastro** e vai para HTML de popup: sempre escapar.

## Visual

**Cores**
| Token | Valor | Uso |
|---|---|---|
| `--fundo` | `#050a14` | Fundo geral |
| `--vidro` / `--vidro-forte` | `rgba(13,22,40,.72)` / `rgba(9,16,30,.86)` | Painéis com `backdrop-filter: blur(18px)` |
| `--borda` | `rgba(148,197,255,.12)` | Bordas finas azuladas |
| `--verde` / `--verde-claro` | `#10b981` / `#34d399` | Rota, destino, subida |
| `--vermelho` | `#ef4444` | Risco, alerta, botão principal |
| `--azul-claro` | `#60a5fa` | Pessoa ("VOCÊ") |
| `--ambar` / laranja | `#f59e0b` / `#fb923c` | Avisos e trecho alagável |

**Fontes:** Inter (texto) e JetBrains Mono (números das métricas).

**Receita do "3D" dos botões**, a mesma em todos:
- degradê vertical claro → escuro;
- `box-shadow` com uma **sombra sólida embaixo** (`0 7px 0 <cor bem escura>`), mais o brilho
  colorido e um realce interno no topo (`inset 0 1px 0 rgba(255,255,255,.4)`);
- ao apertar, `translateY(6px)` e a sombra sólida diminui (efeito de tecla).

**Vidro dos painéis:** fundo translúcido, mais `blur`, mais borda clara, mais uma sombra funda, mais
um reflexo em degradê no topo (`::before`).

**Cartão do destino:** `perspective: 900px`; no `mousemove` aplica `rotateX/rotateY` de até 14°.
O conteúdo fica em `translateZ(28px)`.

**Celular (menos de 820 px):** o painel vira gaveta embaixo (`max-height: 56vh`); a legenda e os
chips extras somem; o enquadramento da câmera reserva a parte de baixo da tela.

## Passando para o Vue

1. `npm i maplibre-gl@5.6.0`. O objeto `ESTILO` e as camadas podem ser copiados como estão.
2. Um service pequeno que chama `/rota-fuga` e `/zonas-risco` deste serviço e monta o link do
   alerta (`/rota-de-fuga?alerta=<id>&auto=1`). O endereço do serviço vai numa variável `VITE_`.
3. Quebrar o painel nos componentes da árvore lá de cima. `perfilSVG`, `iconePasso` e
   `margensDaTela` podem virar utilitários.
4. Manter a versão 2D para quem não tem WebGL.
