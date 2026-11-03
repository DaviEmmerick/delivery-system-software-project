# Refatorações SOLID

## Davi França Emmerick de Souza — agregado Pedido

### Princípio e situação anterior

**Princípio da Responsabilidade Única (SRP).** No commit `d058f44`, anterior a 06/10/2026, `Pedido.__init__` acumulava duas responsabilidades: validar invariantes do agregado e interpretar/converter as diferentes representações aceitas para os itens (`Produto` e `ItemPedido`).

Trecho de `src/domain/entities/pedido.py` em `d058f44` (linhas 20–27):

```python
itens_normalizados = []
for item in itens:
    if isinstance(item, Produto):
        itens_normalizados.append(ItemPedido(item))
    elif isinstance(item, ItemPedido):
        itens_normalizados.append(item)
    else:
        raise ValueError("itens do pedido devem ser Produtos ou ItemPedido")
```

Uma mudança na forma de receber produtos podia obrigar a alterar a própria entidade, mesmo sem mudar as regras que definem um pedido válido.

### Refatoração

A entidade `Pedido` agora recebe somente `ItemPedido` já normalizados e valida as invariantes do agregado. A nova `PedidoFactory` converte entradas `Produto`, `ItemPedido` ou uma mistura dos dois para a representação que a entidade aceita. O serviço de aplicação e o repositório já forneciam `ItemPedido`, portanto não precisaram de alterações.

- **Código anterior:** `d058f44` — `[Feat] Entidades`, de 28/09/2026.
- **Código após a refatoração:** hash do commit deste checkpoint a preencher após o commit das alterações.
- **Arquivos:** `src/domain/entities/pedido.py`, `src/domain/entities/pedido_factory.py`, `tests/unit/test_pedido.py` e `tests/integration/test_repositories.py`.

### Preservação do comportamento

Não foram adicionados novos testes. As chamadas existentes nos testes unitários e de integração que fornecem `Produto` foram direcionadas para a factory; os cenários existentes continuam cobrindo criação simples, itens mistos, validações e cálculo do total. A assinatura de `Pedido` agora aceita apenas itens normalizados.

### Custo

A mudança adiciona uma classe e um módulo e exige que chamadas que fornecem `Produto` usem explicitamente a factory. Isso torna visível a conversão para a representação do domínio e deixa `Pedido` focado nas próprias invariantes; o custo adicional é pequeno e concentrado na criação do agregado. A interface de construção direta de `Pedido` agora exige `ItemPedido`; os caminhos que aceitam `Produto` continuam disponíveis pela factory.

---

## Victor Antunes dos Santos (@VictorAntunesCastro) — Camada de Serviço, Entrypoints e Testes E2E

### Princípio e situação anterior

**Princípio da Inversão de Dependência (DIP).** Nos commits `e4ecb22` (28/09/2026), `937bad5` (29/09/2026) e `1213e36` (29/09/2026), anteriores a 06/10/2026, a camada de serviço (`src/service_layer/services.py`) e o entrypoint Flask (`src/entrypoints/flask_app.py`) apresentavam violação de DIP:

1. **Violação principal (em tempo de execução) — acoplamento direto a estrutura de dados concreta (`dict[str, Entrega]`) nos casos de uso de entrega:** Enquanto os casos de uso de `Cliente`, `Restaurante` e `Pedido` operavam sobre a interface abstrata de repositório (`add`, `get`, `list`), as funções `criar_pedido`, `consultar_status_entrega` e `atualizar_status_entrega` dependiam diretamente de um dicionário Python concreto (`entregas: dict[str, Entrega]`), realizando indexação manual (`entregas[pedido.id] = ...`) dentro da camada de orquestração.
2. **Violação complementar (dependência estática entre camadas):** O módulo `src/service_layer/services.py` importava `AbstractRepository` de `src.adapters.repository` sob `TYPE_CHECKING`, mantendo uma dependência estática de tipagem da camada de serviço para o módulo de adapters em vez de declarar seu próprio protocolo abstrato na camada de serviço.

Trecho de `src/service_layer/services.py` no commit `1213e36` (linhas 6–7 e 70–117) e `937bad5`:

```python
if TYPE_CHECKING: 
    from src.adapters.repository import AbstractRepository
...
def criar_pedido(
    cliente_id: str,
    produtos: list[dict],
    cliente_repo: AbstractRepository,
    pedido_repo: AbstractRepository,
    entregas: dict[str, Entrega],
) -> str:
    consultar_cliente(cliente_id, cliente_repo)  
    if not isinstance(produtos, list) or not produtos:
        raise ValueError("pedido deve conter ao menos um item")
    itens = [_montar_item(produto) for produto in produtos]
    pedido = Pedido(cliente=cliente_id, itens=itens)  
    pedido_repo.add(pedido)
    entregas[pedido.id] = Entrega(pedido_id=pedido.id)
    return pedido.id
...
def consultar_status_entrega(pedido_id: str, entregas: dict[str, Entrega]) -> str:
    entrega = entregas.get(pedido_id)
    if entrega is None:
        raise NaoEncontrado("entrega não encontrada")
    return entrega.status

def atualizar_status_entrega(pedido_id: str, novo_status: str, entregas: dict[str, Entrega]) -> str:
    entrega = entregas.get(pedido_id)
    if entrega is None:
        raise NaoEncontrado("entrega não encontrada")
    ...
    entrega_atualizada = Entrega(pedido_id=pedido_id, status=status_normalizado)
    entregas[pedido_id] = entrega_atualizada
    return entrega_atualizada.status
```

E em `src/entrypoints/flask_app.py` (`937bad5` / `1213e36`, linhas 31–32):

```python
    if entregas is None:
        entregas = {}
```

### Problema concreto

Qualquer mudança de requisito para persistir `Entrega` em um repositório de banco de dados (como SQLAlchemy/SQLite, a exemplo de `ClienteRepository` e `PedidoRepository`) obrigava a modificar diretamente a implementação das três funções de caso de uso em `src/service_layer/services.py` (`criar_pedido`, `consultar_status_entrega` e `atualizar_status_entrega`), pois elas exigiam a sintaxe de indexação por chave de `dict` (`entregas[pedido.id] = ...`) em vez do contrato `add(entity)` / `get(id)` / `list()`. Além disso, a tipagem da camada de serviço apontava para `src.adapters.repository`, contrariando o princípio de que a abstração deve pertencer à camada de alto nível.

### Refatoração

1. **Definição da abstração na camada de serviço (`Repositorio[T]`):** Foi declarado o protocolo genérico `@runtime_checkable class Repositorio(Protocol[T])` com os métodos `add(entity)`, `get(entity_id)` e `list()` diretamente em `src/service_layer/services.py`, eliminando a dependência estática de `src.adapters.repository`.
2. **Unificação do acesso a `Entrega` exclusivamente via `Repositorio[Entrega]`:** Os casos de uso `criar_pedido`, `consultar_status_entrega` e `atualizar_status_entrega` passaram a receber `entregas: Repositorio[Entrega]` e a operar exclusivamente pelos métodos `entregas.add(...)` e `entregas.get(...)`, removendo qualquer acoplamento a `dict[str, Entrega]`.
3. **Implementação de `EntregaMemoryRepository` e injeção no Flask:** Foi criada a classe `EntregaMemoryRepository` cumprindo `Repositorio[Entrega]`, e `create_app()` em `src/entrypoints/flask_app.py` passou a injetá-la por padrão. *Nota sobre localização:* embora repositórios com dependências de infraestrutura (como SQLAlchemy) fiquem em `src/adapters/`, `EntregaMemoryRepository` não depende de banco de dados nem de ORM externo — é um colaborador padrão puramente em memória para os casos de uso de entrega e foi mantido ao lado do protocolo `Repositorio[T]` em `src/service_layer/services.py` para respeitar a divisão de módulos por integrante definida no projeto sem tocar em arquivos de outros membros.

- **Código anterior:** `937bad5` (`Fix: Restaura API Flask funcional após corrupção em merge`, de 29/09/2026) e `1213e36` (29/09/2026).
- **Código após a refatoração:** `46cdb65` — `[Refactor] Aplica DIP na camada de servicos e repositorio de entregas` (03/11/2026) e commit subsequente de remoção do fallback de `dict`.
- **Arquivos alterados:** `src/service_layer/services.py`, `src/entrypoints/flask_app.py`, `tests/unit/test_services.py` e `tests/e2e/test_api.py`.

### Preservação do comportamento

Todos os 33 cenários unitários existentes em `tests/unit/test_services.py` e os 34 cenários E2E em `tests/e2e/test_api.py` continuaram passando sem regressão de contrato HTTP nem de regras de negócio. Além disso, foram adicionados 2 novos testes automatizados para validar especificamente a refatoração:
- `test_entrega_memory_repository_cumpre_protocolo_repositorio` (`tests/unit/test_services.py`): verifica que `EntregaMemoryRepository` satisfaz `isinstance(..., services.Repositorio)` e executa o ciclo completo de criação e atualização de status via `add`, `get` e `list`;
- `test_create_app_aceita_repositorio_de_entrega_injetado` (`tests/e2e/test_api.py`): comprova ponta a ponta no Flask que `create_app(entregas=entrega_repo)` opera desacoplado de dicionários concretos.

### Custo

A refatoração acrescentou o protocolo `Repositorio[T]` e a classe `EntregaMemoryRepository` em `src/service_layer/services.py` (cerca de 28 linhas adicionais e um nível extra de indireção no acesso às entregas). Esse custo compensa porque elimina a dependência da camada de serviços em relação a `src.adapters.repository`, padroniza todos os agregados sob o mesmo contrato abstrato (`add`/`get`/`list`) e permite injetar uma futura implementação persistente de `Repositorio[Entrega]` sem alterar a lógica de orquestração dos casos de uso.
