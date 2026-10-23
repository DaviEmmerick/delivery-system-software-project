# delivery-system-software-project

## Quem faz o quê

| Integrante                                       | Agregado(s) / módulo(s)                     | Responsabilidade                                                  |
| ------------------------------------------------ | ------------------------------------------- | ----------------------------------------------------------------- |
| Davi França Emmerick de Souza                    | Domínio / entidades / regras de negócio      | Estrutura do domínio, entidades, agregados e validações            |
| Leandro Machado                                  | Infraestrutura / ambiente                   | Configuração do projeto, CI e suporte ao repositório              |
| João Gabriel de Azevedo                          | Testes unitários / domínio                  | Implementação da suíte de testes unitários e qualidade do domínio |
| Victor Antunes dos Santos (@VictorAntunesCastro) | Camada de serviço, entrypoints e testes e2e | Orquestração de casos de uso, API Flask e testes de ponta a ponta |

## Visão geral

Este projeto implementa um sistema de delivery com entidades e regras de domínio, uma camada de serviços, uma API REST em Flask e adapters de persistência com SQLAlchemy. A suíte de testes cobre o domínio e os serviços, a API e a integração com SQLite.

## Como executar os testes

Para executar a suíte completa de testes automatizados com o `pytest`, execute:

```bash
pytest
```

Para executar apenas os testes unitários com saída detalhada:

```bash
pytest -v tests/unit
```
