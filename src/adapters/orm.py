from sqlalchemy import ForeignKey, Integer, Numeric, String, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


class ClienteModel(Base):
    __tablename__ = "clientes"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    telefone: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    endereco_rua: Mapped[str | None] = mapped_column(String(200), nullable=True)
    endereco_numero: Mapped[str | None] = mapped_column(String(30), nullable=True)


class RestauranteModel(Base):
    __tablename__ = "restaurantes"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)


class PedidoModel(Base):
    __tablename__ = "pedidos"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    cliente: Mapped[str] = mapped_column(String(200), nullable=False)
    itens: Mapped[list["PedidoItemModel"]] = relationship(
        back_populates="pedido",
        cascade="all, delete-orphan",
        order_by="PedidoItemModel.posicao",
    )


class PedidoItemModel(Base):
    __tablename__ = "pedido_itens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pedido_id: Mapped[str] = mapped_column(ForeignKey("pedidos.id", ondelete="CASCADE"))
    posicao: Mapped[int] = mapped_column(Integer, nullable=False)
    produto_nome: Mapped[str] = mapped_column(String(200), nullable=False)
    produto_preco: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    pedido: Mapped[PedidoModel] = relationship(back_populates="itens")


def create_sqlite_engine(database_url: str = "sqlite+pysqlite:///:memory:") -> Engine:
    engine_options = {}
    if database_url.endswith(":memory:"):
        engine_options["poolclass"] = StaticPool
    if database_url.startswith("sqlite"):
        engine_options["connect_args"] = {"check_same_thread": False}

    engine = create_engine(database_url, **engine_options)
    Base.metadata.create_all(engine)
    return engine