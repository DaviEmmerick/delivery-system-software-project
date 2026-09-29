import math


class Produto:
    def __init__(self, nome: str, preco: float):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("nome do produto é obrigatório")
        try:
            preco_normalizado = float(preco)
        except (TypeError, ValueError):
            raise ValueError("preço deve ser um número") from None
        if not math.isfinite(preco_normalizado) or preco_normalizado < 0:
            raise ValueError("preço não pode ser negativo")

        self.nome = nome.strip()
        self.preco = preco_normalizado
