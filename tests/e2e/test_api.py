"""Testes e2e da API Flask do sistema de delivery."""
import pytest

from src.entrypoints.flask_app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_criar_cliente_retorna_201(client):
    resposta = client.post("/clientes", json={"nome": "Ana", "telefone": "21999999999"})
    assert resposta.status_code == 201
    assert "cliente_id" in resposta.json


def test_criar_pedido_e_consultar(client):
    client.post("/clientes", json={"nome": "Carlos", "telefone": "21988888888"})
    resposta = client.post(
        "/pedidos",
        json={"cliente": "Carlos", "produtos": [{"nome": "Pizza", "preco": 45.5}]},
    )
    assert resposta.status_code == 201
    pedido_id = resposta.json["pedido_id"]

    consulta = client.get(f"/pedidos/{pedido_id}")
    assert consulta.status_code == 200
    assert consulta.json["cliente"] == "Carlos"
    assert consulta.json["total"] == 45.5


def test_atualizar_status_entrega(client):
    client.post("/clientes", json={"nome": "Maria", "telefone": "21977777777"})
    criacao = client.post(
        "/pedidos",
        json={"cliente": "Maria", "produtos": [{"nome": "Suco", "preco": 7.0}]},
    )
    pedido_id = criacao.json["pedido_id"]

    resposta = client.patch(f"/pedidos/{pedido_id}/entrega", json={"status": "em rota"})
    assert resposta.status_code == 200
    assert resposta.json["status"] == "em rota"


def test_consultar_pedido_inexistente_retorna_404(client):
    resposta = client.get("/pedidos/id-que-nao-existe")
    assert resposta.status_code == 404