# Aplicação Flask para endpoints da API.
from flask import Flask, jsonify, request

from src.service_layer import services

app = Flask(__name__)


@app.route("/clientes", methods=["POST"])
def criar_cliente_endpoint():
    dados = request.json
    try:
        cliente_id = services.criar_cliente(
            nome=dados["nome"],
            telefone=dados["telefone"],
            rua=dados.get("rua"),
            numero=dados.get("numero"),
        )
        return jsonify({"cliente_id": cliente_id}), 201
    except (ValueError, KeyError) as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/restaurantes", methods=["POST"])
def criar_restaurante_endpoint():
    dados = request.json
    try:
        restaurante_id = services.criar_restaurante(
            nome=dados["nome"],
            produtos=dados.get("produtos"),
        )
        return jsonify({"restaurante_id": restaurante_id}), 201
    except (ValueError, KeyError) as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/pedidos", methods=["POST"])
def criar_pedido_endpoint():
    dados = request.json
    try:
        pedido_id = services.criar_pedido(
            cliente=dados["cliente"],
            produtos=dados["produtos"],
        )
        return jsonify({"pedido_id": pedido_id}), 201
    except (ValueError, KeyError) as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/pedidos/<pedido_id>", methods=["GET"])
def consultar_pedido_endpoint(pedido_id):
    try:
        pedido = services.consultar_pedido(pedido_id)
        return jsonify({
            "id": pedido.id,
            "cliente": pedido.cliente,
            "total": pedido.total,
            "itens": [item.produto.nome for item in pedido.itens],
        }), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@app.route("/pedidos/<pedido_id>/entrega", methods=["PATCH"])
def atualizar_status_entrega_endpoint(pedido_id):
    dados = request.json
    try:
        status = services.atualizar_status_entrega(pedido_id, dados["status"])
        return jsonify({"status": status}), 200
    except (ValueError, KeyError) as e:
        return jsonify({"erro": str(e)}), 404


@app.route("/clientes/<cliente>/pedidos", methods=["GET"])
def listar_pedidos_do_cliente_endpoint(cliente):
    pedidos = services.listar_pedidos_do_cliente(cliente)
    return jsonify([{"id": p.id, "cliente": p.cliente, "total": p.total} for p in pedidos]), 200


if __name__ == "__main__":
    app.run(port=5000)