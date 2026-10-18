# Handoff para o backend — HydroTech

## Estado do projeto

Este é um protótipo acadêmico. Os níveis, enchentes e alertas mostrados no site são simulados. Pontos de risco são cadastrados no Django para a demonstração; não há avaliação oficial de segurança. A interface, o Django e o serviço de rotas já estão integrados no código local. A instalação limpa e o deploy ainda devem ser verificados pelo time antes da apresentação/publicação.

## Arquitetura e fluxo

```text
Navegador (Vue :5173)
  ├─ autenticação, rios, pontos e monitoramento → Django :8000
  └─ mapa e solicitação de trajeto → FastAPI :8100
                                         ├─ consulta /publico/rios/ e pontos no Django
                                         ├─ ORS (se houver chave) ou OSRM para ruas
                                         └─ serviços públicos para altitude/endereço
```

A simulação de enchente em `MonitoramentoView.vue` altera `floodMap` em `sessionStorage` e alimenta o gráfico; não grava alerta no banco nem envia mensagem externa. Ao clicar **Rota de fuga**, passa `alerta=<id>`, `auto=1` e coordenadas de foco ao Vue. `RotaFugaView.vue` mostra a zona vermelha, oferece GPS, clique no mapa e origem de demonstração, pede `/rota-fuga` e desenha a geometria. `alerta` identifica a origem da simulação; o algoritmo de rota considera todos os pontos próximos.

O projeto evolui [Lautenschlaeger-lucas/HydroTech](https://github.com/Lautenschlaeger-lucas/HydroTech) e integra o módulo FastAPI derivado de [JhonnesDev/hydrotech-rota-fuga](https://github.com/JhonnesDev/hydrotech-rota-fuga). As cópias consultadas não trazem `LICENSE`; o mantenedor informou autorização dos dois autores para publicar esta versão e autorização documentada para adaptar e republicar o módulo de rotas. Os documentos de autorização não foram inspecionados nesta revisão. Não remover atribuições dos mapas.

## O que já existe

- Vue: landing page, login, registro, perfil, páginas administrativas, monitoramento com gráficos, simulação por ponto e mapa da rota.
- Django: autenticação JWT, usuários, rios, pontos de risco, favoritos/alertas por usuário, leitura pública de rios/pontos e resumo público. Existem modelos e APIs de sensores, mas não alimentam esta demonstração de rota.
- FastAPI: leitura pública dos pontos, círculo de risco com raio global, seleção de destino estimado, cálculo via ORS opcional, fallback OSRM, altitude/endereço quando disponíveis, resposta com avisos e passos.
- Segurança preparada nesta cópia: senha padrão de administrador e token/contatos Whapi removidos do código publicável; cadastro e edição do próprio perfil não podem ativar `is_defesa_civil`; logs de autenticação não imprimem email/telefone; `.env` e dados locais ignorados.

## Contratos consumidos

Consulte `hydrotech-frontend/src/services/api.js`, `hydrotechDjango_core/backend/app/urls.py` e `hydrotech-rota-fuga-main/app/main.py` para o contrato exato. Caminhos principais:

| Origem → destino | Endpoints | Uso |
|---|---|---|
| Vue → Django | `POST /auth/register/`, `/auth/login/`, `/auth/refresh/`; `GET/PATCH /auth/me/` | Contas e sessão JWT. |
| Vue → Django | `GET/POST /rios/`, `GET/PUT/DELETE /rios/{id}/`, `GET/POST /rios/{id}/pontos-risco/`, `PUT/DELETE /pontos-risco/{id}/` | Administração conforme permissões. |
| Vue → Django | `GET /publico/rios/`, `/publico/rios/{id}/pontos-risco/`, `/publico/summary/` | Monitoramento público. |
| Vue → FastAPI | `GET /status`, `/zonas-risco?atualizar=1`, `/rota-fuga?lat=...&lng=...&modo=pe&alerta=ID` | Configuração, zonas e trajeto. |
| FastAPI → Django | `GET /publico/rios/`, `/publico/rios/{id}/pontos-risco/` | Pontos fictícios. Sem credenciais. |

`PontoRiscoSerializer` devolve `id`, `rio`, `rio_nome`, `latitude`, `longitude`, `descricao`, `nivel_base`, `limite_atencao`, `limite_alerta`, `limite_emergencia`, `favorito` e campos de auditoria. `zonas-risco` transforma cada ponto em `{id, descricao, rio, cidade, lat, lng, raio_m}`. `rota-fuga` devolve `origem`, `modo`, `dentro_de_zona_risco`, `destino`, `rota`, `links`, `alternativas`, `zonas_risco` e `avisos`. `rota` contém `provedor`, `desvia_zonas`, `zonas_cruzadas`, `geometria`, `distancia_m`, `duracao_s` e `passos`, ou `null` quando não há caminho pelas ruas.

O Django responde `401`/`403` conforme autenticação/permissão. O FastAPI responde `422` para parâmetros inválidos, `502` em `/zonas-risco` quando não consegue ler o Django e `503` para rota indisponível/timeout. O Vue mostra erro e permite tentar atualizar os pontos novamente.

## Configuração e execução

Use o [README principal](../readme.md) para instalar em três terminais. Ambientes independentes são importantes: Django e FastAPI fixam versões distintas de `python-dotenv`/`typing_extensions`. Arquivos de exemplo:

- `hydrotechDjango_core/backend/.env.example`: SQLite local; no host configurar PostgreSQL, `SECRET_KEY`, `DEBUG=False`, hosts, CORS e URL do frontend. `ADMIN_EMAIL` e `ADMIN_PASSWORD` são opcionais para a criação inicial; o comando não cria conta com senha padrão. `GEMINI_API_KEY` é opcional para a descrição de rios.
- `hydrotech-rota-fuga-main/.env.example`: `HYDROTECH_API_URL` obrigatório para acessar o Django; `ORS_API_KEY` opcional; raio, margens e tempos configuráveis.
- `hydrotech-frontend/.env.example`: `VITE_API_URL` e `VITE_ROTA_API_URL`. Seus valores entram no bundle e não podem ser segredos.

No deploy, o FastAPI precisa de URL HTTPS acessível ao navegador e conexão com a API pública do Django. Configurar apenas a URL do Django não publica automaticamente o serviço de rotas. O `render.yaml` da raiz descreve o Django e o banco; não descreve o FastAPI. O `.env` local não deve ser enviado ao host ou ao GitHub.
Os dois contextos de Docker têm `.dockerignore` para não copiar banco local, logs, `.env`, cache e ambientes virtuais para a imagem do Django.

## Dependências externas e limites

- OpenRouteService: chave opcional **no FastAPI**. Um `200` do ORS mostra que respondeu, mas verifique `rota.provedor` para saber qual trajeto foi exibido.
- OSRM: fallback público. Seleciona alternativas, mas não impõe desvio dos círculos.
- OpenStreetMap: mapas/ruas; serviços públicos de altitude e Nominatim podem ficar indisponíveis. Destino é estimado, não abrigo cadastrado.
- O círculo de risco usa `RAIO_ZONA_RISCO_M` global (300 m padrão), não um raio individual por ponto.
- Links externos Google Maps/Waze não conhecem as zonas fictícias; a página avisa isso.

## Pendências e riscos conhecidos

1. **Credenciais antigas:** o mantenedor informou que o token Whapi e a senha administrativa antiga foram invalidados. Isto não foi verificado nas contas dos provedores. A remoção do código não retira os valores do histórico existente.
2. **Git:** o clone oficial foi criado a partir do commit `090002132f` de `main`, com um único commit no histórico. A branch local `feat/integracao-rota-fuga` contém a integração sem commit ou push. A auditoria encontrou no commit original um token Whapi em dois arquivos e uma senha administrativa fixa no `render.yaml`, sem registrar seus valores aqui. Uma alteração nesta branch não apaga o histórico antigo. Não reescrever `main` automaticamente.
3. **Origem da rota:** o mantenedor informou autorização documentada para adaptação e republicação do módulo; conservar esse registro, pois não há licença publicada na cópia consultada.
4. **Instalação limpa:** executar as instruções do README em um clone novo. Banco local, caches e chaves não irão junto; será necessário cadastrar rio/ponto e configurar uma conta de demonstração.
5. **Persistência:** o botão de simular enchente usa `sessionStorage`; outros usuários não veem o mesmo alerta, e o estado não sobrevive a uma nova sessão. Não declarar monitoramento em tempo real.
6. **Serviços gratuitos:** ORS/OSRM/altitude/Nominatim podem falhar ou limitar requisições. Quando o Django falha, `/zonas-risco` retorna erro; o mapa não deve ser interpretado como completo.
7. **Dados pessoais:** `db.sqlite3` local e logs ficam fora do Git. Revisar documentos Office/PDF da raiz antes de publicá-los, pois podem conter nomes ou outros dados de terceiros.

## Continuidade sugerida

- Se alertas compartilhados forem necessários após a apresentação, especificar primeiro o modelo e as permissões no Django; manter o rótulo de simulação.
- Se cada ponto precisar de área diferente, adicionar `raio_m` ao modelo/serializer e depois adaptar `zonas.py` e mapa, com migração planejada.
- Se houver notificações reais no futuro, desenhar serviço backend separado, consentimento e credenciais no host; nunca reintroduzir token ou contatos no Vue. Não há envio WhatsApp no fluxo atual.
- Preservar testes de permissões de cadastro/perfil e acrescentar testes de contrato ao alterar APIs.

## Verificação e entrega

Rode `manage.py check`, `manage.py test`, `python -m pytest` no serviço de rotas e `npm run build` no Vue. Verifique `/publico/rios/`, `/zonas-risco`, `/status` e uma rota simulada em navegador. Veja [a revisão de publicação](REVISAO-PUBLICACAO.md) para os achados do histórico e as confirmações do mantenedor. Não há commit nem push nesta entrega.
