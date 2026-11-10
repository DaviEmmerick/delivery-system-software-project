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

- Adicionei identificadores estáveis às entidades `Cliente`, `Pedido` e `Restaurante`.

#### Por que

- Para que cada entidade de domínio pudesse ser identificada de forma estável.

#### Arquivos alterados

Arquivos Python:

- `src/domain/entities/cliente.py`
- `src/domain/entities/pedido.py`
- `src/domain/entities/restaurante.py`

#### Commits relevantes

- `d058f44` — [Feat] Entidades

#### Uso de IA

- Usei IA como apoio para revisar as alterações nas entidades de domínio.

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

## Parte 2 - checkpoint 1 (22/10/2026)

### Davi França Emmerick de Souza

#### O que implementei

- Documentei a análise arquitetural em `docs/arquitetura.md`, usando o código, o histórico e os testes atuais como evidência.
- Registrei em `docs/adr/0001-modelagem-dos-agregados-de-dominio.md` a decisão de modelar as entidades e regras de domínio.

#### Arquivos alterados

- `docs/arquitetura.md`
- `docs/adr/0001-modelagem-dos-agregados-de-dominio.md`
- `DECISIONS.md`

#### Commits relevantes

- `a10761d` — [Feat] arch.md, adr da modelagem e decisões.md atualizada

#### Decisão de projeto

- Modelar `Endereco` e `ItemPedido` como objetos de valor imutáveis e manter o cálculo dos subtotais e do total dentro do domínio.

#### Uso de IA

- Usei um assistente de IA para extrair os requisitos do enunciado em PDF, examinar o repositório e preparar rascunhos da documentação. Revisei as evidências contra o código, o histórico e a suíte local; os integrantes responsáveis ainda precisam validar os ADRs atribuídos a eles e registrar sua própria autoria nos commits.

### Victor Antunes dos Santos (@VictorAntunesCastro)

#### O que implementei

- Elaborei o ADR `docs/adr/0003-camada-de-servico-e-entrypoint-flask.md`, documentando a decisão de isolar a camada de serviços (`src/service_layer/services.py`) do entrypoint HTTP (`src/entrypoints/flask_app.py`) por meio da injeção explícita de repositórios (`AbstractRepository` / `FakeRepository`) e do tratamento centralizado de exceções no Flask.
- Revisei e complementei o documento `docs/arquitetura.md`, adicionando explicitamente as restrições arquiteturais do projeto (Seção 2), detalhando o papel do `FakeRepository` e o mapeamento de erros HTTP na tabela de componentes (Seção 3) e incluindo nas evidências (Seção 6) o comparativo real de desempenho entre a suíte unitária (`114` testes em `~0,14 s`) e a suíte E2E (`34` testes em `~0,32 s`), além da referência aos ADRs do grupo.

#### Arquivos alterados

- `docs/adr/0003-camada-de-servico-e-entrypoint-flask.md`
- `docs/arquitetura.md`
- `DECISIONS.md`

#### Commits relevantes

- Commits da decisão arquitetural documentada no ADR (Fase 1): `9849b96`, `ab5eec4`, `e4ecb22` e `937bad5`
- Commits deste Checkpoint 1 (Fase 2): `0753ce8` e `1246917` (adição de `docs/adr/0003-camada-de-servico-e-entrypoint-flask.md`, revisão de `docs/arquitetura.md` e atualização de `DECISIONS.md`)

#### Decisão de projeto

- Isolar a orquestração dos casos de uso em `src/service_layer/services.py` recebendo instâncias de `AbstractRepository` por parâmetro e manter `src/entrypoints/flask_app.py` como um adaptador HTTP fino com `@app.errorhandler`, permitindo validar toda a lógica de serviço em milissegundos com `FakeRepository` sem depender de Flask ou SQLite.

#### Uso de IA

- Utilizei o assistente de IA (Gemini) para revisar o docs/arquitetura.md em busca de lacunas em relação ao barema, me auxiliar na decisão arquitetural da camada de serviços e corrigir a redação do meu ADR (docs/adr/0003-camada-de-servico-e-entrypoint-flask.md) e deste autorrelato. Todo o texto foi baseado no código e nos testes que implementei na API Flask. Revisei e validei todo o conteúdo ajustado contra o código-fonte e a suíte de testes do repositório.

### João Gabriel de Azevedo

#### O que implementei

- Elaborei o ADR `docs/adr/0004-estrategia-de-testes-unitarios-e-qualidade-do-dominio.md`, documentando formalmente a decisão arquitetural da estratégia de testabilidade com testes unitários isolados no domínio puro, validação exaustiva de invariantes com parametrização do pytest e testes explícitos de imutabilidade e igualdade por valor em Value Objects.
- Registrei a referência ao ADR 0004 no documento `docs/arquitetura.md` (Seção 6), complementando as evidências de rastreabilidade das decisões do grupo.

#### Arquivos alterados

- `docs/adr/0004-estrategia-de-testes-unitarios-e-qualidade-do-dominio.md`
- `docs/arquitetura.md`
- `DECISIONS.md`

#### Commits relevantes

- Commits da decisão arquitetural documentada no ADR (Fase 1 e evolução): `b87b6fb`, `ea8cb1d`, `436a8ab`, `299b640`, `e8f972c`, `183a70f`, `4569297`, `67deecd`, `eb71869` e `13560d5`
- Commits deste Checkpoint 1 (Fase 2): criação de `docs/adr/0004-estrategia-de-testes-unitarios-e-qualidade-do-dominio.md`, atualização de `docs/arquitetura.md` e atualização de `DECISIONS.md`

#### Decisão de projeto

- Adotar uma suíte de testes unitários isolados para o domínio puro (`tests/unit/`) com pytest parametrizado, exercitando exaustivamente invariantes e casos de borda em POPOs sem acoplamento a frameworks (Flask/SQLAlchemy), assegurando feedback na ordem de microssegundos e documentação executável das regras de negócio.

#### Uso de IA

- Utilizei assistente de IA para auxiliar na estruturação e revisão do ADR `docs/adr/0004-estrategia-de-testes-unitarios-e-qualidade-do-dominio.md` e na organização deste autorrelato, com base nas implementações de testes unitários e configurações de ambiente realizadas no projeto.

## Parte 2 - checkpoint 2 (03/11/2026)

### Davi França Emmerick de Souza

#### O que implementei

- Separei a normalização de `Produto` e `ItemPedido` da entidade `Pedido`, criando `PedidoFactory` e mantendo as invariantes do agregado na entidade.
- Atualizei chamadas existentes dos testes unitários e de integração para usar a factory na criação de pedidos com `Produto`.
- Documentei a violação de SRP, a refatoração, as evidências e os custos em `docs/solid.md`.

#### Arquivos alterados

- `src/domain/entities/pedido.py`
- `src/domain/entities/pedido_factory.py`
- `docs/solid.md`
- `DECISIONS.md`

#### Commits relevantes

- Código anterior: `d058f44` — `[Feat] Entidades`.
- Commit próprio com a refatoração: a preencher depois de criar o commit.

#### Decisão de projeto

- Fazer `Pedido` aceitar somente `ItemPedido` normalizado e concentrar a conversão das formas de entrada em uma factory, separando a construção das invariantes do agregado.

#### Uso de IA

- Usei um assistente de IA para localizar a seção SOLID do enunciado, analisar o histórico e o agregado `Pedido`. Revisei a proposta contra a implementação e os testes do repositório.

### Victor Antunes dos Santos (@VictorAntunesCastro)

#### O que implementei

- Refatorei a camada de serviço (`src/service_layer/services.py`) e o entrypoint Flask (`src/entrypoints/flask_app.py`) aplicando o **Princípio da Inversão de Dependência (DIP)**, declarando o protocolo abstrato `Repositorio[T]` diretamente na camada de serviço (eliminando a dependência estática de `src.adapters.repository`) e unificando o acesso a entregas exclusivamente por meio do contrato `Repositorio[Entrega]` com a implementação em memória `EntregaMemoryRepository` (`add` / `get` / `list`).
- Atualizei e ampliei as suítes `tests/unit/test_services.py` e `tests/e2e/test_api.py` com 2 novos testes validando o protocolo `Repositorio[Entrega]` e a injeção de `EntregaMemoryRepository` em `create_app()`.
- Documentei a violação de DIP, o código anterior (`937bad5` e `1213e36`), a refatoração, a justificativa arquitetural de localização de `EntregaMemoryRepository`, a preservação de comportamento e a análise de custos em `docs/solid.md`.

#### Arquivos alterados

- `src/service_layer/services.py`
- `src/entrypoints/flask_app.py`
- `tests/unit/test_services.py`
- `tests/e2e/test_api.py`
- `docs/solid.md`
- `DECISIONS.md`

#### Commits relevantes

- Código anterior (Fase 1, antes de 06/10/2026): `e4ecb22`, `937bad5` e `1213e36`.
- Commits próprios deste Checkpoint 2: `46cdb65` (`[Refactor] Aplica DIP na camada de servicos e repositorio de entregas`), `fdc3558` (`[Docs] Documenta refatoracao DIP em solid.md e autorrelato do Checkpoint 2`) e commit de refinamento removendo o fallback de dicionário.

#### Decisão de projeto

- Definir o protocolo `Repositorio[T]` na própria camada de serviço (`src/service_layer/services.py`) e exigir que os casos de uso de pedido e entrega operem exclusivamente sobre `Repositorio[Entrega]` (sem união com `dict[str, Entrega]`), mantendo `EntregaMemoryRepository` junto ao protocolo por não possuir dependências de infraestrutura ou ORM e por preservar o escopo de arquivos do integrante.

#### Uso de IA

- Utilizei o assistente de IA (Gemini) para  identificar a violação do Princípio da Inversão de Dependência (DIP) nos módulos sob minha responsabilidade (`src/service_layer/services.py` e `src/entrypoints/flask_app.py`), estruturar a refatoração com `Repositorio[T]` e `EntregaMemoryRepository` no código e nos testes e revisar a documentação em `docs/solid.md` e neste autorrelato. Todo o código e documentação foram revisados e validados contra os requisitos do trabalho.

### João Gabriel de Azevedo 



#### O que implementei

- Refatorei o contrato de repositório da camada de serviço (`src/service_layer/services.py`) aplicando o **Princípio da Segregação de Interfaces (ISP)**, dividindo o protocolo monolítico `Repositorio[T]` em papéis granulares e coesos: `LeitorRepositorio[T]` (leitura pontual por ID), `ListadorRepositorio[T]` (listagem de coleções) e `EscritorRepositorio[T]` (adição/persistência).
- Recompus o protocolo completo `Repositorio[T]` através da herança múltipla dos protocolos segregados (`LeitorRepositorio`, `ListadorRepositorio` e `EscritorRepositorio`), assegurando 100% de compatibilidade estrutural retroativa com os repositórios existentes (`SQLAlchemyRepository`, `ClienteRepository`, `RestauranteRepository`, `PedidoRepository`, `EntregaMemoryRepository` e `FakeRepository`).
- Atualizei as assinaturas das funções de caso de uso em `src/service_layer/services.py` para dependerem estritamente da interface mínima necessária (`consultar_cliente`, `consultar_pedido` e `consultar_status_entrega` dependem de `LeitorRepositorio`; `listar_restaurantes` depende de `ListadorRepositorio`; `listar_pedidos_do_cliente` e `criar_pedido` dependem dos papéis específicos de leitura e escrita).
- Adicionei 3 novos testes unitários em `tests/unit/test_services.py` comprovando que dublês parciais (que implementam somente `get` ou somente `list`) funcionam perfeitamente nos serviços, sem necessidade de implementar métodos não utilizados.
- Documentei detalhadamente a violação de ISP, a refatoração, a preservação de comportamento e os custos no arquivo `docs/solid.md`.

#### Arquivos alterados

- `src/service_layer/services.py`
- `tests/unit/test_services.py`
- `docs/solid.md`
- `DECISIONS.md`

#### Commits relevantes

- Código anterior: `46cdb65` e `5438f36`.
- Commit próprio com a refatoração ISP: a preencher após o commit das alterações.

#### Decisão de projeto

- Segregar a abstração de repositório na camada de serviços em protocolos de papéis específicos (`LeitorRepositorio`, `ListadorRepositorio`, `EscritorRepositorio`) e manter `Repositorio` como a composição desses protocolos, garantindo que consumidores de leitura não sejam forçados a depender de operações de escrita ou varredura de coleções (ISP) e permitindo dublês de teste mais leves e expressivos.

#### Uso de IA

- Utilizei assistente de IA para auxiliar na análise das interfaces da camada de serviços perante o Princípio da Segregação de Interfaces (ISP), na estruturação dos protocolos segregados e na elaboração da documentação em `docs/solid.md` e neste autorrelato.

## Parte 2 - checkpoint 3 (10/11/2026)

### Victor Antunes dos Santos (@VictorAntunesCastro)

#### O que implementei

- Implementei o padrão GoF comportamental **Observer** na camada de serviço (`src/service_layer/services.py`) com o protocolo `ObservadorEntrega`, o sujeito `NotificadorEntrega`, o evento imutável `EventoStatusEntrega` e dois observadores concretos (`HistoricoEntregaObservador` e `NotificacaoClienteObservador`), integrando a publicação de eventos aos casos de uso `criar_pedido` e `atualizar_status_entrega`.
- Conectei o `NotificadorEntrega` e o `HistoricoEntregaObservador` ao entrypoint Flask (`src/entrypoints/flask_app.py`), expondo a consulta da trilha de auditoria das transições no endpoint `GET /pedidos/<pedido_id>/entrega/historico` sem alterar o contrato das rotas existentes.
- Adicionei testes unitários e E2E (`tests/unit/test_services.py` e `tests/e2e/test_api.py`) cobrindo a notificação de múltiplos observadores, cancelamento de inscrição (`desinscrever`), não emissão em transições inválidas ou idempotentes e consulta HTTP do histórico.
- Documentei o padrão Observer, justificativa, alternativa considerada, participantes, diagrama de classes em Mermaid, testes e análise de custo em `docs/gof.md`.

#### Arquivos alterados

- `src/service_layer/services.py`
- `src/entrypoints/flask_app.py`
- `tests/unit/test_services.py`
- `tests/e2e/test_api.py`
- `docs/gof.md`
- `DECISIONS.md`

#### Commits relevantes

- Commits próprios deste Checkpoint 3 (Fase 2): implementação do padrão Observer na camada de serviço, endpoint e testes automatizados, além da documentação em `docs/gof.md` e atualização deste autorrelato em `DECISIONS.md`.

#### Decisão de projeto

- Utilizar o padrão **Observer** (`NotificadorEntrega` e `ObservadorEntrega`) injetado opcionalmente em `criar_pedido` e `atualizar_status_entrega` para desacoplar o registro de histórico de transições (`HistoricoEntregaObservador`) e as mensagens ao cliente (`NotificacaoClienteObservador`) da orquestração principal, garantindo que apenas mudanças efetivas e válidas de estado disparem eventos sem alterar a entidade `Entrega` nem quebrar chamadas existentes.

#### Uso de IA

- Utilizei o assistente de IA (Gemini) como apoio na análise dos padrões GoF, na organização da implementação do Observer, na elaboração dos testes e na criação do diagrama Mermaid para a documentação. O código e os testes foram revisados e validados localmente com `pytest`.

### Davi França Emmerick de Souza

#### O que implementei

- Apliquei o padrão GoF Strategy ao cálculo do agregado `Pedido`, com uma política de preço regular e uma estratégia de desconto percentual.
- Mantive `Pedido.total` e os chamadores existentes com cálculo regular; o método `Pedido.calcular_total()` permite solicitar outro cálculo sem alterar os itens nem o total padrão.
- Adicionei testes unitários para as estratégias, a validação do percentual e a preservação do total padrão; documentei participantes, diagrama, alternativa e custo em `docs/gof.md`.

#### Arquivos alterados

- `src/domain/entities/politica_preco_pedido.py`
- `src/domain/entities/pedido.py`
- `src/domain/entities/__init__.py`
- `src/domain/model.py`
- `tests/unit/test_pedido.py`
- `docs/gof.md`
- `DECISIONS.md`

#### Decisão de projeto

- Usar Strategy para encapsular variações de cálculo de preço, mantendo o cálculo regular como padrão para preservar compatibilidade e não guardar uma campanha promocional como estado do pedido.

#### Uso de IA

- Utilizei o assistente de IA para testar as estratégias e redigir a documentação e este autorrelato.