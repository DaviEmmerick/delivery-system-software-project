# ADR 0003: Validar e organizar os dados no domínio

- **Responsável:** Leandro Machado Cardoso da Cunha
- **Status:** decisão implementada na Fase 1 (commits `cb7d31a`, `7875dc1`, `ca6d033` e `1213e36`)
- **Data:** 22/10/2026

## Contexto

Os dados chegam à API como JSON e podem ter tipos errados. Por exemplo, um `nome` pode ser número, um `preco` pode ser texto ou `NaN`, e uma lista de produtos pode ser `null`.

Antes, as entidades verificavam apenas se os valores estavam vazios. Quando recebiam um tipo errado, geravam `AttributeError` em vez de `ValueError`. Assim, a API respondia com erro interno, e não com HTTP 400. Além disso, o `Restaurante` ainda não recebia produtos, embora o serviço de criação precisasse deles.

Isso pode deixar dados inválidos no sistema. Se uma entidade inválida for criada, qualquer serviço ou repositório pode salvá-la.

## Decisão

1. **As entidades fazem a validação final.** Cada entidade rejeita tipos inválidos com `ValueError` e uma mensagem clara.
2. **O domínio organiza os dados.** Textos usam `strip()`. O preço de `Produto` vira `float`, deve ser finito e não pode ser negativo. Valores não numéricos geram `ValueError`.
3. **`Restaurante` tem uma lista de `produtos`.** A lista é normalizada e cada item precisa ser um `Produto`.
4. **Os serviços validam apenas o formato do JSON.** Eles montam os produtos e itens antes de criar as entidades. O status da entrega é normalizado e comparado com `STATUS_ENTREGA`. Ao atualizar uma entrega, uma nova entidade é criada e validada.
5. **A API não valida regras de negócio.** Ela envia os dados para os serviços. O campo `produtos` é recebido na criação do restaurante, e todo `ValueError` vira HTTP 400.

## Alternativas consideradas

- **Validar apenas na API (Flask).** Seria simples, mas outros pontos do sistema poderiam criar entidades inválidas.
- **Usar uma biblioteca de esquemas (Pydantic ou Marshmallow).** Reduziria código manual, mas criaria uma dependência e levaria parte das regras para fora das entidades.
- **Confiar no banco (`NOT NULL`, `UNIQUE`).** Protegeria os dados salvos, mas não validaria regras como preço finito e status válido.

## Consequências

- (+) Entidades inválidas são rejeitadas, independentemente de onde foram criadas.
- (+) Erros de entrada viram `ValueError` e a API responde HTTP 400. Os testes e2e verificam esse comportamento em 16 casos.
- (+) O domínio continua independente de Flask e SQLAlchemy.
- (−) Algumas validações são repetidas no serviço e no domínio.
- (−) `isinstance(..., str)` rejeita valores que poderiam ser convertidos para texto.
- (−) A mensagem para preços `NaN` ou infinitos diz apenas que o preço não pode ser negativo.
- (−) **Risco:** `Restaurante.produtos` é validado, mas o repositório salva apenas `id` e `nome`. Os produtos informados na criação são perdidos.

## Evidências

- As entidades usam `ValueError` para rejeitar entradas inválidas, e os testes unitários cobrem essas validações com `pytest.raises`.
- Foram testados casos inválidos como `Produto("x", "abc")`, `Produto(123, 1)`, `Restaurante("r", produtos=[1])`, `Pedido("c", 5)` e `Entrega("p", None)`.
- Os arquivos `src/adapters/repository.py` e `src/adapters/orm.py` não usam `produtos`, confirmando o risco de perda desses dados.