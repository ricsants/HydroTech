# 💧 HydroTech API

API REST para gerenciamento e monitoramento de rios, desenvolvida com **Django** e **Django REST Framework**.

---

## 📋 Sumário

- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Execução](#-instalação-e-execução)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Rotas da API](#-rotas-da-api)
  - [Autenticação](#autenticação)
  - [Usuários](#usuários)
  - [Rios](#rios)
- [Exemplos de Requisição](#-exemplos-de-requisição)
- [Estrutura do Projeto](#-estrutura-do-projeto)

---

## 🚀 Tecnologias

- [Python 3.10+](https://www.python.org/)
- [Django 4.x](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- SQLite (banco de dados padrão para desenvolvimento)

---

## ✅ Pré-requisitos

Certifique-se de ter instalado em sua máquina:

- Python 3.10 ou superior
- pip
- Git

---

## ⚙️ Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/ricsants/HydroTech.git
cd HydroTech
```

### 2. Crie e ative um ambiente virtual

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute as migrações

```bash
python manage.py migrate
```

### 5. (Opcional) Crie um superusuário

```bash
python manage.py createsuperuser
```

### 6. Inicie o servidor

```bash
python manage.py runserver
```

A API estará disponível em: `http://127.0.0.1:8000/`


## 🗺️ Rotas da API

Base URL: `http://127.0.0.1:8000/`

### Usuários

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|--------------|
| `POST` | `/usuarios/` | Cadastra um novo usuário
| `GET` | `/usuarios/` | Retorna dados do usuário autenticado
| `PUT` | `/usuarios/{id}` | Atualiza dados do usuário autenticado

#### Exemplo de cadastro

```http
POST /usuarios/
Content-Type: application/json

{
  "username": "lucas",
  "email": "lucas@email.com",
  "password": "senha123"
}
```

---

### Rios

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|--------------|
| `GET` | `/rios/` | Lista todos os rios
| `POST` | `/rios/` | Cadastra um novo rio 
| `GET` | `/rios/{id}/` | Retorna detalhes de um rio 
| `PUT` | `/rios/{id}/` | Atualiza todos os dados de um rio 
| `PATCH` | `/rios/{id}/` | Atualiza parcialmente um rio 
| `DELETE` | `/rios/{id}/` | Remove um rio 

#### Exemplo de criação de rio

```http
POST /rios/
Authorization: Bearer <token>
Content-Type: application/json

{
  "nome": "Rio Paraná",
  "estado": "SP",
  "extensao_km": 4880,
  "descricao": "Um dos maiores rios da América do Sul."
}
```

#### Exemplo de listagem com filtro

```http
GET /rios/?estado=SP
```

---

## 💡 Exemplos de Requisição com cURL

### Listar rios
```bash
curl http://127.0.0.1:8000/rios/ \
```

### Criar rio
```bash
curl -X POST http://127.0.0.1:8000/rios/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "Rio Tietê", "estado": "SP"}'
```

### Deletar rio
```bash
curl -X DELETE http://127.0.0.1:8000/rios/1/ \
```

---

## 📁 Estrutura do Projeto

```
HydroTech/
├── app/                  # Configurações principais do Django
│   ├── settings.py       # Configurações do projeto
│   ├── urls.py           # Roteamento principal
│   └── wsgi.py
├── rios/                 # App de gerenciamento de rios
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── usuarios/             # App de autenticação e usuários
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── manage.py
├── requirements.txt
├── db.sqlite3
└── .gitignore
```


