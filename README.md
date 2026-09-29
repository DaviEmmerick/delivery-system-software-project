# delivery-system-software-project

## Quem faz o quê

| Integrante                                       | Agregado(s) / módulo(s)                     | Responsabilidade                                                  |
| ------------------------------------------------ | ------------------------------------------- | ----------------------------------------------------------------- |
| Davi França Emmerick de Souza                    | Dominio / entidades / regras de negócio     | Estrutura do domínio, entidades e validações                      |
| Leandro Machado                                  | Infraestrutura / ambiente                   | Configuração do projeto e suporte ao repositório                  |
| João Gabriel de Azevedo                          | Testes unitários / domínio                  | Implementação da suíte de testes unitários e qualidade do domínio |
| Victor Antunes dos Santos (@VictorAntunesCastro) | Camada de serviço, entrypoints e testes e2e | Orquestração de casos de uso, API Flask e testes de ponta a ponta |

## Visão geral

Este projeto implementa uma base inicial de domínio para um sistema de delivery, com foco em entidades e regras de negócio antes da camada de serviços e interfaces.

## Como executar os testes

Para executar a suíte completa de testes automatizados com o `pytest`, execute:

```bash
pytest
```

Para executar apenas os testes unitários com saída detalhada:

```bash
pytest -v tests/unit
```
