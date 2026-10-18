# Revisão antes de publicar ou transferir o HydroTech

Revisão local iniciada em 14/10/2026 e complementada em 18/10/2026 no clone oficial `ricsants/HydroTech`. A branch `feat/integracao-rota-fuga` parte do commit `090002132f` de `main`. O clone tem um único commit e nenhuma mudança foi publicada por esta preparação.

## Achados e ações nesta cópia

| Achado | Estado local | Ação fora do código |
|---|---|---|
| Token Whapi embutido no Vue e em um exemplo Node, com telefones fixos | Removidos. O Vue mantém somente a simulação local. O exemplo Node lê token/contatos do ambiente e não envia sem configuração explícita. | **Revogar o token anterior no provedor e gerar outro somente se houver necessidade autorizada.** Avisar pessoas responsáveis pelos contatos se estes foram publicados. |
| Senha administrativa fixa em `render.yaml` e em `seed_admin.py` | Removida. O comando exige `ADMIN_EMAIL` e `ADMIN_PASSWORD` e não imprime a senha. | Trocar a senha da conta já criada no ambiente hospedado, se a configuração anterior foi usada. Alterar o arquivo não modifica senhas existentes. |
| Utilitários locais criavam conta comum com senha previsível e alteravam o banco no diagnóstico | `create_user.py` exige `DEMO_EMAIL`/`DEMO_PASSWORD`; `check_setup.py` agora consulta o banco sem gravar. | Não reutilizar senhas de contas criadas pelos scripts antigos. |
| Registro de usuário escrevia telefone em arquivo JavaScript local | Removido. Registro continua criando usuário normalmente. | Examinar cópias antigas do arquivo e o histórico do repositório usado pela equipe. |
| Usuário podia enviar `is_defesa_civil` no cadastro/perfil | Corrigido nos dois endpoints; teste de regressão incluído. | Revisar contas existentes no banco para permissões concedidas indevidamente. |
| Logs de autenticação incluíam email ou telefone em alguns caminhos | Esses caminhos agora registram apenas ID ou evento. | Logs já gerados não mudam; manter fora do Git e revisar política de retenção. |
| Configuração `ORS_API_KEY` no `.env` local do FastAPI | O arquivo continua no computador e está ignorado; a variável está vazia nesta revisão. Não há chave no frontend. | Se uma chave anterior já esteve em commit, revogá-la e limpar o histórico pelo procedimento definido pela equipe. |
| `db.sqlite3`, logs e cache local | Ignorados no `.gitignore`; preservados na máquina. O banco local contém 2 usuários, com 2 emails e 1 telefone (somente contagens verificadas). | Não enviar esses arquivos em ZIP manual ou commit. O banco pode conter usuários e tokens. |
| Contexto de build Docker copiava backend local | `.dockerignore` na raiz e no backend agora excluem `.env`, SQLite, logs, mídia, caches e ambientes virtuais do contexto. | Validar o build Docker no ambiente do backend antes do deploy; não passar segredos por `COPY`. |
| `docker-compose.yml` tinha senha de banco literal de exemplo | Passou a exigir `POSTGRES_PASSWORD` e `SECRET_KEY` do ambiente. | Definir valores individuais antes de usar Compose. |
| Módulo de rotas derivado de repositório externo sem `LICENSE` nesta cópia | Origem atribuída no README/handoff. | Confirmar autorização e termos de redistribuição com o autor antes de publicar o código derivado. |

Os arquivos `.env.example` usam apenas valores fictícios e locais. A senha e token antigos não devem ser reutilizados. Os arquivos Office/PDF na raiz podem conter nomes de terceiros: revisar seu conteúdo e metadados antes de decidir incluí-los em um repositório público.

## Arquivos preparados nesta revisão

- Raiz: `.gitignore`, `.dockerignore`, `readme.md`, `INTEGRACAO-ROTAS.md`, `render.yaml`, `exemplo_whapi_alerta.js`.
- Vue: `.gitignore`, `.env.example`, `README.md`, `src/views/MonitoramentoView.vue`.
- FastAPI: `.gitignore`, `.env.example`, `README.md`. O `.env` local foi preservado.
- Django: `.gitignore`, `.dockerignore`, `.env.example`, `README.md`, `SETUP.md`, `GUIA_RAPIDO.md`, `docker-compose.yml`, `app/settings.py`, `usuarios/views.py`, `usuarios/tests.py`, `usuarios/management/commands/seed_admin.py`, `create_user.py`, `check_setup.py`, `test_gemini.py`.
- Novos: `docs/HANDOFF_BACKEND.md` e este `docs/REVISAO-PUBLICACAO.md`.

Ignorados para o Git: `.env` e variantes, bancos `*.sqlite3`, logs, caches, `.venv`, `node_modules`, `dist`, artefatos de teste e configurações locais do editor. Arquivos de lock e migrações foram preservados.

## Auditoria do repositório oficial

- O único commit de `main` foi examinado sem imprimir valores: foram encontrados um token Whapi embutido em `exemplo_whapi_alerta.js` e `hydrotech-frontend/src/views/MonitoramentoView.vue`, além de uma senha administrativa fixa em `render.yaml`. Todos os três foram removidos da versão de trabalho da branch, mas continuam no histórico de `main`.
- O clone oficial tinha 98 arquivos rastreados, nenhum arquivo remoto exclusivo na comparação com a cópia local revisada e nenhum `.env`, SQLite, log, `node_modules` ou `dist` rastreado. A transferência preservou os arquivos originais que tinham apenas diferenças de quebra de linha.
- A branch foi preparada localmente, sem commit nem push. O índice e o conteúdo a incluir devem ser novamente revisados antes de qualquer publicação.
- Instalação totalmente limpa em outro computador e deploy hospedado: dependem de ambiente/credenciais que não acompanham o projeto.
- Validade atual do token Whapi, estado da conta hospedada e eventual exposição anterior: precisam ser verificados pelos responsáveis pelas contas e pelo repositório real.

## Validação local executada

- Django: `manage.py check` sem problemas em modo local; `manage.py test usuarios rios sensores` com **14 testes aprovados**. `check_setup.py` consultou o banco sem gravar; `create_user.py` sem credenciais não criou conta. O arquivo de diagnóstico Gemini foi isolado para não executar durante descoberta de testes.
- Rotas: `pytest` com **128 testes aprovados e 24 testes ao vivo ignorados**; `pip check` sem conflitos. O diretório temporário padrão do Windows negou acesso na primeira tentativa, então os testes foram repetidos com um diretório temporário dentro do projeto e passaram.
- Vue: `npm run build` aprovado; `npm ci --offline` aprovado em pasta isolada, usando o lockfile. O npm avisou que o script de instalação do `esbuild` não estava autorizado nesse teste isolado; o build do projeto instalado anteriormente passou.
- `gitignore`: testado em repositório temporário; `.env`, banco, logs, `node_modules` e `dist` ficaram ignorados; `.env.example` permaneceu visível. O repositório temporário foi removido.
- No clone oficial, Django passou com **14 testes** (`DEBUG=True` em modo local), FastAPI com **128 aprovados e 24 ao vivo ignorados**, e Vue passou em `npm ci --offline` seguido de `npm run build`.
- Instalação Python completamente limpa, acesso real aos provedores externos e implantação hospedada **não foram verificados** nesta revisão. Os ambientes Python existentes passaram em `pip check` e nas suítes locais.

Em 18/10/2026, o mantenedor informou que o token Whapi e a senha administrativa antigos foram invalidados. Informou também autorização dos dois autores de origem para publicar esta versão derivada, com autorização documentada para adaptar e republicar o módulo de rotas. **Essas confirmações foram fornecidas pelo mantenedor; não houve acesso às contas dos provedores nem inspeção dos documentos de autorização.** A auditoria confirmou credenciais no commit original de `main`; a limpeza da branch não remove segredos de commits antigos, forks, builds já enviados ou contas hospedadas.

## Revisão no clone Git real

Execute na raiz do clone que será publicado, sem imprimir valores de segredos:

```powershell
git status --short
git branch --show-current
git diff --stat
git diff --cached --stat
git ls-files
git check-ignore -v hydrotech-rota-fuga-main/.env hydrotechDjango_core/backend/db.sqlite3 hydrotech-frontend/dist/index.html
```

Inspecione `git diff` e `git diff --cached` com cuidado em ambiente privado. Procure arquivos `.env`, bancos, logs, bundles antigos, tokens, senhas e telefones **também em commits anteriores**. Se algum segredo real já entrou no histórico, revogue primeiro; não reescreva o histórico automaticamente. A equipe deve decidir como limpar o repositório remoto e cópias existentes.

Os arquivos de código e documentação foram selecionados por caminho e estão no índice da branch local. Não crie commit nem envie a branch sem aprovação explícita do proprietário. Mensagem sugerida depois disso: `feat: integra rotas de fuga simuladas e prepara colaboração`.
