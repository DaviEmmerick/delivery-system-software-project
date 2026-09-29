from uuid import uuid4


class Restaurante:
    def __init__(self, nome: str, id: str | None = None):
        if not nome or not nome.strip():
            raise ValueError("nome é obrigatório")

        self.nome = nome.strip()
        self.id = id or uuid4().hex
