class Restaurante:
    def __init__(self, nome: str):
        if not nome or not nome.strip():
            raise ValueError("nome é obrigatório")

        self.nome = nome.strip()
