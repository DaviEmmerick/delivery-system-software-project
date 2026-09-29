from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from src.adapters.orm import ClienteModel, PedidoItemModel, PedidoModel, RestauranteModel
from src.domain.entities.cliente import Cliente
from src.domain.entities.endereco import Endereco
from src.domain.entities.item_pedido import ItemPedido
from src.domain.entities.pedido import Pedido
from src.domain.entities.produto import Produto
from src.domain.entities.restaurante import Restaurante


T = TypeVar("T")


class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, entity_id: str) -> T | None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[T]:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository[T], ABC):
    model_type: type

    def __init__(self, engine: Engine):
        self._session_factory = sessionmaker(bind=engine)

    @abstractmethod
    def _to_model(self, entity: T):
        raise NotImplementedError

    @abstractmethod
    def _to_entity(self, model) -> T:
        raise NotImplementedError

    def add(self, entity: T) -> None:
        with self._session_factory.begin() as session:
            session.merge(self._to_model(entity))

    def get(self, entity_id: str) -> T | None:
        with self._session_factory() as session:
            model = session.get(self.model_type, entity_id)
            return self._to_entity(model) if model is not None else None

    def list(self) -> list[T]:
        with self._session_factory() as session:
            models = session.scalars(select(self.model_type).order_by(self.model_type.id)).all()
            return [self._to_entity(model) for model in models]


class ClienteRepository(SQLAlchemyRepository[Cliente]):
    model_type = ClienteModel

    def _to_model(self, entity: Cliente) -> ClienteModel:
        endereco = entity.endereco
        return ClienteModel(
            id=entity.id,
            nome=entity.nome,
            telefone=entity.telefone,
            endereco_rua=endereco.rua if endereco else None,
            endereco_numero=endereco.numero if endereco else None,
        )

    def _to_entity(self, model: ClienteModel) -> Cliente:
        endereco = None
        if model.endereco_rua is not None and model.endereco_numero is not None:
            endereco = Endereco(model.endereco_rua, model.endereco_numero)
        return Cliente(model.nome, model.telefone, endereco=endereco, id=model.id)


class RestauranteRepository(SQLAlchemyRepository[Restaurante]):
    model_type = RestauranteModel

    def _to_model(self, entity: Restaurante) -> RestauranteModel:
        return RestauranteModel(id=entity.id, nome=entity.nome)

    def _to_entity(self, model: RestauranteModel) -> Restaurante:
        return Restaurante(model.nome, id=model.id)


class PedidoRepository(SQLAlchemyRepository[Pedido]):
    model_type = PedidoModel

    def _to_model(self, entity: Pedido) -> PedidoModel:
        return PedidoModel(
            id=entity.id,
            cliente=entity.cliente,
            itens=[
                PedidoItemModel(
                    posicao=position,
                    produto_nome=item.produto.nome,
                    produto_preco=item.produto.preco,
                    quantidade=item.quantidade,
                )
                for position, item in enumerate(entity.itens)
            ],
        )

    def _to_entity(self, model: PedidoModel) -> Pedido:
        itens = [
            ItemPedido(
                Produto(item.produto_nome, float(item.produto_preco)),
                quantidade=item.quantidade,
            )
            for item in model.itens
        ]
        return Pedido(model.cliente, itens, id=model.id)