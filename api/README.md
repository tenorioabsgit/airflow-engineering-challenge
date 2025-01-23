# API de Teste - Sistema de Vendas

Esta é uma API REST que simula um sistema de vendas com produtos, carrinhos, clientes e logística.

## Endpoints Disponíveis

### Autenticação

Para acessar os endpoints da API, você precisa obter um token de acesso:

**Login para obter token:**
```
POST /token

Body (form-data):
username: admin
password: admin

Resposta:
{
    "access_token": "seu_token_jwt",
    "refresh_token": "seu_refresh_token",
    "token_type": "bearer"
}
```

**Renovar token expirado:**
```
POST /refresh-token
Header: Authorization: Bearer seu_refresh_token

Resposta:
{
    "access_token": "novo_token_jwt",
    "token_type": "bearer"
}
```

### Endpoints da API

Todos os endpoints requerem autenticação via Bearer token no header:
```
Authorization: Bearer seu_token_jwt
```

#### Produtos
```
GET /api/v1/products?skip=0&limit=50

Resposta:
[
    {
        "category": "Casa & Decora\u00e7\u00e3o",
        "name": "Maiores explicabo.",
        "created_at": "2025-01-22T20:16:16.618630",
        "price": 2431.76,
        "id": 654
    }
]
```

#### Carrinhos/Vendas
```
GET /api/v1/carts?skip=0&limit=50

Resposta:
[
    {
        "id": 1,
        "sale_date": "2023-03-20T18:36:26.596781",
        "total_amount": 5111.08,
        "shipping_info": {},
        "created_at": "2025-01-22T20:16:23.783600",
        "status": "APPROVED",
        "customer_id": 1409,
        "logistic_id": 8,
        "items": [ ],
        "payment_info": {}
    }
]
```

#### Clientes
```
GET /api/v1/customer?skip=0&limit=50

Resposta:
[
    {
        "phone": "+55 21 7122 8587",
        "id": 2,
        "full_name": "Rafael Camargo",
        "city": "Dias Alegre",
        "address": "Vila de Machado, 90",
        "email": "bmoreira@example.net",
        "created_at": "2025-01-22T20:16:16.627947"
    }
]
```

#### Logística
```
GET /api/v1/logistict?skip=0&limit=50

Resposta:
[
    {
        "company_name": "Cassiano Mendes - ME",
        "service_type": "Normal",
        "origin_warehouse": "Rezende de Machado",
        "contact_phone": "+55 41 0420-2451",
        "id": 8,
        "created_at": "2025-01-22T20:16:23.769077"
    }
]
```

## Paginação

Todos os endpoints suportam paginação através dos parâmetros:
- `skip`: número de registros para pular (default: 0)
- `limit`: número de registros por página (default: 50, máximo: 50)

## Observações Importantes

1. A API pode apresentar instabilidades e retornar erros 500 de forma aleatória
2. Implemente tratamento adequado de erros e retentativas
3. O token de acesso expira em 30 minutos
4. Use o refresh_token para obter um novo token de acesso quando necessário
5. Todos os timestamps estão em UTC 