# Decisões do Projeto

## Parte 1 - decisões iniciais

### Davi França Emmerick de Souza

#### O que implementei
- Estrutura inicial do domínio do sistema de delivery
- Criação das entidades de Cliente, Produto e Pedido
- Definição das regras básicas de validação do domínio

#### Por que
- Para manter o núcleo do sistema simples, testável e independente de infraestrutura
- Para garantir que as regras de negócio fiquem centralizadas antes da implementação de serviços e interfaces

#### Arquivos alterados

Arquivos Python:
- `src/domain/model.py`
- `src/domain/entities/__init__.py`
- `src/domain/entities/cliente.py`
- `src/domain/entities/endereco.py`
- `src/domain/entities/entrega.py`
- `src/domain/entities/pedido.py`
- `src/domain/entities/produto.py`
- `src/domain/entities/restaurante.py`

Arquivos Markdown:
- `README.md`
- `PROPOSTA.md`
- `DECISIONS.md`

#### Commits relevantes
- `a063097` — [Feat] Entidades: restaurante, endereço e entrega v0
- `118b56a` — [Feat] git ignore
- `5efa26f` — [Feat] Funcionalidades básicas das entidades do sistema
- `1479db0` — [Fix] Definição das entidades
- `37640ce` — [Docs] Responsabilidades iniciais
- `16b587c` — [Docs] Ideia inicial do projeto - sem definir as decisões técnicas ainda
- `af33cf0` — [Feat] Estrutura base do projeto - Sistema de Delivery

#### Uso de IA
- Usei IA como apoio para fazer brainstorming inicial sobre o domínio do projeto, gerando ideias e levantando possibilidades de entidades e agregados.
- Também usei IA para revisar a documentação final e ajustar a redação das decisões do projeto, sem substituir a implementação ou a decisão final do grupo.