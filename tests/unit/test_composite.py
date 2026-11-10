import pytest

from src.domain.entities.combo import Combo, ComponenteItem, Item
from src.domain.entities.pedido import Pedido
from src.domain.entities.produto import Produto


def test_item_protocol_compliance_e_propriedades():
    item = Item("Hambúrguer", 25.00)

    assert isinstance(item, ComponenteItem)
    assert item.nome() == "Hambúrguer"
    assert item.preco() == 25.00
    assert repr(item) == "Item(nome='Hambúrguer', valor=25.0)"
    assert item == Item("Hambúrguer", 25.00)
    assert item != Item("Outro", 25.00)
    assert item != "não_item"


def test_item_converte_para_produto():
    item = Item("Suco de Laranja", 8.50)
    produto = item.para_produto()

    assert isinstance(produto, Produto)
    assert produto.nome == "Suco de Laranja"
    assert produto.preco == 8.50


@pytest.mark.parametrize(
    "nome_invalido",
    ["", "   ", None, 123],
)
def test_item_rejeita_nome_invalido(nome_invalido):
    with pytest.raises(ValueError, match="nome do item é obrigatório"):
        Item(nome_invalido, 10.0)


@pytest.mark.parametrize(
    "valor_invalido",
    [-0.01, -10.0, True, False, "10", None],
)
def test_item_rejeita_valor_invalido(valor_invalido):
    with pytest.raises(ValueError, match="valor do item não pode ser negativo"):
        Item("Item", valor_invalido)


def test_combo_criacao_e_manipulacao_de_filhos():
    combo = Combo("Combo Básico", 0.05)

    assert isinstance(combo, ComponenteItem)
    assert combo.nome() == "Combo Básico"
    assert combo.desconto == 0.05
    assert combo.filhos == ()
    assert combo.preco() == 0.0

    item1 = Item("Hambúrguer", 20.00)
    item2 = Item("Refrigerante", 5.00)

    combo.adicionar(item1).adicionar(item2)
    assert len(combo.filhos) == 2
    # Total 25.00 com 5% de desconto = 23.75
    assert combo.preco() == pytest.approx(23.75)

    combo.remover(item1)
    assert combo.filhos == (item2,)
    # Total 5.00 com 5% de desconto = 4.75
    assert combo.preco() == pytest.approx(4.75)


@pytest.mark.parametrize(
    "nome_invalido",
    ["", "   ", None, 123],
)
def test_combo_rejeita_nome_invalido(nome_invalido):
    with pytest.raises(ValueError, match="nome do combo é obrigatório"):
        Combo(nome_invalido)


@pytest.mark.parametrize(
    "desconto_invalido",
    [-0.01, 1.01, -1.0, 2.0, True, False, "0.1", None],
)
def test_combo_rejeita_desconto_invalido(desconto_invalido):
    with pytest.raises(ValueError, match="desconto deve ser um valor decimal entre 0.0 e 1.0"):
        Combo("Combo", desconto=desconto_invalido)


def test_combo_rejeita_adicao_de_objeto_incompativel():
    combo = Combo("Combo")
    with pytest.raises(ValueError, match="apenas instâncias de ComponenteItem podem ser adicionadas"):
        combo.adicionar("string_invalida")  # type: ignore


def test_cenario_slides_seminario_composite_arvore_de_precos():
    """Reproduz exatamente a árvore e valores apresentados nos slides 8, 9 e 10:

    - Hambúrguer: R$ 25.00
    - Suco: R$ 8.00
    - Combo Bebidas (2x Suco, desc 0%): R$ 16.00
    - Combo Casal (2x Burger + Batata G R$ 12 + Combo Bebidas, desc 10%): R$ 70.20
    - Sobremesa: R$ 10.00
    - Total esperado: R$ 80.20
    """
    burger = Item("Hambúrguer", 25.00)
    suco = Item("Suco", 8.00)

    combo_bebidas = Combo("Combo Bebidas", 0.0)
    combo_bebidas.adicionar(suco).adicionar(suco)
    assert combo_bebidas.preco() == 16.00

    batata_g = Item("Batata G", 12.00)
    combo_casal = Combo("Combo Casal", 0.10)
    combo_casal.adicionar(burger).adicionar(burger).adicionar(batata_g).adicionar(combo_bebidas)

    # Subtotal bruto: 25 + 25 + 12 + 16 = 78.00
    # Com 10% de desconto: 78 * 0.9 = 70.20
    assert combo_casal.preco() == pytest.approx(70.20)

    sobremesa = Item("Sobremesa", 10.00)

    # Cliente tratando folhas e nós compostos uniformemente
    itens_cardapio: list[ComponenteItem] = [combo_casal, sobremesa]
    total_direto = sum(item.preco() for item in itens_cardapio)
    assert total_direto == pytest.approx(80.20)

    # Integração com o agregado Pedido do domínio
    pedido = Pedido(
        cliente="João Gabriel",
        itens=[combo_casal.para_produto(), sobremesa.para_produto()],
    )
    assert pedido.total == pytest.approx(80.20)
