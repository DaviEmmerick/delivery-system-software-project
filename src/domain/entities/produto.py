class Produto:
    def __init__(self, nome: str, preco: float):
        if not nome or not nome.strip():
            raise ValueError("nome do produto é obrigatório")
        if preco < 0:
            raise ValueError("preço não pode ser negativo")

        self.nome = nome.strip()
        self.preco = float(preco)
