# Proposta do projeto

## Objetivo

Construir um sistema de delivery eficiente para facilitar pedidos, entregas e o acompanhamento do atendimento, reduzindo o uso de processos manuais e melhorando o fluxo entre cliente, restaurante e entregador.

## Público-alvo
- Clientes que desejam realizar pedidos de forma rápida e prática
- Restaurantes e estabelecimentos que precisam organizar o atendimento
- Entregadores que acompanham pedidos e rotas
- Administradores que controlam o fluxo do sistema

## Entidades iniciais do domínio
- Cliente
- Pedido
- Produto
- Entrega
- Endereço
- Restaurante

## Agregados previstos

### 1. Agregado Cliente
- Raiz: Cliente
- Entidades/objetos de valor: Cliente, Endereço
- Regras: cliente deve ter nome e telefone válidos; endereço deve ter rua e número

### 2. Agregado Pedido
- Raiz: Pedido
- Entidades/objetos de valor: Pedido, Produto, Entrega
- Regras: pedido deve conter ao menos um item; o total deve ser calculado a partir dos itens; entrega deve refletir o status do pedido

### 3. Agregado Restaurante
- Raiz: Restaurante
- Entidades/objetos de valor: Restaurante
- Regras: restaurante deve possuir nome válido e atuar como ponto de origem do pedido

## Funcionalidades previstas
- Cadastro de clientes
- Gestão de produtos e categorias
- Criação e acompanhamento de pedidos
- Atualização de status do pedido
- Controle de entrega
- Histórico de pedidos
- Dashboard administrativo

## Integrantes
- Leandro Machado — GitHub: @LeandroMachadoCC
- Davi França Emmerick de Souza — GitHub: @DaviEmmerick
- Joao Gabriel Azevedo — GitHub: @JoaoGAzevedo

## Divisão inicial de responsabilidades
- Leandro Machado: infraestrutura, ambiente e backend
- Davi França Emmerick de Souza: arquitetura, entidades e regras de negócio
- JoaoGAzevedo: modelagem de dados, validações e apoio na integração do backend
- Todos: testes, revisão final e ajustes de integração