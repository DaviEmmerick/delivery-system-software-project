from uuid import uuid4
from typing import List
from src.domain.entities.produto import Produto

class Restaurante:
    def __init__(self, nome: str, id: str | None = None, produtos: List[Produto] | None = None):
        if not nome or not nome.strip():
            raise ValueError("nome é obrigatório")

        self.nome = nome.strip()
        self.id = id or uuid4().hex
        self.produtos = produtos or []
        
