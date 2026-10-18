# HydroTech — frontend Vue

Interface do protótipo acadêmico HydroTech. Alertas, níveis e recomendações de rota são simulações; veja o [README principal](../readme.md) e o [handoff do backend](../docs/HANDOFF_BACKEND.md) para executar os três serviços.

## Desenvolvimento local

Requer Node.js 20.19+ ou 22.12+ e npm. Na pasta `hydrotech-frontend`:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
npm.cmd ci
npm.cmd run dev
```

`VITE_API_URL` aponta para o Django e `VITE_ROTA_API_URL` para o FastAPI. As variáveis `VITE_*` ficam públicas no JavaScript do navegador; nunca coloque tokens ou senhas nelas. Reinicie o Vite após editá-las.

Para conferir a compilação:

```powershell
npm.cmd run build
```

O build fica em `dist/`, que é ignorado pelo Git. O mapa usa recursos públicos de mapas; a rota de fuga depende do FastAPI separado.
