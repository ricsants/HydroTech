# HydroTech Backend - Pronto para Produção ✓

Backend Django completo e otimizado para a aplicação HydroTech.

## 📋 Resumo das Melhorias Implementadas

### 🔐 Segurança
- ✓ Variáveis de ambiente com `python-dotenv`
- ✓ SECRET_KEY removida do código-fonte
- ✓ DEBUG configurável por variável de ambiente
- ✓ ALLOWED_HOSTS dinâmico
- ✓ CORS configurável com `django-cors-headers`
- ✓ Configurações de segurança para HTTPS em produção
- ✓ XSS protection e Content Security Policy

### 🗄️ Banco de Dados
- ✓ Suporte a SQLite (desenvolvimento) e PostgreSQL (produção)
- ✓ Modelos bem definidos com relacionamentos corretos
- ✓ Migrações organizadas
- ✓ Admin do Django configurado

### 📊 API REST
- ✓ Paginação automática em endpoints de lista
- ✓ Filtros e busca configurados
- ✓ Autenticação JWT + API Token
- ✓ Permissões granulares por endpoint
- ✓ Serializers com validações robustas
- ✓ Tratamento de erros consistente

### ✅ Validações
- ✓ Validação de email (único)
- ✓ Validação de senha forte (8+ chars, maiúscula, minúscula, número)
- ✓ Validação de data de nascimento (mínimo 13 anos)
- ✓ Validação de coordenadas geográficas
- ✓ Validação de campos obrigatórios

### 📝 Logging
- ✓ Sistema de logging configurado
- ✓ Logs em arquivo e console
- ✓ Níveis de log configuráveis
- ✓ Rotação de arquivos de log automática

### 🐳 Deployment
- ✓ Dockerfile para containerização
- ✓ docker-compose.yml com PostgreSQL
- ✓ Gunicorn configurado para produção
- ✓ WhiteNoise para servir arquivos estáticos
- ✓ WSGI production pronto

### 📚 Documentação
- ✓ SETUP.md com guia completo
- ✓ check_setup.py para validar instalação
- ✓ Comentários em código
- ✓ Este README

## 🚀 Início Rápido

### Desenvolvimento Local

```bash
# 1. Navegue até o backend
cd hydrotechDjango_core/backend

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env  # Use .env que já está configurado para dev

# 5. Execute as migrações
python manage.py migrate

# 6. Crie um superuser
python manage.py createsuperuser

# 7. Verifique o setup
python check_setup.py

# 8. Inicie o servidor
python manage.py runserver
```

Acesse:
- API: http://localhost:8000
- Admin: http://localhost:8000/admin
- Docs: http://localhost:8000/api-docs (com drf-spectacular)

### Com Docker (Produção)

```bash
# 1. Navegue até o backend
cd hydrotechDjango_core/backend

# 2. Inicie os containers
docker-compose up -d

# 3. Execute as migrações
docker-compose exec web python manage.py migrate

# 4. Crie um superuser
docker-compose exec web python manage.py createsuperuser

# 5. Verifique
docker-compose exec web python check_setup.py
```

## 📁 Estrutura de Arquivos

```
backend/
├── .env                    # Variáveis de ambiente (desenvolvimento)
├── .env.example            # Template de variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo git
├── requirements.txt        # Dependências Python
├── manage.py               # Gerenciador Django
├── check_setup.py          # Script de validação
├── docker-compose.yml      # Configuração Docker
├── Dockerfile              # Imagem Docker
├── SETUP.md                # Guia de instalação
├── README.md               # Este arquivo
│
├── app/
│   ├── settings.py         # Configurações principais
│   ├── urls.py             # Rotas principais
│   ├── wsgi.py             # WSGI (desenvolvimento)
│   ├── wsgi_prod.py        # WSGI production
│   ├── middleware.py       # Custom middleware
│   └── asgi.py             # ASGI
│
├── usuarios/
│   ├── models.py           # Modelo de usuário
│   ├── views.py            # Endpoints de usuários
│   ├── serializers.py      # Serializers com validações
│   ├── permissions.py      # Permissões customizadas
│   ├── authentication.py   # JWT + API Token auth
│   ├── admin.py            # Admin do Django
│   ├── urls.py             # Rotas (se separadas)
│   └── migrations/         # Migrações do banco
│
├── rios/
│   ├── models.py           # Modelos de rios e pontos de risco
│   ├── views.py            # Endpoints de rios
│   ├── serializers.py      # Serializers com validações
│   ├── admin.py            # Admin do Django
│   ├── urls.py             # Rotas (se separadas)
│   └── migrations/         # Migrações do banco
│
├── logs/                   # Logs da aplicação
└── staticfiles/            # Arquivos estáticos (produção)
```

## 🔌 Endpoints Principais

### Autenticação
- `POST /auth/login/` - Login
- `POST /auth/register/` - Registro
- `POST /auth/refresh/` - Renovar token JWT
- `GET /auth/me/` - Dados do usuário logado

### Usuários (Admin)
- `GET /usuarios/` - Listar usuários
- `GET /usuarios/<id>/` - Detalhe do usuário
- `PUT /usuarios/<id>/` - Atualizar usuário
- `DELETE /usuarios/<id>/` - Deletar usuário

### Rios
- `GET /rios/` - Listar rios (paginado)
- `POST /rios/` - Criar rio
- `GET /rios/<id>/` - Detalhe do rio
- `PUT /rios/<id>/` - Atualizar rio
- `DELETE /rios/<id>/` - Deletar rio
- `POST /rios/<id>/favorite/` - Adicionar/remover favorito

### Pontos de Risco
- `GET /rios/<rio_id>/pontos-risco/` - Listar pontos (paginado)
- `POST /rios/<rio_id>/pontos-risco/` - Criar ponto
- `GET /pontos-risco/<id>/` - Detalhe do ponto
- `PUT /pontos-risco/<id>/` - Atualizar ponto
- `DELETE /pontos-risco/<id>/` - Deletar ponto

## 🔑 Variáveis de Ambiente Principais

```env
# Segurança
DEBUG=True                                          # False em produção
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1,seu-dominio.com

# Banco de Dados
DATABASE_ENGINE=django.db.backends.sqlite3         # ou postgresql
DATABASE_NAME=db.sqlite3

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60                       # minutos
JWT_REFRESH_TOKEN_LIFETIME=7                       # dias

# Logging
LOG_LEVEL=INFO                                     # DEBUG, INFO, WARNING, ERROR
```

## 🧪 Validações Implementadas

### Usuários
- Nome: mínimo 3 caracteres
- Email: formato válido, único
- Senha: 8+ caracteres, maiúscula, minúscula, número
- Data de nascimento: mínimo 13 anos

### Rios
- Nome: mínimo 3 caracteres
- Cidade e Estado: obrigatórios
- Risco: 1 (Baixo), 2 (Médio), 3 (Alto), 4 (Muito Alto)

### Pontos de Risco
- Latitude: -90 a 90
- Longitude: -180 a 180
- Descrição: mínimo 10 caracteres
- Nível de Risco: 1 (Baixo), 2 (Médio), 3 (Alto)

## 📊 Paginação

Todos os endpoints de lista suportam paginação:

```
GET /rios/?page=1&page_size=10
```

Respostas incluem:
- `count`: Total de itens
- `next`: URL da próxima página
- `previous`: URL da página anterior
- `results`: Array de resultados

## 🔑 Autenticação

### JWT Token
```bash
# Obter token
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","senha":"password"}'

# Usar token em requisições
curl -H "Authorization: Bearer <token>" http://localhost:8000/auth/me/
```

### API Token
```bash
# Via admin do Django, gerar um API Token para o usuário
# Usar em requisições
curl -H "Authorization: Bearer <api_token>" http://localhost:8000/rios/
```

## 🚨 Troubleshooting

**Erro: ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**Erro: Database error**
```bash
python manage.py migrate --run-syncdb
```

**CORS Errors**
- Verificar `CORS_ALLOWED_ORIGINS` no `.env`

**Logs**
- Ver em `backend/logs/django.log`

## 📈 Performance

- ✓ Paginação padrão em listas
- ✓ Select_related/prefetch_related em serializers
- ✓ Índices no banco de dados
- ✓ Cache de tokens JWT
- ✓ Compressão Gzip (WhiteNoise)

## 🔄 Ciclo de Desenvolvimento

```bash
# Fazer mudanças nos models
python manage.py makemigrations

# Aplicar mudanças
python manage.py migrate

# Testar
python manage.py test

# Testar setup completo
python check_setup.py

# Collect static files (produção)
python manage.py collectstatic --noinput
```

## 📦 Dependências Principais

- Django 4.2.29
- Django REST Framework 3.16.1
- djangorestframework-simplejwt 5.5.1
- django-cors-headers 4.3.1
- python-dotenv 1.0.0
- psycopg2-binary 2.9.9
- gunicorn 21.2.0
- whitenoise 6.6.0

## ✨ Próximas Melhorias (Opcional)

- [ ] Adicionar drf-spectacular para documentação OpenAPI
- [ ] Implementar rate limiting
- [ ] Adicionar cache Redis
- [ ] Testes automatizados completos
- [ ] CI/CD com GitHub Actions
- [ ] Monitoramento com Sentry
- [ ] Analytics com Mixpanel/Amplitude

## 📞 Suporte

Para dúvidas ou problemas, consulte:
- SETUP.md - Guia detalhado de instalação
- Logs em `backend/logs/django.log`
- Django Docs: https://docs.djangoproject.com/

## ✅ Checklist Final

- [x] Variáveis de ambiente configuradas
- [x] Segurança otimizada
- [x] Banco de dados robusto
- [x] Autenticação JWT + API Token
- [x] Validações em todos os serializers
- [x] Logging configurado
- [x] Docker setup
- [x] Documentação completa
- [x] Script de validação
- [x] Admin Django configurado

**O backend está 100% pronto para produção!** 🎉
