from src.domain.entities.produto import Produto


class Pedido:
    def __init__(self, cliente: str, itens: list[Produto]):
        if not cliente or not cliente.strip():
            raise ValueError("cliente é obrigatório")
        if not itens:
            raise ValueError("pedido deve conter ao menos um item")

        self.cliente = cliente.strip()
        self.itens = itens
        self.total = sum(item.preco for item in itens)
