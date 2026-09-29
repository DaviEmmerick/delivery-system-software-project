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

### Victor Antunes dos Santos (@VictorAntunesCastro)

#### O que implementei

- Desenvolvimento da camada de serviço completa com 9 casos de uso (criação e consulta de clientes, restaurantes, pedidos e atualização de status de entrega)
- Implementação da API REST utilizando Flask com 8 endpoints mapeados e orquestração de tratamento de exceções (como `NaoEncontrado` e `Conflito`)
- Criação da suíte de testes de ponta a ponta (E2E) para validar a API e testes unitários isolados para os serviços
- _Nota de autoria: Devido a uma configuração local, alguns dos meus commits iniciais foram assinados com o usuário `VictorAntunes7`, mas todos pertencem à minha conta oficial vinculada a este projeto (`@VictorAntunesCastro`)._

#### Por que

- Para garantir que a lógica de orquestração ficasse completamente isolada de frameworks (Flask) e de bancos de dados reais, decidindo injetar as instâncias de repositório como parâmetros nas funções
- Para viabilizar a validação de todas as regras de negócio em milissegundos utilizando o `FakeRepository` nos testes unitários

#### Arquivos alterados

Arquivos Python:

- `src/service_layer/services.py`
- `src/entrypoints/flask_app.py`
- `tests/unit/test_services.py`
- `tests/e2e/test_api.py`

#### Commits relevantes

- `9849b96` a `ab5eec4` — Implementação base da camada de serviços, endpoints Flask e testes E2E
- `e4ecb22` — Refatoração da camada de serviços e ajustes de tratamento de erro na API
- `937bad5` — Fix: Restauração da estrutura dos endpoints da API Flask após corrupção gerada por conflito de merge
- `2092bf7` — Docs: Padronização do username oficial e correção de formatação

#### Uso de IA

- Utilizei IA exclusivamente para tirar dúvidas conceituais sobre o funcionamento do `pytest` com o Flask e para entender mensagens de erro do terminal (ex: `SyntaxError` durante resolução de conflitos de merge). Todo o código commitado foi escrito e validado por mim.

## Parte 2 - decisões da semana 2

### Davi França Emmerick de Souza

#### O que implementei

- Explicitei a composição do agregado Cliente, permitindo associar um Endereco ao cliente
- Tornei Endereco imutável e validei sua associação ao Cliente
- Criei ItemPedido como objeto de valor imutável, com produto, quantidade e subtotal
- Ajustei Pedido para aceitar Produtos ou ItemPedido, preservar os itens recebidos e calcular o total pelos subtotais
- Expus ItemPedido pelo módulo `src/domain/model.py`
- Os testes existentes não foram alterados neste commit; as novas regras ainda precisam de testes unitários específicos

#### Por que

- Para representar melhor os agregados Cliente e Pedido e proteger suas regras de domínio
- Para permitir quantidade por produto no pedido e manter o cálculo do total centralizado no domínio
- Para manter o modelo independente de adapters, service layer e entrypoints

#### Arquivos alterados

Arquivos Python:

- `src/domain/entities/cliente.py`
- `src/domain/entities/endereco.py`
- `src/domain/entities/item_pedido.py`
- `src/domain/entities/pedido.py`
- `src/domain/model.py`

#### Commits relevantes

- `6b53d71` — [Feat] Mudança nos agregados

#### Uso de IA

- Usei IA para revisar as regras do domínio.

## Parte 3 - decisões da semana 3

### Davi França Emmerick de Souza

#### O que implementei

- Adicionei identificadores estáveis às raízes dos agregados `Cliente`, `Pedido` e `Restaurante`
- Criei os mapeamentos ORM com SQLAlchemy para persistir os agregados e os itens do pedido
- Implementei `AbstractRepository` e repositórios SQLAlchemy com operações para adicionar, buscar e listar agregados
- Criei testes de integração com SQLite para persistir e recuperar os três agregados
- Criei `FakeRepository` para testar o contrato básico do repositório e atualizei o teste de `Pedido` para refletir seus itens como `ItemPedido`

#### Por que

- Para persistir os agregados em SQLite sem colocar dependências de banco de dados dentro do domínio
- Para validar a conversão entre os objetos do domínio e os persistidos
- Para permitir testar o contrato dos repositórios sem depender do banco nos testes unitários

#### Arquivos alterados

Arquivos Python:

- `src/domain/entities/cliente.py`
- `src/domain/entities/pedido.py`
- `src/domain/entities/restaurante.py`
- `src/adapters/__init__.py`
- `src/adapters/orm.py`
- `src/adapters/repository.py`
- `tests/fakes.py`
- `tests/unit/test_pedido.py`
- `tests/unit/test_repository.py`
- `tests/integration/test_repositories.py`

Arquivos de configuração:

- `requirements.txt`

#### Commits relevantes

- `bd56b97` — [Feat] SQLAlchemy e atualização nas dependências
- `d058f44` — [Feat] Entidades
- `ac665e3` — [Feat] Agregado dos repositórios
- `70f7257` — [Fix] Ajuste no teste, esperava uma tupla antes

#### Uso de IA

- Usei IA como apoio para estruturar e revisar os mapeamentos, repositórios e testes de persistência. As decisões finais foram ajustadas ao modelo e à estrutura do projeto.

### João Gabriel de Azevedo

#### O que implementei

- Criação da suíte de testes unitários para a nova entidade `ItemPedido`, cobrindo cálculo de subtotais, validações de integridade (tipo de produto e quantidade estritamente positiva), igualdade por valor e garantia de imutabilidade com dataclass congelada (`frozen=True`)
- Atualização e expansão dos testes unitários de `Cliente` e `Endereco`, validando a geração automática de identificador UUID hex, suporte a ID customizado, associação com a entidade `Endereco`, validação de tipos e imutabilidade de `Endereco`
- Atualização e expansão dos testes unitários de `Pedido` e `Restaurante`, validando identificadores únicos (`id`), normalização automática de itens para tuplas de `ItemPedido`, aceitação de itens como `Produto`, `ItemPedido` ou coleções mistas, cálculo dinâmico da propriedade `total` a partir dos subtotais e rejeição de itens inválidos ou coleções vazias

#### Por que

- Para assegurar que as novas regras de negócio e agregados introduzidos nas entidades e objetos de valor estejam plenamente cobertos por testes automatizados
- Para garantir que a integridade dos agregados (como geração de ID e imutabilidade de value objects) seja validada no nível de domínio
- Para prevenir regressões e assegurar que a suíte de testes continue consistente com a evolução do domínio

#### Arquivos alterados

Arquivos Python:

- `tests/unit/test_item_pedido.py`
- `tests/unit/test_cliente.py`
- `tests/unit/test_endereco.py`
- `tests/unit/test_pedido.py`
- `tests/unit/test_restaurante.py`

Arquivos Markdown:

- `DECISIONS.md`

#### Commits relevantes

- `436a8ab` — [Test] Testes unitários para a entidade ItemPedido
- `299b640` — [Test] Atualização dos testes unitários de Cliente e Endereco
- `e8f972c` — [Test] Atualização dos testes unitários de Pedido e Restaurante

#### Uso de IA

- Usei IA para apoiar no levantamento e planejamento dos cenários de teste necessários para as novas regras de negócio dos agregados.
- Também usei IA para revisar a cobertura dos casos de borda e auxiliar na redação e organização desta documentação de decisões do projeto.
