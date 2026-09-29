from uuid import uuid4
from typing import List

from src.domain.entities.produto import Produto


class Restaurante:
    def __init__(self, nome: str, id: str | None = None, produtos: List[Produto] | None = None):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("nome é obrigatório")
        try:
            produtos_normalizados = list(produtos or [])
        except TypeError:
            raise ValueError("produtos devem ser instâncias de Produto") from None
        if any(not isinstance(produto, Produto) for produto in produtos_normalizados):
            raise ValueError("produtos devem ser instâncias de Produto")

        self.nome = nome.strip()
        self.id = id or uuid4().hex
        self.produtos = produtos_normalizados

