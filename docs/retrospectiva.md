# Retrospectiva da arquitetura

**Pergunta:** depois de conviver com a arquitetura em camadas (domínio, Service Layer, Repository e entrypoint Flask), refatorar princípios SOLID e aplicar padrões GoF, nós a escolheríamos de novo?

**Resposta curta:** sim, mas com ajustes. Manteríamos as camadas e os repositórios e adotaríamos uma solução híbrida nos pontos em que a Fase 2 mostrou que a separação ficou incompleta: o estado das entregas e o histórico de eventos ainda ficam em memória, e alguns padrões continuam isolados no domínio, sem caminho até a API ou o banco.

## 1. As previsões do Checkpoint 1 se confirmaram?

Em `docs/arquitetura.md`, priorizamos **integridade dos dados**, **testabilidade** e **modificabilidade** e registramos dois riscos: a perda dos produtos do restaurante no `RestauranteRepository` e o status de entrega mantido em um dicionário fora do banco.

| Previsão do Checkpoint 1 | O que aconteceu na Fase 2 | Confirmou? |
| --- | --- | --- |
| **Testabilidade:** regras e serviços testáveis sem Flask nem banco. | A suíte foi de 148 testes (Checkpoint 1) para **201**. Os 161 testes de `tests/unit/` rodam em **~0,18 s**, enquanto os 36 testes E2E levam **~0,33 s**, ou seja, cerca de 8 vezes mais tempo por teste. Toda a camada de serviço continua sendo testada com `FakeRepository` e dublês parciais. | Sim, foi o benefício mais concreto. |
| **Modificabilidade:** mudanças de persistência ficariam em `src/adapters/`, sem alterar o domínio. | A refatoração LSP de `RestauranteRepository` (`90bfefc`) corrigiu a perda dos produtos mexendo apenas em `src/adapters/orm.py`, `src/adapters/repository.py` e em um teste de integração. Nenhuma entidade foi alterada. | Sim. |
| **Inversão de dependência parcial:** `AbstractRepository` estava declarado em `adapters/`. | A refatoração DIP (`46cdb65`) moveu o contrato `Repositorio[T]` para a camada de serviço, e a ISP (`8eee1ad`) o dividiu em `LeitorRepositorio`, `ListadorRepositorio` e `EscritorRepositorio`. A direção das dependências passou a ser a pretendida. | Sim. A lacuna foi corrigida. |
| **Risco:** status de entrega em memória, fora de uma transação com o pedido. | Continua aberto. `Entrega` ganhou o padrão State (`9598c9c`) e o histórico ganhou o Observer (`3866298`), mas os dois ainda vivem em memória (`EntregaMemoryRepository` e `HistoricoEntregaObservador`). Se o processo reiniciar, os dados se perdem. | Sim, e o risco ficou maior, porque agora há mais estado em memória. |

**Trade-off que mais pesou na prática:** *testabilidade versus simplicidade*. A testabilidade pagou o custo: todas as refatorações foram validadas pela suíte existente. Mas a indireção cresceu bastante: `services.py` passou de 117 para **272 linhas**, com quatro protocolos de repositório, um repositório em memória e as classes do Observer. Entre o Checkpoint 1 e hoje, `src/` e `tests/` somaram **1.023 inserções em 21 arquivos**.

## 2. As camadas facilitaram ou atrapalharam a Fase 2?

**Facilitaram** quando a mudança respeitava a fronteira de uma camada:

- **State** (`9598c9c`) alterou apenas `src/domain/entities/entrega.py`. O ajuste no serviço (`d615d4b`) mudou somente 6 linhas de `services.py`.
- **Observer** (`3866298`) mexeu apenas em `service_layer/`, `entrypoints/` e testes, **sem tocar em nenhum arquivo de `src/domain/`**. Isso só funcionou porque os serviços já recebiam suas dependências por parâmetro.
- **ISP** (`8eee1ad`) alterou apenas `services.py` e `test_services.py`. Os repositórios SQLAlchemy continuaram compatíveis porque os protocolos são estruturais.
- **Strategy** (`607d0af`) e **Composite** (`0650ba3`) ficaram inteiramente em `src/domain/` e nos testes unitários.

**Atrapalharam** ou cobraram um custo em três situações:

1. **Mudanças no construtor de entidades se propagaram para os testes.** A refatoração SRP de `Pedido` com `PedidoFactory` (`46bed0d`) deixou testes antigos de `Pedido` falhando, como `docs/solid.md` registra na seção do LSP, e exigiu um commit de correção (`f475260`, 94 inserções em três arquivos de teste). O isolamento do domínio não protege contra acoplamento dos testes à forma de construir as entidades.
2. **Padrões do domínio sem caminho até a borda.** Uma busca por `Combo` e `PoliticaPreco` em `src/adapters/`, `src/service_layer/` e `src/entrypoints/` não encontra nenhuma referência. Para expor combos ou políticas de preço na API, seria preciso criar mapeamentos ORM novos, como aconteceu com os produtos do restaurante. A separação permitiu adicionar os padrões sem risco, mas também facilitou deixá-los "pela metade".
3. **Assinaturas longas.** `criar_pedido` recebe hoje seis parâmetros (três repositórios, os produtos, o cliente e o notificador). Sem Unit of Work nem um ponto único de composição, quem chama precisa montar tudo, e isso se concentra em `create_app()`.

## 3. Comparação com a alternativa do Checkpoint 1

No Checkpoint 1, a alternativa comparada foi **Transaction Script com acesso direto ao SQLAlchemy**. Com o que vivemos na Fase 2:

- Com a alternativa, o **State** e o **Observer** teriam de ser aplicados dentro das rotas ou sobre modelos ORM. As transições de `Entrega` seriam testáveis apenas com banco e contexto HTTP, perdendo a diferença de velocidade medida acima.
- As refatorações **DIP** e **ISP** não fariam sentido, porque não haveria contrato de repositório para inverter ou segregar.
- Por outro lado, o risco de integridade das entregas **não existiria** na alternativa: tudo estaria em tabelas desde o início, e a criação do pedido e da entrega caberia numa única transação. Esse é o ponto em que a alternativa é objetivamente melhor que a nossa implementação atual.

Não implementamos o experimento opcional em `experimentos/`, então essa comparação é argumentativa e se apoia nos commits citados, não em uma medição lado a lado.

## 4. Decisão final

**Manteríamos a arquitetura em camadas com repositórios, adotando ajustes híbridos.** Para este domínio de delivery, que tem regras com estado (ciclo de vida da entrega), cálculo de preço variável (Strategy e Composite) e efeitos colaterais (Observer), a separação entre domínio, serviços e adapters se pagou: todas as refatorações e os quatro padrões GoF da Fase 2 foram introduzidos sem quebrar o contrato HTTP, e a suíte cresceu de 148 para 201 testes, permanecendo verde.

Os ajustes que faríamos, se começássemos de novo:

1. **Persistir `Entrega` e o histórico desde o início** com um `EntregaRepository` SQLAlchemy, eliminando o risco que ficou aberto desde o Checkpoint 1.
2. **Aceitar Transaction Script nos casos puramente CRUD** (como `listar_restaurantes`), reservando serviço e entidades ricas para fluxos com regra de negócio. Isso reduziria a indireção onde ela não traz benefício.
3. **Ligar cada padrão do domínio a um caso de uso** (serviço, mapeamento e rota) no mesmo checkpoint em que ele for criado, para que nenhum padrão fique sem uso no sistema em execução.
4. **Criar entidades nos testes por meio de fixtures ou factories**, para que mudanças de construtor como a do `46bed0d` não se espalhem pela suíte.
