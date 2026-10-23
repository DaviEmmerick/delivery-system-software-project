# ADR 0001: Modelar os agregados e regras no domínio

- **Responsável:** Davi França Emmerick de Souza
- **Status:** decisão implementada na Fase 1
- **Data:** 25/09/2026

## Contexto

O sistema precisa representar clientes, endereços e pedidos com regras de negócio próprias. Um pedido pode conter produtos em quantidades diferentes, e seu total precisa refletir esses itens sem transferir essa regra para a API ou para a infraestrutura. O cliente também pode ter um endereço associado, cujos dados devem permanecer válidos.

## Decisão

Manter essas regras nas entidades e objetos de valor do domínio:

- `Cliente` pode ser associado a um `Endereco`;
- `Endereco` é imutável;
- `ItemPedido` é um objeto de valor imutável que contém um produto e uma quantidade e calcula o subtotal;
- `Pedido` normaliza produtos para itens, preserva os itens e calcula o total a partir dos subtotais.

Assim, o modelo de domínio permanece independente de entrypoints, serviços e infraestrutura.

## Alternativas consideradas

- Calcular quantidades e totais na camada de serviço ou nas rotas da API.
- Guardar produtos e quantidades em estruturas genéricas, sem um objeto de domínio `ItemPedido`.
- Permitir alterações em endereço ou itens após sua criação, validando-os a cada atualização.

## Consequências

- O cálculo do pedido e as validações ficam próximos dos dados e podem ser exercitados sem iniciar Flask ou acessar infraestrutura.
- `ItemPedido` e `Endereco` expressam regras de imutabilidade; para alterar seus valores, é necessário criar novos objetos.
- A composição explícita aumenta a quantidade de objetos e exige que a camada consumidora converta os dados de entrada para as entidades do domínio.
- As novas regras precisaram de testes específicos para cobrir quantidades, subtotais, imutabilidade e associação entre entidades.

## Evidências

- `5efa26f` e `a063097` registram a estrutura inicial do domínio e suas entidades.
- `6b53d71` registra a mudança nos agregados: associação de endereço ao cliente, introdução de `ItemPedido` e cálculo do total de `Pedido` pelos subtotais.
- Os arquivos correspondentes são `src/domain/entities/cliente.py`, `src/domain/entities/endereco.py`, `src/domain/entities/item_pedido.py` e `src/domain/entities/pedido.py`.
