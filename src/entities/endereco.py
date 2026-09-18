class Endereco:
    def __init__(self, rua: str, numero: str):
        if not rua or not rua.strip():
            raise ValueError("rua é obrigatória")
        if not numero or not numero.strip():
            raise ValueError("número é obrigatório")

        self.rua = rua.strip()
        self.numero = numero.strip()
