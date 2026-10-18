# Rotas de fuga simuladas no HydroTech

Esta integração usa os pontos fictícios já cadastrados no Django. A interface Vue mostra círculos vermelhos de 300 m e chama o serviço FastAPI extraído de `hydrotech-rota-fuga-main.zip`. Os mapas, as ruas e a altitude podem vir de serviços externos reais, mas **nenhum alerta ou risco do HydroTech representa uma emergência real**.

## Executar localmente

1. Inicie o Django em `http://127.0.0.1:8000` com SQLite local. Copie `hydrotechDjango_core/backend/.env.example` para `.env` apenas se ainda não houver um arquivo local e defina uma `SECRET_KEY` exclusiva. Em um terminal PowerShell:

   ```powershell
   cd hydrotechDjango_core/backend
   py -3 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   if (-not (Test-Path .env)) { Copy-Item .env.example .env }
   .\.venv\Scripts\python.exe manage.py migrate
   .\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
   ```

   Se o banco local estiver vazio, crie um usuário de demonstração da Defesa Civil antes de abrir o site. Escolha seus próprios valores para e-mail e senha:

   ```powershell
   $env:ADMIN_EMAIL = 'seu-email@exemplo.com'
   $env:ADMIN_PASSWORD = 'sua-senha-local'
   .\.venv\Scripts\python.exe manage.py seed_admin
   ```

   Depois, entre no site e cadastre ao menos um rio e um ponto de risco com coordenadas válidas. Execute `seed_admin` no terminal do backend, antes de `runserver`, ou abra outro terminal na mesma pasta e configure as variáveis novamente.
2. Em `hydrotech-rota-fuga-main`, crie um ambiente Python e instale `requirements.txt`. Copie `.env.example` para `.env` somente se ainda não houver um arquivo local e configure `HYDROTECH_API_URL=http://127.0.0.1:8000`. No PowerShell:

   ```powershell
   cd hydrotech-rota-fuga-main
   py -3 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   if (-not (Test-Path .env)) { Copy-Item .env.example .env }
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8100
   ```

   Use ambientes Python separados para Django e FastAPI: os dois projetos fixam versões diferentes de `python-dotenv` e `typing_extensions`.

3. Em outro terminal, instale e inicie o Vue com as duas APIs locais. O `.env.example` do frontend já aponta para os serviços locais:

   ```powershell
   cd hydrotech-frontend
   if (-not (Test-Path .env)) { Copy-Item .env.example .env }
   npm.cmd ci
   npm.cmd run dev
   ```

   Reinicie o Vite após mudar essas variáveis.

4. Abra `/monitoramento`, ative **Simular enchente** em um ponto e use **Rota de fuga**. A rota pode ser aberta diretamente em `/rota-de-fuga?alerta=ID&auto=1`; `auto=1` escolhe uma partida simulada próxima ao ponto do alerta e calcula a rota sem pedir GPS. Também é possível tocar no mapa, usar **Simular no ponto de risco**, selecionar **Usar minha localização** ou informar coordenadas pela URL: `/rota-de-fuga?alerta=ID&lat=-22.8885&lng=-47.0505`.

O estado da simulação de enchente fica apenas na sessão do navegador. Não há sensor, alerta público compartilhado ou mudança no banco de dados. No mapa, **Atualizar pontos do HydroTech** ignora o cache do serviço para mostrar novos cadastros.

## OpenRouteService e serviços gratuitos

`ORS_API_KEY` é opcional e pertence apenas ao `.env` do FastAPI. Não coloque essa chave em `VITE_*` ou no frontend. Com a chave, o serviço tenta pedir ao ORS um percurso que desvie das zonas. Sem chave, ou se o ORS falhar, usa o OSRM público e compara alternativas; esse fallback não consegue impor o desvio. Se nenhum provedor fornecer ruas, a tela mostra somente o destino estimado e explica a limitação. Links para Google Maps e Waze abrem aplicativos externos que **não conhecem** os riscos simulados.

O cálculo considera todos os pontos de risco próximos, mesmo quando a URL inclui `alerta=ID`. O ID destaca o ponto que motivou a simulação. O destino é apenas potencialmente menos exposto pelos critérios de distância e altitude; não é abrigo nem garantia de segurança. Altitude e ruas dependem de serviços externos gratuitos e podem estar indisponíveis.

Em celular, o navegador exige HTTPS para usar GPS, exceto em `localhost`. O toque no mapa funciona como origem simulada. Em uma implantação, configure `VITE_ROTA_API_URL` para a URL HTTPS pública do FastAPI e `HYDROTECH_API_URL` para a URL pública do Django. A chave ORS, quando usada, fica exclusivamente no ambiente do FastAPI.

## Verificação

```powershell
cd hydrotech-rota-fuga-main
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest
```

```powershell
cd hydrotech-frontend
npm.cmd run build
```

Os testes comuns do serviço simulam os provedores externos. Testes `--ao-vivo` fazem chamadas reais e exigem serviços e dados de teste ativos; não são necessários para uma demonstração local.
