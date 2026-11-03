# ADR 0004: Estratégia de Testabilidade com Testes Unitários Isolados para o Domínio Puro

- **Responsável:** João Gabriel de Azevedo (`@JoaoGAzevedo`)
- **Status:** decisão implementada na Fase 1 e refinada nas Fases subsequentes
- **Data:** 22/10/2026

## Contexto

O núcleo do sistema de delivery é composto por entidades e objetos de valor de domínio puro (`Cliente`, `Endereco`, `ItemPedido`, `Pedido`, `Produto`, `Restaurante` e `Entrega`). Essas classes concentram as invariantes essenciais de negócio da aplicação, incluindo sanitização de entradas (`strip()`), validação estrita de tipos e limites (como preço não negativo, quantidade inteira positiva e formato/comprimento de telefone), cálculos dinâmicos de agregação (`subtotal` e `total`) e garantias de imutabilidade estrutural em Value Objects (`Endereco` e `ItemPedido`).

Se a verificação dessas regras fosse realizada exclusivamente por meio de testes de ponta a ponta (E2E) através de requisições HTTP na API Flask ou dependesse da persistência real em tabelas do SQLite via SQLAlchemy, o ciclo de desenvolvimento enfrentaria problemas graves:
1. **Feedback lento:** testes que sobem transporte HTTP e banco de dados são cerca de 8 a 10 vezes mais lentos por teste do que testes unitários em memória (~9,4 ms contra ~1,2 ms por caso de teste, conforme documentado em `docs/arquitetura.md`).
2. **Dificuldade na cobertura combinatória de casos de borda:** exercitar dezenas de variações de entradas inválidas (`None`, strings vazias, espaços em branco, tipos numéricos incompatíveis, listas vazias) via payloads JSON em rotas HTTP introduz overhead desnecessário de parsing e serialização.
3. **Mapeamento impreciso de falhas:** um erro HTTP 400 retornado pela API dificulta identificar imediatamente se a rejeição decorreu de validação sintática do JSON no entrypoint ou de violação de regra de negócio no domínio.
4. **Risco de acoplamento da suíte:** a ausência de testes focados nas entidades poderia permitir que detalhes de infraestrutura ou de frameworks vazassem silenciosamente para o pacote `src/domain/`.

## Decisão

Adotar uma estratégia de **Testes Unitários Isolados para o Domínio Puro** (`tests/unit/`), garantindo testabilidade imediata, determinística e livre de dependências externas:

1. **Isolamento completo de frameworks e banco de dados:**
   - As entidades e value objects são instanciados e exercitados diretamente como objetos Python puros (POPO - *Plain Old Python Objects*), sem importar `Flask`, `SQLAlchemy` ou inicializar engines de SQLite.
2. **Cobertura exaustiva de invariantes com parametrização (`@pytest.mark.parametrize`):**
   - Utilizar testes parametrizados do `pytest` para cobrir sistematicamente classes de equivalência de dados inválidos (como `[None, "", "   "]` para nomes e ruas, e `[None, "", "   ", "123456789"]` para telefones).
   - Validar que cada violação de regra resulte na exceção semântica esperada (`ValueError`) com mensagens assertivas através de `pytest.raises(ValueError, match=...)`.
3. **Validação de Value Objects e Imutabilidade:**
   - Testar expressamente que classes congeladas (`@dataclass(frozen=True)` em `Endereco` e `ItemPedido`) rejeitam mutação em tempo de execução disparando `dataclasses.FrozenInstanceError`.
   - Validar a semântica de igualdade estrutural por valor (`assert obj1 == obj2`) para garantir que dois objetos com o mesmo estado sejam indistinguíveis.
4. **Verificação de sanitização e precisão aritmética:**
   - Testar a remoção sistemática de espaços periféricos (`strip()`) em campos textuais.
   - Utilizar `pytest.approx()` nas asserções de propriedades calculadas (`ItemPedido.subtotal` e `Pedido.total`) para prevenir falhas espúrias decorrentes de imprecisão de ponto flutuante em operações financeiras com `float`.
5. **Padronização do ambiente de execução e fixtures compartilhadas:**
   - Configurar o `pytest.ini` na raiz do projeto e em `tests/` com `pythonpath = . ..` e `testpaths = tests`, assegurando execução uniforme e sem erros de importação (`ModuleNotFoundError`) tanto na raiz quanto em subdiretórios e na Integração Contínua (CI).
   - Disponibilizar fixtures utilitárias compartilhadas em `tests/conftest.py` (`produto_exemplo`, `endereco_exemplo`, `cliente_exemplo`) para simplificar a criação de instâncias válidas e evitar duplicação de setup nos testes.

## Alternativas consideradas

- **Validar as regras de domínio apenas por testes E2E (`tests/e2e/test_api.py`):**
  - *Descartada:* Embora os testes E2E sejam essenciais para validar a integração entre HTTP, serviços e ORM, usá-los como única linha de defesa tornaria a suíte pesada, lenta e menos resiliente, contrariando a boa prática da Pirâmide de Testes.
- **Utilizar mocks e dublês pesados (`unittest.mock.patch` / `MagicMock`):**
  - *Descartada:* Como as entidades de domínio são puras e não realizam chamadas de rede ou I/O em disco, o uso de mocks traria complexidade acidental, fragilidade e testes difíceis de ler. A instanciação direta é mais clara, segura e executa na ordem de microssegundos.
- **Testes manuais ou asserts agrupados sem parametrização:**
  - *Descartada:* Testes com múltiplos asserts consecutivos interrompem a execução no primeiro erro, ocultando se os demais casos de borda passariam ou falhariam. A parametrização trata cada combinação como um caso de teste individualizado.

## Consequências

- **Positivas:**
  - **Execução em alta velocidade:** a suíte unitária de domínio executa dezenas de cenários em cerca de **~0,10 s**, garantindo feedback quase instantâneo durante o desenvolvimento local e na esteira de CI.
  - **Blindagem contra regressão:** qualquer alteração inadvertida nas regras de validação ou nos cálculos de subtotal/total é imediatamente detectada com indicação exata da linha e da entidade afetada.
  - **Garantia de pureza arquitetural:** os testes unitários comprovam empiricamente que a camada `src/domain/` não depende de detalhes de transporte ou armazenamento.
  - **Documentação executável:** as suítes de teste em `tests/unit/` servem como especificação viva dos comportamentos aceitos e rejeitados por cada entidade do sistema.
- **Negativas e trade-offs:**
  - **Manutenção de assinaturas:** refatorações estruturais no domínio (como quando `Pedido` passa a exigir `ItemPedido` ou uma fábrica em vez de aceitar diretamente listas de `Produto`) exigem atualização correspondente dos testes unitários das entidades afetadas.
  - **Não substitui testes de integração:** os testes unitários de domínio garantem a consistência lógica em memória, mas não substituem os testes em `tests/integration/` (mapeamento relacional ORM) nem em `tests/e2e/` (contrato HTTP REST).

## Evidências

- **Commits da implementação e evolução da suíte unitária:**
  - `b87b6fb` — `Add: Adicionados testes unitários para as entidades Cliente, Endereco, Entrega, Pedido, Produto e Restaurante` (estruturação inicial da suíte com 48 testes unitários passando com 100% de sucesso).
  - `ea8cb1d` — `Fix: Ajustes na Estrutura do Projeto` (configuração de `pytest.ini` e resolução do `pythonpath`).
  - `436a8ab` — `[Test] Testes unitários para a entidade ItemPedido` (cobertura do novo Value Object com cálculo de subtotal, validação de tipos, imutabilidade e igualdade por valor).
  - `299b640` — `[Test] Atualização dos testes unitários de Cliente e Endereco` (cobertura de UUID hex, associação/validação de `Endereco` e imutabilidade).
  - `e8f972c` — `[Test] Atualização dos testes unitários de Pedido e Restaurante` (testes de ID customizado e tuplas de itens).
  - `183a70f`, `4569297`, `67deecd`, `eb71869` e `13560d5` — inclusão de docstrings explicativas, testes de precisão decimal e fixtures reutilizáveis em `tests/conftest.py`.
- **Arquivos relacionados:**
  - `tests/unit/test_cliente.py`
  - `tests/unit/test_endereco.py`
  - `tests/unit/test_entrega.py`
  - `tests/unit/test_item_pedido.py`
  - `tests/unit/test_pedido.py`
  - `tests/unit/test_produto.py`
  - `tests/unit/test_restaurante.py`
  - `tests/conftest.py`
  - `pytest.ini` e `tests/pytest.ini`
