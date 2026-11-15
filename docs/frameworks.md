# Análise de Frameworks

## 1. Papel dos frameworks na solução e isolamento do domínio

O sistema utiliza três frameworks principais — **Flask**, **SQLAlchemy** e **pytest** — posicionados exclusivamente nas camadas externas e na infraestrutura de verificação, mantendo o núcleo do negócio (`src/domain/`) como código Python puro (POPOs — *Plain Old Python Objects*).

| Framework | Papel na solução | Camada / Localização | Por que o domínio (`src/domain/`) não depende dele |
| --- | --- | --- | --- |
| **Flask** | Expõe a API REST HTTP, realiza o roteamento de URLs (`@app.route`), faz o parsing de requisições JSON, compõe os colaboradores (`create_app`) e traduz exceções de aplicação em códigos HTTP (`@app.errorhandler`). | Entrypoints (`src/entrypoints/flask_app.py`) | Regras de negócio (cálculo de subtotais, descontos, validações de identidade e máquina de estados da entrega) são agnósticas ao protocolo HTTP. Se o domínio importasse `flask.request` ou `abort`, não seria possível reutilizar as entidades em filas, CLIs ou testes sem contexto web. |
| **SQLAlchemy** | Realiza o mapeamento objeto-relacional declarativo (`DeclarativeBase`), gerencia conexões e transações (`create_engine`, `sessionmaker`) e traduz entidades para tabelas relacionais no SQLite. | Adapters (`src/adapters/orm.py` e `src/adapters/repository.py`) | As entidades (`Cliente`, `Restaurante`, `Pedido`, `Produto`, `Entrega`) e objetos de valor (`Endereco`, `ItemPedido`) não herdam de `DeclarativeBase` nem carregam colunas `Mapped[...]`. Isso impede que restrições de banco (chaves estrangeiras, auto-incremento ou lazy loading) contaminem as invariantes e a imutabilidade (`@dataclass(frozen=True)`) do domínio. |
| **pytest** | Descobre e executa a suíte automatizada (unitária, integração e E2E), injeta dependências de teste via fixtures (`conftest.py`), parametriza cenários de borda e captura exceções esperadas (`pytest.raises`). | Infraestrutura de testes (`tests/` e `pytest.ini`) | O código de produção não deve depender de ferramentas de verificação. O domínio apenas expõe interfaces limpas e lança exceções padrão (`ValueError`), permitindo que o `pytest` o exercite externamente sem acoplamento. |

---

## 2. Biblioteca vs. Framework e Inversão de Controle (IoC)

A diferença fundamental entre usar uma **biblioteca** e usar um **framework** está em **quem detém o fluxo de controle da execução**:

- **Biblioteca (ex.: `uuid`, `math`, `dataclasses`):** o código do grupo está no comando. As entidades em `src/domain/` importam `uuid.uuid4().hex` ou `math.isfinite()` e as invocam explicitamente quando precisam gerar um ID ou validar um preço.
- **Framework (Flask, SQLAlchemy, pytest):** aplica o **Princípio de Hollywood (*"Não nos ligue, nós ligamos para você"*)**. O framework detém o ciclo de vida principal (loop de servidor WSGI, gerenciamento de sessão/unidade de trabalho ou runner de testes) e invoca funções ou classes registradas pelo grupo nos momentos apropriados.

### Pontos de Inversão de Controle no repositório

1. **Registro de rotas e tratamento global de exceções no Flask (`src/entrypoints/flask_app.py`):**
   O grupo não escreve um loop de leitura de sockets HTTP nem um `try/except` manual em cada função. Em vez disso, funções como `criar_cliente()`, `criar_pedido()` e `atualizar_status_entrega()` são registradas via decoradores (`@app.post(...)`, `@app.patch(...)`, `@app.errorhandler(NaoEncontrado)`). Quando uma requisição chega, o servidor WSGI do Flask inspeciona o método/caminho, invoca a função correspondente do grupo e, caso uma exceção seja levantada na `service_layer`, intercepta o fluxo e aciona o handler registrado para devolver HTTP `400`, `404` ou `409`.
2. **Descoberta de testes e injeção de fixtures no pytest (`tests/conftest.py`, `tests/unit/`, `tests/e2e/`):**
   O grupo não escreve um script `main()` chamando manualmente cada função `test_*`. Ao executar `pytest`, o framework varre os diretórios configurados em `pytest.ini`, lê os parâmetros declarados nas assinaturas das funções de teste (como `client`, `engine` ou valores de `@pytest.mark.parametrize`), instancia e injeta automaticamente as *fixtures* correspondentes antes de chamar a função de teste do grupo.
3. **Ciclo de persistência e cascata no SQLAlchemy (`src/adapters/orm.py` e `src/adapters/repository.py`):**
   Em `SQLAlchemyRepository.add()`, o código apenas entrega um objeto mapeado a `session.merge(self._to_model(entity))` dentro do gerenciador de contexto `with self._session_factory.begin() as session:`. O SQLAlchemy assume o controle do ciclo de vida da transação (*Unit of Work*), inspeciona os metadados declarados em `ClienteModel`, `RestauranteModel` e `PedidoModel` (incluindo `cascade="all, delete-orphan"` e `order_by`), gera as instruções SQL `INSERT`/`UPDATE`/`DELETE` na ordem referencial correta e executa o `commit` automático ao sair do bloco.

---

## 3. Padrões de projeto internos dos frameworks usados no código

Os frameworks utilizados empregam padrões GoF clássicos em sua arquitetura interna, os quais se manifestam diretamente nos pontos de extensão usados pelo grupo:

1. **Factory Method / Abstract Factory — `create_sqlite_engine()` (`src/adapters/orm.py`) e `sessionmaker` (`src/adapters/repository.py`):**
   - **Como aparece no código:** `create_engine(database_url, ...)` encapsula a criação de `Engine` e dialetos específicos (configurando `StaticPool` quando a URL termina em `:memory:` e `check_same_thread=False` para SQLite), enquanto `sessionmaker(bind=engine)` atua como uma fábrica configurada que produz novas instâncias de `Session` a cada chamada `self._session_factory()`.
2. **Data Mapper & Identity Map / Unit of Work — `DeclarativeBase` e `Session` (`src/adapters/orm.py` e `src/adapters/repository.py`):**
   - **Como aparece no código:** O mapeamento declarativo (`ClienteModel`, `RestauranteModel`, `PedidoModel`) implementa o padrão *Data Mapper* (isolando o esquema relacional das entidades de domínio), enquanto o objeto `Session` gerenciado por `self._session_factory.begin()` implementa *Unit of Work* e *Identity Map*, rastreando modificações nos objetos mapeados e sincronizando-as atomicamente com o SQLite.
3. **Decorator (estrutural) e Chain of Responsibility — Rotas e Error Handlers do Flask (`src/entrypoints/flask_app.py`):**
   - **Como aparece no código:** Os decoradores `@app.get(...)`, `@app.post(...)` e `@app.errorhandler(...)` envolvem as funções de view do grupo e as registram nas estruturas internas de despacho do Flask/Werkzeug. Durante o processamento de uma requisição, o pipeline WSGI e o despacho de exceções percorrem uma cadeia de middlewares e handlers registrados até encontrar o tratador compatível com a rota ou com a classe da exceção (`NaoEncontrado`, `Conflito`, `ValueError`).
4. **Template Method — Ciclo de execução de testes do `pytest` (`tests/unit/`, `tests/integration/`, `tests/e2e/`):**
   - **Como aparece no código:** O `pytest` define o esqueleto fixo do algoritmo de execução de cada item de teste (*setup* de fixtures -> chamada da função `test_*` -> captura de asserções/exceções -> *teardown* das fixtures), permitindo que o grupo personalize apenas os passos variáveis (dados de entrada e asserções de domínio/HTTP) sem reescrever a infraestrutura de execução e relatório.

---

## 4. O que mudaria se o grupo tivesse usado um framework full-stack (Django)

Se o grupo tivesse optado por **Django** (com Django ORM e Django REST Framework) em vez da combinação **Flask + SQLAlchemy**, a estrutura do sistema sofreria impactos arquiteturais significativos:

1. **Acoplamento estrutural no modelo de domínio (Active Record vs. Data Mapper):**
   O Django utiliza o padrão *Active Record* (`models.Model`), no qual os atributos da tabela, validações de banco, gerenciadores de consulta (`Model.objects`) e persistência (`obj.save()`) residem na própria classe de modelo. Manter `src/domain/entities/` como POPOs puros exigiria duplicar praticamente toda a hierarquia de classes (um conjunto de entidades puras e outro conjunto de `django.db.models.Model` com conversores manuais), o que vai contra o fluxo idiomático do Django.
2. **Direção de dependências e organização de pastas:**
   Em vez de uma arquitetura centrada no domínio (`src/domain/`, `src/service_layer/`, `src/adapters/`, `src/entrypoints/`), o Django impõe sua própria convenção orientada a *apps* (`models.py`, `views.py`, `serializers.py`, `urls.py`, `admin.py`), além de exigir configuração global centralizada (`settings.py`, `DJANGO_SETTINGS_MODULE`) antes mesmo de importar modelos.
3. **Impacto nos testes unitários e na velocidade de feedback:**
   Atualmente, os testes unitários em `tests/unit/` executam em milissegundos sem carregar ORM ou banco de dados. No Django, testar regras acopladas a `models.Model` normalmente exige herdar de `django.test.TestCase`, inicializar o registro de aplicações (*app registry*) e criar bancos de teste com migrações, aumentando o tempo de execução e acoplando a suíte ao ciclo de vida do framework.
4. **Trade-off de produtividade vs. controle arquitetural:**
   O Django entregaria recursos prontos fora da caixa — como painel administrativo, sistema de migrações (`makemigrations`), autenticação/permissões e serialização declarativa — reduzindo o código de infraestrutura inicial. Em contrapartida, tornaria mais difícil e custoso exercitar explicitamente a inversão de dependências, o isolamento do domínio e a substituição limpa de adaptadores propostas como objetivos desta disciplina.