from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from src.adapters.orm import create_sqlite_engine
from src.adapters.repository import ClienteRepository, PedidoRepository, RestauranteRepository
from src.service_layer import services

def _corpo_json() -> dict:
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        raise ValueError("o corpo da requisição deve ser um objeto JSON")
    return dados

def _texto(dados: dict, campo: str, obrigatorio: bool = True) -> str | None:
    valor = dados.get(campo)
    if valor is None and not obrigatorio:
        return None
    if not isinstance(valor, str):
        raise ValueError(f"campo '{campo}' é obrigatório e deve ser texto")
    return valor

def create_app(cliente_repo=None, restaurante_repo=None, pedido_repo=None, entregas=None) -> Flask:
    """Monta a API. Sem argumentos usa SQLite em memória; nos testes dá para injetar repositórios."""
    if cliente_repo is None or restaurante_repo is None or pedido_repo is None:
        engine = create_sqlite_engine()
        if cliente_repo is None:
            cliente_repo = ClienteRepository(engine)
        if restaurante_repo is None:
            restaurante_repo = RestauranteRepository(engine)
        if pedido_repo is None:
            pedido_repo = PedidoRepository(engine)
    if entregas is None:
        entregas = {}
    app = Flask(__name__)

    @app.errorhandler(services.NaoEncontrado)
    def _nao_encontrado(erro):
        return jsonify({"erro": str(erro)}), 404

    @app.errorhandler(services.Conflito)
    def _conflito(erro):
        return jsonify({"erro": str(erro)}), 409

    @app.errorhandler(ValueError)
    def _requisicao_invalida(erro):
        return jsonify({"erro": str(erro)}), 400

    @app.errorhandler(HTTPException)
    def _erro_http(erro):
        return jsonify({"erro": erro.description}), erro.code

    @app.post("/clientes")
    def criar_cliente():
        dados = _corpo_json()
        cliente_id = services.criar_cliente(
            nome=_texto(dados, "nome"),
            telefone=_texto(dados, "telefone"),
            rua=_texto(dados, "rua", obrigatorio=False),
            numero=_texto(dados, "numero", obrigatorio=False),
            cliente_repo=cliente_repo,)
        return jsonify({"cliente_id": cliente_id}), 201

    @app.get("/clientes/<cliente_id>")
    def consultar_cliente(cliente_id):
        cliente = services.consultar_cliente(cliente_id, cliente_repo)
        endereco = None
        if cliente.endereco is not None:
            endereco = {"rua": cliente.endereco.rua, "numero": cliente.endereco.numero}
        return jsonify(
            {"id": cliente.id, "nome": cliente.nome, "telefone": cliente.telefone, "endereco": endereco}), 200

    @app.get("/clientes/<cliente_id>/pedidos")
    def listar_pedidos_do_cliente(cliente_id):
        pedidos = services.listar_pedidos_do_cliente(cliente_id, cliente_repo, pedido_repo)
        return jsonify(
            [{"id": p.id, "cliente_id": p.cliente, "total": p.total} for p in pedidos]), 200

    @app.post("/restaurantes")
    def criar_restaurante():
        dados = _corpo_json()
        restaurante_id = services.criar_restaurante(
            nome=_texto(dados, "nome"),
            restaurante_repo=restaurante_repo,
            produtos=dados.get("produtos"),
        )
        return jsonify({"restaurante_id": restaurante_id}), 201

    @app.get("/restaurantes")
    def listar_restaurantes():
        restaurantes = services.listar_restaurantes(restaurante_repo)
        return jsonify([{"id": r.id, "nome": r.nome} for r in restaurantes]), 200

    @app.post("/pedidos")
    def criar_pedido():
        dados = _corpo_json()
        pedido_id = services.criar_pedido(
            cliente_id=_texto(dados, "cliente_id"),
            produtos=dados.get("produtos"),
            cliente_repo=cliente_repo,
            pedido_repo=pedido_repo,
            entregas=entregas,)
        return jsonify({"pedido_id": pedido_id}), 201

    @app.get("/pedidos/<pedido_id>")
    def consultar_pedido(pedido_id):
        pedido = services.consultar_pedido(pedido_id, pedido_repo)
        status = services.consultar_status_entrega(pedido_id, entregas)
        return jsonify(
            {
                "id": pedido.id,
                "cliente_id": pedido.cliente,
                "total": pedido.total,
                "status_entrega": status,
                "itens": [
                    {
                        "nome": item.produto.nome,
                        "preco": item.produto.preco,
                        "quantidade": item.quantidade,
                        "subtotal": item.subtotal,
                    }
                    for item in pedido.itens
                ],
            }
        ), 200

    @app.patch("/pedidos/<pedido_id>/entrega")
    def atualizar_status_entrega(pedido_id):
        dados = _corpo_json()
        status = services.atualizar_status_entrega(pedido_id, _texto(dados, "status"), entregas)
        return jsonify({"status": status}), 200

    return app

app = create_app()

if __name__ == "__main__":
    app.run(port=5000)
