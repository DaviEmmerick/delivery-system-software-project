# ADR 0003: Separação entre Entrypoint Flask e Service Layer com Injeção de Repositórios

- **Responsável:** Victor Antunes dos Santos (`@VictorAntunesCastro`)
- **Status:** decisão implementada na Fase 1
- **Data:** 22/10/2026

## Contexto

O sistema de delivery precisa expor seus casos de uso (cadastro e consulta de clientes, cadastro e listagem de restaurantes, criação e consulta de pedidos, listagem de pedidos por cliente e consulta/atualização de status de entrega) por meio de uma API HTTP REST em Flask.

Se as regras de orquestração (como verificar duplicidade de telefone de cliente ou nome de restaurante, validar existência prévia do cliente ao criar um pedido e inicializar a entrega com status `"pendente"`) estivessem misturadas dentro das funções de rota do Flask ou acopladas diretamente a sessões do SQLAlchemy, qualquer teste de caso de uso exigiria subir o cliente de teste HTTP e criar tabelas no SQLite. Além disso, o tratamento de erros HTTP ficaria repetido em cada endpoint.

## Decisão

1. **Orquestração isolada na camada de serviços (`src/service_layer/services.py`):**
   - Implementar os 9 casos de uso como funções independentes de transporte HTTP (`criar_cliente`, `consultar_cliente`, `criar_restaurante`, `listar_restaurantes`, `criar_pedido`, `consultar_pedido`, `listar_pedidos_do_cliente`, `consultar_status_entrega` e `atualizar_status_entrega`).
   - Receber explicitamente por parâmetro as dependências de persistência (`cliente_repo`, `restaurante_repo`, `pedido_repo` tipados com `AbstractRepository`) e o dicionário `entregas: dict[str, Entrega]`, sem instanciar engine ou sessão do SQLAlchemy dentro da camada de serviço.
2. **Exceções semânticas de negócio:**
   - Declarar `NaoEncontrado(ValueError)` e `Conflito(ValueError)` em `src/service_layer/services.py` para sinalizar falhas de busca e violações de unicidade sem acoplar o serviço a códigos de status HTTP.
3. **Entrypoint HTTP fino com Application Factory (`src/entrypoints/flask_app.py`):**
   - Estruturar a aplicação Flask por meio de `create_app(cliente_repo=None, restaurante_repo=None, pedido_repo=None, entregas=None)`, instanciando `create_sqlite_engine()` e os repositórios SQLAlchemy apenas quando nenhuma implementação é injetada.
   - Restringir as rotas HTTP à leitura/validação estrutural do payload JSON (`_corpo_json` e `_texto`), chamada da função correspondente em `services.py` e serialização da resposta com `jsonify`.
   - Centralizar o mapeamento de exceções em `@app.errorhandler`: `NaoEncontrado` para HTTP `404`, `Conflito` para HTTP `409`, `ValueError` (incluindo erros de validação do domínio) para HTTP `400` e `HTTPException` para JSON padronizado `{"erro": ...}`.
4. **Estratégia de testes em dois níveis (`FakeRepository` vs E2E):**
   - Testar exaustivamente os casos de uso e casos de borda na suíte unitária (`tests/unit/test_services.py`) injetando um `FakeRepository` em memória que herda de `AbstractRepository`.
   - Validar o contrato HTTP, códigos de status e integração real com SQLite na suíte ponta a ponta (`tests/e2e/test_api.py`).

## Alternativas consideradas

- **Transaction Script direto nas rotas do Flask:** implementar validações, consultas e `session.add()` diretamente nas funções decoradas com `@app.post` e `@app.get`. Foi descartada por acoplar regras de orquestração ao contexto de requisição do Flask e dificultar testes unitários sem HTTP.
- **Instanciação direta dos repositórios SQLAlchemy dentro de `services.py`:** evitaria passar `cliente_repo`, `pedido_repo` e `restaurante_repo` como argumentos em cada chamada, mas impediria o uso direto do `FakeRepository` nos testes unitários sem recorrer a monkeypatching (`unittest.mock.patch`).
- **Retorno de tuplas `(dict, int)` pela camada de serviço:** simplificaria as rotas do Flask, mas vazaria semântica de protocolo HTTP (códigos `201`, `400`, `404`, `409`) para dentro da camada de serviço.

## Consequências

- **Positivas:**
  - Os 33 testes unitários da camada de serviço (`tests/unit/test_services.py`) executam inteiramente em memória usando uma implementação de `FakeRepository` de apenas 11 linhas (`linhas 5–15`), sem iniciar o Flask nem o SQLAlchemy.
  - O tratamento de erros na API ficou uniforme: qualquer `ValueError` levantado pelas entidades de domínio ou pelos serviços é convertido automaticamente em HTTP `400` com corpo JSON `{"erro": ...}` por um único handler em `flask_app.py` (`linhas 35–50`).
  - A fábrica `create_app` permite tanto execução padrão com SQLite em memória quanto injeção de dependências alternativas em testes.
- **Negativas e trade-offs:**
  - As assinaturas das funções de serviço ficaram mais verbosas (por exemplo, `criar_pedido` recebe 5 parâmetros, incluindo dois repositórios e o dicionário `entregas`), pois o projeto não utiliza um container de injeção de dependência nem o padrão Unit of Work.
  - A verificação de unicidade em `criar_cliente` e `criar_restaurante` percorre `repo.list()` em memória na camada de serviço (`services.py`, linhas 27 e 47), o que é simples e funciona igualmente no `FakeRepository` e no `SQLAlchemyRepository`, mas teria custo $O(n)$ em bancos grandes caso não houvesse método específico de busca por atributo no repositório.
  - O estado das entregas (`entregas: dict[str, Entrega]`) é mantido em um dicionário em memória separado do `PedidoRepository`, o que significa que a criação do pedido e o registro da entrega (`services.py`, linhas 82–83) não compartilham uma transação atômica no banco de dados.

## Evidências

- `9849b96` — implementação inicial da camada de serviços em `src/service_layer/services.py` com injeção explícita de repositórios e exceções `NaoEncontrado` e `Conflito`.
- `ab5eec4` — implementação da API Flask em `src/entrypoints/flask_app.py`, suíte unitária de serviços com `FakeRepository` em `tests/unit/test_services.py` e suíte E2E em `tests/e2e/test_api.py`.
- `e4ecb22`, `937bad5` e `1213e36` — refinamento do tratamento de erros na API Flask, padronização das respostas JSON de erro e envio direto de `cliente_id` na criação de pedidos.

