from abc import ABC, abstractmethod


class EstadoEntrega(ABC):
    status: str

    @abstractmethod
    def transicionar(self, novo_status: str) -> "EstadoEntrega":
        raise NotImplementedError

    def _transicao_invalida(self, novo_status: str) -> ValueError:
        return ValueError(
            f"transição de entrega inválida: {self.status} -> {novo_status}"
        )


class EntregaPendente(EstadoEntrega):
    status = "pendente"

    def transicionar(self, novo_status: str) -> EstadoEntrega:
        if novo_status == self.status:
            return self
        if novo_status == "em_transito":
            return EntregaEmTransito()
        if novo_status == "cancelada":
            return EntregaCancelada()
        raise self._transicao_invalida(novo_status)


class EntregaEmTransito(EstadoEntrega):
    status = "em_transito"

    def transicionar(self, novo_status: str) -> EstadoEntrega:
        if novo_status == self.status:
            return self
        if novo_status == "entregue":
            return EntregaConcluida()
        if novo_status == "cancelada":
            return EntregaCancelada()
        raise self._transicao_invalida(novo_status)


class EntregaConcluida(EstadoEntrega):
    status = "entregue"

    def transicionar(self, novo_status: str) -> EstadoEntrega:
        if novo_status == self.status:
            return self
        raise self._transicao_invalida(novo_status)


class EntregaCancelada(EstadoEntrega):
    status = "cancelada"

    def transicionar(self, novo_status: str) -> EstadoEntrega:
        if novo_status == self.status:
            return self
        raise self._transicao_invalida(novo_status)


class Entrega:
    def __init__(self, pedido_id: str, status: str = "pendente"):
        if not isinstance(pedido_id, str) or not pedido_id.strip():
            raise ValueError("pedido_id é obrigatório")
        if not isinstance(status, str) or not status.strip():
            raise ValueError("status é obrigatório")

        self.pedido_id = pedido_id.strip()
        estados = {
            "pendente": EntregaPendente,
            "em_transito": EntregaEmTransito,
            "entregue": EntregaConcluida,
            "cancelada": EntregaCancelada,
        }
        status_normalizado = status.strip()
        if status_normalizado not in estados:
            raise ValueError(f"status inválido: {status_normalizado}")
        self._estado = estados[status_normalizado]()

    @property
    def status(self) -> str:
        return self._estado.status

    def atualizar_status(self, novo_status: str) -> None:
        if not isinstance(novo_status, str) or not novo_status.strip():
            raise ValueError("status inválido")
        self._estado = self._estado.transicionar(novo_status.strip())
