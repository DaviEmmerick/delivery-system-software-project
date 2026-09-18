class Cliente:
    def __init__(self, nome: str, telefone: str):
        if not nome or not nome.strip():
            raise ValueError("nome é obrigatório")
        if not telefone or len(telefone.strip()) < 10:
            raise ValueError("telefone inválido")

        self.nome = nome.strip()
        self.telefone = telefone.strip()
