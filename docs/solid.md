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

**Princípio da Inversão de Dependência (DIP).** Nos commits `e4ecb22` (28/09/2026), `937bad5` (29/09/2026) e `1213e36` (29/09/2026), anteriores a 06/10/2026, a camada de serviço (`src/service_layer/services.py`) e o entrypoint Flask (`src/entrypoints/flask_app.py`) apresentavam duas violações diretas de DIP:

1. **Acoplamento direto a estrutura de dados concreta (`dict[str, Entrega]`) nos casos de uso de entrega:** Enquanto os casos de uso de `Cliente`, `Restaurante` e `Pedido` operavam sobre a interface abstrata de repositório (`add`, `get`, `list`), as funções `criar_pedido`, `consultar_status_entrega` e `atualizar_status_entrega` dependiam diretamente de um dicionário Python concreto (`entregas: dict[str, Entrega]`), realizando indexação manual (`entregas[pedido.id] = ...`) na camada de orquestração.
2. **Direção invertida do contrato de repositório:** O módulo `src/service_layer/services.py` importava `AbstractRepository` de `src.adapters.repository` (camada de infraestrutura/adapters), fazendo com que a camada de alto nível dependesse do módulo de adapters em vez de declarar seu próprio protocolo abstrato.

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

Qualquer mudança de requisito para persistir `Entrega` em um repositório real (como SQLAlchemy/SQLite, a exemplo de `ClienteRepository` e `PedidoRepository`) obrigava a modificar diretamente a implementação das três funções de caso de uso em `src/service_layer/services.py` (`criar_pedido`, `consultar_status_entrega` e `atualizar_status_entrega`), pois elas assumiam a sintaxe de indexação por chave de `dict` (`entregas[pedido.id] = ...`) em vez do contrato `add(entity)` / `get(id)` / `list()`. Além disso, a camada de serviço conhecia o pacote `src.adapters.repository`, contrariando a regra de que as abstrações devem pertencer à camada de alto nível.

### Refatoração

1. **Definição da abstração na camada de serviço (`Repositorio[T]`):** Foi declarado o protocolo genérico `@runtime_checkable class Repositorio(Protocol[T])` com os métodos `add(entity)`, `get(entity_id)` e `list()` diretamente em `src/service_layer/services.py`, eliminando a importação de `src.adapters.repository` pela camada de serviço.
2. **Unificação do acesso a `Entrega` via repositório (`EntregaMemoryRepository`):** Foi implementada a classe `EntregaMemoryRepository` cumprindo o protocolo `Repositorio[Entrega]`, e os casos de uso `criar_pedido`, `consultar_status_entrega` e `atualizar_status_entrega` passaram a operar exclusivamente pelos métodos `entrega_repo.add(...)` e `entrega_repo.get(...)` (com adaptação transparente em `_obter_entrega_repo` quando um `dict` legado é fornecido).
3. **Injeção na Application Factory do Flask:** Em `src/entrypoints/flask_app.py`, `create_app()` passou a instanciar `services.EntregaMemoryRepository()` por padrão e a permitir a injeção de qualquer implementação de `Repositorio[Entrega]`.

- **Código anterior:** `937bad5` (`Fix: Restaura API Flask funcional após corrupção em merge`, de 29/09/2026) e `1213e36` (29/09/2026).
- **Código após a refatoração:** `46cdb65` — `[Refactor] Aplica DIP na camada de servicos e repositorio de entregas` (03/11/2026).
- **Arquivos alterados:** `src/service_layer/services.py`, `src/entrypoints/flask_app.py`, `tests/unit/test_services.py` e `tests/e2e/test_api.py`.

### Preservação do comportamento

Todos os 33 cenários unitários existentes em `tests/unit/test_services.py` e os 34 cenários E2E em `tests/e2e/test_api.py` continuaram passando sem regressão de contrato HTTP nem de regras de negócio. Além disso, foram adicionados 3 novos testes automatizados para validar especificamente a refatoração:
- `test_entrega_memory_repository_cumpre_protocolo_repositorio` (`tests/unit/test_services.py`): verifica que `EntregaMemoryRepository` satisfaz `isinstance(..., services.Repositorio)` e executa o ciclo completo de criação e atualização de status via `add`, `get` e `list`;
- `test_servicos_entrega_mantem_compatibilidade_com_dicionario` (`tests/unit/test_services.py`): garante retrocompatibilidade com chamadas legadas que ainda passem `dict[str, Entrega]`;
- `test_create_app_aceita_repositorio_de_entrega_injetado` (`tests/e2e/test_api.py`): comprova ponta a ponta no Flask que `create_app(entregas=entrega_repo)` opera desacoplado de dicionários concretos.

### Custo

A refatoração acrescentou o protocolo `Repositorio[T]`, a classe `EntregaMemoryRepository` e a função auxiliar `_obter_entrega_repo` em `src/service_layer/services.py` (cerca de 35 linhas adicionais e um nível extra de indireção no acesso às entregas). Esse custo compensa amplamente porque elimina a dependência da camada de serviços em relação a `src.adapters.repository`, padroniza todos os agregados sob o mesmo contrato abstrato (`add`/`get`/`list`) e permite substituir o armazenamento de entregas em memória por uma implementação SQLAlchemy sem alterar uma única linha da lógica de orquestração dos casos de uso.
