# Sistema de Delivery

Projeto acadêmico de um sistema de delivery que organiza clientes, restaurantes, pedidos e entregas. A aplicação separa as regras de negócio do domínio, os casos de uso, a API HTTP e a persistência.

## Funcionalidades

- Cadastro e consulta de clientes, com endereço opcional.
- Cadastro e listagem de restaurantes e seus produtos.
- Criação e consulta de pedidos, com itens, quantidades, subtotais e total.
- Acompanhamento e atualização do status da entrega, respeitando transições válidas.
- Registro e consulta do histórico de mudanças de status da entrega.
- Validação de dados no domínio e persistência com SQLAlchemy/SQLite.

## Contribuições dos integrantes

| Integrante | Funcionalidades e responsabilidades |
| --- | --- |
| **Davi França Emmerick de Souza** ([@DaviEmmerick](https://github.com/DaviEmmerick)) | Modelagem do domínio e dos agregados; entidades e regras de negócio de clientes, endereços, pedidos, produtos, restaurantes e entregas; objetos de valor imutáveis e `PedidoFactory`; estratégias de cálculo de preço (`Strategy`), incluindo preço regular e desconto percentual. |
| **Leandro Machado Cardoso da Cunha** ([@LeandroMachadoCC](https://github.com/LeandroMachadoCC)) | Validação e normalização dos dados no domínio, incluindo validação de tipos, textos e preços; configuração do ambiente de testes e integração contínua com GitHub Actions. |
| **João Gabriel de Azevedo** ([@JoaoGAzevedo](https://github.com/JoaoGAzevedo)) | Testes unitários das entidades e regras do domínio, incluindo casos inválidos, imutabilidade e igualdade por valor; segregação dos contratos de repositório em interfaces de leitura, listagem e escrita (ISP). |
| **Victor Antunes dos Santos** ([@VictorAntunesCastro](https://github.com/VictorAntunesCastro)) | Camada de serviços e casos de uso; API REST Flask; testes unitários de serviços e testes E2E; publicação de eventos de entrega com Observer, notificações e consulta do histórico de status. |

## API

A API Flask disponibiliza os seguintes endpoints:

| Método | Endpoint | Descrição |
| --- | --- | --- |
| `POST` | `/clientes` | Cadastra um cliente |
| `GET` | `/clientes/<cliente_id>` | Consulta um cliente |
| `GET` | `/clientes/<cliente_id>/pedidos` | Lista os pedidos de um cliente |
| `POST` | `/restaurantes` | Cadastra um restaurante |
| `GET` | `/restaurantes` | Lista os restaurantes |
| `POST` | `/pedidos` | Cria um pedido |
| `GET` | `/pedidos/<pedido_id>` | Consulta um pedido e o status da entrega |
| `PATCH` | `/pedidos/<pedido_id>/entrega` | Atualiza o status da entrega |
| `GET` | `/pedidos/<pedido_id>/entrega/historico` | Consulta o histórico de status da entrega |

As respostas de erro usam códigos HTTP apropriados para dados inválidos, recursos não encontrados e conflitos.

## Como executar

Requer Python 3.12 ou compatível com as dependências do projeto.

```bash
python -m pip install -r requirements.txt
python -m src.entrypoints.flask_app
```

A API será iniciada em `http://127.0.0.1:5000`. Por padrão, a aplicação usa SQLite em memória.

## Testes

Execute toda a suíte automatizada:

```bash
pytest
```

Para executar somente os testes unitários:

```bash
pytest -v tests/unit
```

Os testes também cobrem a API (E2E) e a integração com os repositórios.

## Documentação

- [Proposta do projeto](PROPOSTA.md)
- [Arquitetura](docs/arquitetura.md)
- [Padrões GoF](docs/gof.md)
- [Princípios SOLID](docs/solid.md)
- [Decisões do projeto e autorrelatos](DECISIONS.md)
