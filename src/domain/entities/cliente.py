from src.domain.entities.endereco import Endereco


class Cliente:
    def __init__(self, nome: str, telefone: str, endereco: Endereco | None = None):
        if not nome or not nome.strip():
            raise ValueError("nome é obrigatório")
        if not telefone or len(telefone.strip()) < 10:
            raise ValueError("telefone inválido")
        if endereco is not None and not isinstance(endereco, Endereco):
            raise ValueError("endereco deve ser um Endereco")

        self.nome = nome.strip()
        self.telefone = telefone.strip()
        self.endereco = endereco
