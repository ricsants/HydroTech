# API de Pontos de Risco - Guia de Uso

## Visão Geral
Sistema de criação e gerenciamento de pontos de risco de alagamento em rios. Apenas **Defesa Civil** e **Admin** podem criar/editar/deletar pontos de risco.

## Permissões
- **GET** (listar/visualizar): Qualquer usuário autenticado
- **POST** (criar): Apenas Defesa Civil + Admin
- **PUT/PATCH** (editar): Apenas Defesa Civil + Admin + criador original
- **DELETE**: Apenas Defesa Civil + Admin + criador original

## Credenciais

### Defesa Civil
```
Email: defesa_civil@hidrotech.com
Senha: defesa123
API Token: oLnZ7mM3O5-XRn-7kiN_FqhRRfYREC4u1SqX-O96YKY
```

### Admin
```
Username: admin
Senha: admin123
Email: admin@example.com
```

## Endpoints

### 1. Listar Pontos de Risco de um Rio
```bash
GET /rios/{rio_id}/pontos-risco/

curl -H "Authorization: Bearer {token}" \
  http://127.0.0.1:8000/rios/1/pontos-risco/
```

**Resposta:**
```json
[
  {
    "id": 1,
    "rio": 1,
    "rio_nome": "Tietê",
    "latitude": -23.5505,
    "longitude": -46.6333,
    "descricao": "Ponto crítico de inundação próximo ao centro",
    "nivel_risco": 3,
    "criado_por": 2,
    "criado_por_nome": "Defesa Civil",
    "criado_em": "2026-05-02T10:30:00Z",
    "atualizado_em": "2026-05-02T10:30:00Z"
  }
]
```

### 2. Criar Ponto de Risco (Defesa Civil/Admin)
```bash
POST /rios/{rio_id}/pontos-risco/

curl -X POST \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "rio": 1,
    "latitude": -23.5505,
    "longitude": -46.6333,
    "descricao": "Ponto crítico de inundação próximo ao centro",
    "nivel_risco": 3
  }' \
  http://127.0.0.1:8000/rios/1/pontos-risco/
```

**Níveis de Risco:**
- 1 = Baixo
- 2 = Médio
- 3 = Alto

### 3. Obter Detalhes de um Ponto de Risco
```bash
GET /pontos-risco/{ponto_id}/

curl -H "Authorization: Bearer {token}" \
  http://127.0.0.1:8000/pontos-risco/1/
```

### 4. Atualizar Ponto de Risco (Defesa Civil/Admin/Criador)
```bash
PUT /pontos-risco/{ponto_id}/

curl -X PUT \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "rio": 1,
    "latitude": -23.5506,
    "longitude": -46.6334,
    "descricao": "Descrição atualizada",
    "nivel_risco": 2
  }' \
  http://127.0.0.1:8000/pontos-risco/1/
```

### 5. Deletar Ponto de Risco (Defesa Civil/Admin/Criador)
```bash
DELETE /pontos-risco/{ponto_id}/

curl -X DELETE \
  -H "Authorization: Bearer {token}" \
  http://127.0.0.1:8000/pontos-risco/1/
```

## Exemplos com Postman

### Login Defesa Civil
```
POST http://127.0.0.1:8000/auth/login/
Content-Type: application/json

{
  "username": "defesa_civil@hidrotech.com",
  "password": "defesa123"
}
```

Copie o `access` token da resposta.

### Usar Token no Header
```
Authorization: Bearer {seu_token_jwt}
```

## Fluxo de Trabalho

1. **Defesa Civil faz login** e obtém JWT token
2. **Defesa Civil cria pontos de risco** em rios já cadastrados
3. **Usuários normais consultam** pontos de risco via GET
4. **Admin gerencia** todos os pontos de risco

## Estrutura de Dados

### PontoRisco
```python
{
  "id": int,                    # ID do ponto de risco
  "rio": int,                   # ID do rio
  "rio_nome": str,              # Nome do rio (somente leitura)
  "latitude": float,            # Coordenada Y
  "longitude": float,           # Coordenada X
  "descricao": str,             # Descrição do ponto
  "nivel_risco": int,           # 1=Baixo, 2=Médio, 3=Alto
  "criado_por": int,            # ID do usuário that criou
  "criado_por_nome": str,       # Nome do usuário (somente leitura)
  "criado_em": datetime,        # Data/hora de criação
  "atualizado_em": datetime     # Data/hora da última atualização
}
```

## Permissões Detalhadas

### IsDefesaCivilAdminOrOwner
- **GET**: ✅ Todos os usuários autenticados
- **POST**: ✅ Apenas Defesa Civil + Admin
- **PUT/PATCH**: ✅ Apenas criador + Admin + Defesa Civil
- **DELETE**: ✅ Apenas criador + Admin

## Códigos HTTP Esperados

| Código | Significado |
|--------|------------|
| 200 | OK - Sucesso |
| 201 | Created - Recurso criado |
| 204 | No Content - Deletado com sucesso |
| 400 | Bad Request - Dados inválidos |
| 401 | Unauthorized - Token ausente/inválido |
| 403 | Forbidden - Sem permissão |
| 404 | Not Found - Recurso não existe |

## Notas
- O campo `criado_por` é preenchido automaticamente com o usuário autenticado
- Não é necessário passar `criado_por`, `criado_em` ou `atualizado_em` nas requisições - são gerados automaticamente
- Rio ID deve ser válido e existir no banco de dados
