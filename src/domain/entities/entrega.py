class Entrega:
    def __init__(self, pedido_id: str, status: str = "pendente"):
        if not isinstance(pedido_id, str) or not pedido_id.strip():
            raise ValueError("pedido_id é obrigatório")
        if not isinstance(status, str) or not status.strip():
            raise ValueError("status é obrigatório")

        self.pedido_id = pedido_id.strip()
        self.status = status.strip()
