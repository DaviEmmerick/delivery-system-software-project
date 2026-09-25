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

### João Gabriel de Azevedo

#### O que implementei
- Criação e estruturação da suíte de testes unitários para todas as entidades de domínio (`Cliente`, `Endereco`, `Entrega`, `Pedido`, `Produto` e `Restaurante`)
- Cobertura completa de casos de sucesso, sanitização de dados (remoção de espaços com `strip`) e validações de regras de negócio com lançamento de exceções (`ValueError`)
- Configuração e ajuste do ambiente de execução do `pytest` (`pytest.ini` e `tests/pytest.ini`) para permitir execução transparente dos testes a partir da raiz do projeto

#### Por que
- Para assegurar a integridade e confiabilidade das regras de negócio do núcleo da aplicação
- Para prevenir regressões e garantir que dados ou comportamentos inválidos sejam devidamente barrados pelas entidades de domínio
- Para viabilizar feedback rápido e contínuo durante a evolução do sistema

#### Arquivos alterados

Arquivos Python:
- `tests/unit/test_cliente.py`
- `tests/unit/test_endereco.py`
- `tests/unit/test_entrega.py`
- `tests/unit/test_pedido.py`
- `tests/unit/test_produto.py`
- `tests/unit/test_restaurante.py`

Arquivos de Configuração:
- `pytest.ini`
- `tests/pytest.ini`

Arquivos Markdown:
- `DECISIONS.md`

#### Commits relevantes
- `b87b6fb` — Add: Adicionados testes unitários para as entidades Cliente, Endereco, Entrega, Pedido, Produto e Restaurante

#### Uso de IA
- Usei IA para auxiliar no planejamento e estruturação dos cenários de testes unitários de cada entidade de domínio.
- Também usei IA para revisar a documentação final e ajustar a redação das decisões do projeto, sem substituir a implementação ou a decisão final do grupo.


### Leandro Machado Cardoso da Cunha

#### O que implementei
- Criei uma workflow de GitHub Actions para executar a suíte de testes em cada push e pull request na branch `main`
- Configurei a execução em ambiente Ubuntu com Python 3.12
- Instalei as dependências automaticamente a partir do `requirements.txt`
- Defini a execução do pytest com o `PYTHONPATH=src` para garantir que os módulos do projeto sejam importados corretamente

#### Por que
- Para garantir que qualquer alteração na branch principal seja validada automaticamente
- Para padronizar o ambiente de testes entre desenvolvimento e integração contínua
- Para reduzir erros de configuração e evitar que código quebrado seja mergeado sem validação
- Para manter o processo de qualidade com feedback rápido durante o desenvolvimento

#### Arquivos alterados

Arquivos de workflow:
- `.github/workflows/ci.yml`

Arquivos de configuração:
- `pytest.ini`
- `requirements.txt`

Arquivos Markdown:
- `DECISIONS.md`

#### Commits relevantes
- `41cd01f` — Feat: Implementando a esteira de testes
- `5b14a36` — Fix: Corrigindo versão do python e modelo do runner(ubunto)
- `708246a` — Fix: Corrigindo o nome do runner(ubuntu)
- `43880e2` — Fix: Corrigindo o uses para a versão 5
- `3676927` — Fix: Corrigindo o uses para a versão actions/checkout@v4
- `55b0604` — Fix: Corrigindo o uses para a versão python3.12
- `04f429a` — Fix: Corrigindo o nome do actions/setup-python@v5

#### Uso de IA
- Usei IA para ajustar a redação desta decisão de forma clara e objetiva, sem substituir a escolha técnica final do grupo.

