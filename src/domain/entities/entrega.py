class Entrega:
    def __init__(self, pedido_id: str, status: str = "pendente"):
        if not pedido_id or not pedido_id.strip():
            raise ValueError("pedido_id é obrigatório")

        self.pedido_id = pedido_id.strip()
        self.status = status
