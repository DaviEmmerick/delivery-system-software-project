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