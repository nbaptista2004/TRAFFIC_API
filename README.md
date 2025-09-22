Traffic API:

API REST desenvolvida em Django + Django Rest Framework para gestão de segmentos de estrada, leituras de velocidade e integração de sensores de tráfego móveis.

http://127.0.0.1:8000/admin/
→ Django Admin (Username: admin Password: admin)

http://127.0.0.1:8000/api/docs/
→ Swagger UI

http://127.0.0.1:8000/api/segments/
→ endpoint dos segmentos

http://127.0.0.1:8000/api/readings/
→ endpoint das leituras

Funcionalidades:

Parte 1 – API Base:

CRUD de segmentos de estrada com permissões por tipo de utilizador.
CRUD de leituras de velocidade média associadas a segmentos.
Retorno do número de leituras por segmento.
Swagger UI disponível em /api/docs.
Gestão de utilizadores via Django Admin.

Parte 2 – Testes e Filtros:

Testes unitários que validam permissões e operações da API.
Endpoint para filtrar segmentos pela intensidade da última leitura.

Parte 3 – Integração de Sensores:

Modelo de sensores móveis com UUID.
Modelo de carros (registados automaticamente).
Endpoint POST /passages/bulk/ que recebe registos em batch enviados pelos sensores.
Endpoint GET /passages/by-car/?license_plate=XXX que devolve passagens de um carro nas últimas 24h.
Autenticação de sensores via API Key (X-API-KEY: 23231c7a-80a7-4810-93b3-98a18ecfbc42).
