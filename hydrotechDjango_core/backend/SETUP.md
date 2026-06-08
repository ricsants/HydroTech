# Guia de Setup e Deployment - Backend HydroTech

## 1. Setup Local (Desenvolvimento)

### Pré-requisitos
- Python 3.11+
- pip ou poetry
- Git

### Instalação

1. **Clone o repositório e navegue até o backend:**
```bash
cd hydrotechDjango_core/backend
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o .env se necessário para desenvolvimento local
```

5. **Execute as migrações:**
```bash
python manage.py migrate
```

6. **Crie um superuser (admin):**
```bash
python manage.py createsuperuser
```

7. **Inicie o servidor:**
```bash
python manage.py runserver
```

O backend estará disponível em `http://localhost:8000`

O painel admin estará em `http://localhost:8000/admin`

## 2. Setup com Docker (Recomendado para Produção)

### Pré-requisitos
- Docker
- Docker Compose

### Instalação

1. **Navegue até o diretório backend:**
```bash
cd hydrotechDjango_core/backend
```

2. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env.prod
# Edite .env.prod com configurações de produção
```

3. **Inicie os containers:**
```bash
docker-compose up -d
```

4. **Execute as migrações:**
```bash
docker-compose exec web python manage.py migrate
```

5. **Crie um superuser:**
```bash
docker-compose exec web python manage.py createsuperuser
```

6. **Recolha arquivos estáticos:**
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

O backend estará disponível em `http://localhost:8000`

## 3. Variáveis de Ambiente

O arquivo `.env` controla as seguintes configurações:

### Segurança
- `DEBUG`: Deve ser `False` em produção
- `SECRET_KEY`: Chave secreta única para seu projeto
- `ALLOWED_HOSTS`: Lista de hosts permitidos

### Banco de Dados
- `DATABASE_ENGINE`: Engine do banco de dados
- `DATABASE_NAME`: Nome do banco de dados
- `DATABASE_USER`: Usuário do banco (para PostgreSQL)
- `DATABASE_PASSWORD`: Senha do banco (para PostgreSQL)
- `DATABASE_HOST`: Host do banco (para PostgreSQL)
- `DATABASE_PORT`: Porta do banco (para PostgreSQL)

### Autenticação
- `JWT_ACCESS_TOKEN_LIFETIME`: Tempo de vida do token de acesso (em minutos)
- `JWT_REFRESH_TOKEN_LIFETIME`: Tempo de vida do token de refresh (em dias)

### CORS
- `CORS_ALLOWED_ORIGINS`: URLs permitidas para CORS (separadas por vírgula)
- `FRONTEND_URL`: URL do frontend

### Email
- `EMAIL_BACKEND`: Backend de email
- `EMAIL_HOST`: Host SMTP
- `EMAIL_PORT`: Porta SMTP
- `EMAIL_HOST_USER`: Usuário do email
- `EMAIL_HOST_PASSWORD`: Senha do email

## 4. Endpoints Principais

### Autenticação
- `POST /auth/login/` - Login de usuário
- `POST /auth/register/` - Registro de novo usuário
- `POST /auth/refresh/` - Renovar token
- `GET /auth/me/` - Obter dados do usuário logado

### Usuários
- `GET /usuarios/` - Listar usuários (apenas admin)
- `GET /usuarios/<id>/` - Obter dados do usuário
- `PUT /usuarios/<id>/` - Atualizar usuário
- `DELETE /usuarios/<id>/` - Deletar usuário

### Rios
- `GET /rios/` - Listar rios
- `POST /rios/` - Criar novo rio
- `GET /rios/<id>/` - Obter dados do rio
- `PUT /rios/<id>/` - Atualizar rio
- `DELETE /rios/<id>/` - Deletar rio
- `POST /rios/<id>/favorite/` - Adicionar/remover de favoritos

### Pontos de Risco
- `GET /rios/<rio_id>/pontos-risco/` - Listar pontos de risco
- `POST /rios/<rio_id>/pontos-risco/` - Criar ponto de risco
- `GET /pontos-risco/<id>/` - Obter dados do ponto
- `PUT /pontos-risco/<id>/` - Atualizar ponto
- `DELETE /pontos-risco/<id>/` - Deletar ponto

## 5. Migração para PostgreSQL

Se estiver usando SQLite em desenvolvimento e quiser usar PostgreSQL:

1. **Atualize a variável de ambiente:**
```env
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=hydrotech_db
DATABASE_USER=seu_usuario
DATABASE_PASSWORD=sua_senha
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

2. **Instale o driver PostgreSQL:**
```bash
pip install psycopg2-binary
```

3. **Execute as migrações:**
```bash
python manage.py migrate
```

## 6. Logs

Os logs são salvos em `backend/logs/django.log` e também são exibidos no console.

Configure o nível de log com a variável `LOG_LEVEL`:
- `DEBUG`: Informações detalhadas para debug
- `INFO`: Informações gerais
- `WARNING`: Avisos
- `ERROR`: Erros

## 7. Checklist de Segurança para Produção

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` gerada aleatoriamente e segura
- [ ] `ALLOWED_HOSTS` configurado corretamente
- [ ] HTTPS ativado
- [ ] Banco de dados PostgreSQL ou similar
- [ ] Variáveis de ambiente em arquivo seguro (não commitado)
- [ ] Backups do banco de dados configurados
- [ ] Logs centralizados configurados
- [ ] Rate limiting configurado
- [ ] CORS adequadamente configurado

## 8. Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Erro: "django.db.utils.OperationalError: FATAL: Ident authentication failed"
Verifique as credenciais do PostgreSQL no `.env`

### Erro: "CORS not allowed"
Verifique se `CORS_ALLOWED_ORIGINS` inclui seu frontend URL

### Erro ao executar migrations
```bash
python manage.py migrate --run-syncdb
```

## 9. Comandos Úteis

```bash
# Criar novo app
python manage.py startapp nome_app

# Fazer migrations
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate

# Testar o backend
python manage.py test

# Shell interativo Django
python manage.py shell

# Limpar banco de dados
python manage.py flush

# Recolher arquivos estáticos
python manage.py collectstatic --noinput
```
