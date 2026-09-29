import pytest
from src.entrypoints.flask_app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def _criar_cliente(client, nome="Ana", telefone="21999999999", **extra):
    resposta = client.post("/clientes", json={"nome": nome, "telefone": telefone, **extra})
    assert resposta.status_code == 201
    return resposta.json["cliente_id"]


def _criar_pedido(client, cliente_id, produtos=None):
    produtos = produtos or [{"nome": "Pizza", "preco": 45.5}]
    resposta = client.post("/pedidos", json={"cliente_id": cliente_id, "produtos": produtos})
    assert resposta.status_code == 201
    return resposta.json["pedido_id"]

def test_criar_cliente_retorna_201(client):
    resposta = client.post("/clientes", json={"nome": "Ana", "telefone": "21999999999"})
    assert resposta.status_code == 201
    assert "cliente_id" in resposta.json

def test_consultar_cliente_com_endereco(client):
    cliente_id = _criar_cliente(client, rua="Rua das Flores", numero="10")
    resposta = client.get(f"/clientes/{cliente_id}")
    assert resposta.status_code == 200
    assert resposta.json["nome"] == "Ana"
    assert resposta.json["endereco"] == {"rua": "Rua das Flores", "numero": "10"}

def test_consultar_cliente_sem_endereco(client):
    cliente_id = _criar_cliente(client)
    assert client.get(f"/clientes/{cliente_id}").json["endereco"] is None

def test_criar_cliente_com_telefone_curto_retorna_400(client):
    resposta = client.post("/clientes", json={"nome": "Bia", "telefone": "123"})
    assert resposta.status_code == 400
    assert "telefone" in resposta.json["erro"]

def test_criar_cliente_com_telefone_duplicado_retorna_409(client):
    _criar_cliente(client, "Ana", "21999999999")
    resposta = client.post("/clientes", json={"nome": "Outra", "telefone": "21999999999"})
    assert resposta.status_code == 409

@pytest.mark.parametrize(
    "corpo",
    [
        {},
        {"nome": "Ana"},
        {"telefone": "21999999999"},
        {"nome": 123, "telefone": "21999999999"},
        {"nome": "Ana", "telefone": "21999999999", "rua": "Rua A"},
    ],)
def test_criar_cliente_com_corpo_invalido_retorna_400(client, corpo):
    assert client.post("/clientes", json=corpo).status_code == 400

def test_corpo_que_nao_e_json_retorna_400_em_json(client):
    resposta = client.post("/clientes", data="nome=Ana")
    assert resposta.status_code == 400
    assert "erro" in resposta.json

def test_consultar_cliente_inexistente_retorna_404(client):
    assert client.get("/clientes/nao-existe").status_code == 404

def test_criar_e_listar_restaurantes(client):
    resposta = client.post("/restaurantes", json={"nome": "Cantina"})
    assert resposta.status_code == 201
    restaurante_id = resposta.json["restaurante_id"]

    listagem = client.get("/restaurantes")
    assert listagem.status_code == 200
    assert listagem.json == [{"id": restaurante_id, "nome": "Cantina"}]

def test_criar_restaurante_duplicado_retorna_409(client):
    client.post("/restaurantes", json={"nome": "Cantina"})
    assert client.post("/restaurantes", json={"nome": "Cantina"}).status_code == 409

def test_criar_restaurante_sem_nome_retorna_400(client):
    assert client.post("/restaurantes", json={}).status_code == 400

def test_criar_pedido_e_consultar(client):
    cliente_id = _criar_cliente(client, "Carlos", "21988888888")
    pedido_id = _criar_pedido(client, cliente_id, [{"nome": "Pizza", "preco": 45.5}])
    consulta = client.get(f"/pedidos/{pedido_id}")
    assert consulta.status_code == 200
    assert consulta.json["cliente_id"] == cliente_id
    assert consulta.json["total"] == 45.5
    assert consulta.json["status_entrega"] == "pendente"

def test_total_do_pedido_considera_quantidade(client):
    cliente_id = _criar_cliente(client)
    pedido_id = _criar_pedido(
        client, cliente_id, [{"nome": "Coca", "preco": 5.0, "quantidade": 3}, {"nome": "Pizza", "preco": 40.0}])
    consulta = client.get(f"/pedidos/{pedido_id}").json
    assert consulta["total"] == 55.0
    assert consulta["itens"][0] == {"nome": "Coca", "preco": 5.0, "quantidade": 3, "subtotal": 15.0}

def test_criar_pedido_para_cliente_inexistente_retorna_404(client):
    resposta = client.post(
        "/pedidos", json={"cliente_id": "fantasma", "produtos": [{"nome": "X", "preco": 1.0}]})
    assert resposta.status_code == 404

@pytest.mark.parametrize(
    "produtos",
    [
        [],
        "abc",
        None,
        [{"nome": "X"}],
        [{"nome": "X", "preco": "abc"}],
        [{"nome": "X", "preco": -5}],
        [{"nome": "X", "preco": 10, "quantidade": 0}],
    ],)
def test_criar_pedido_com_produtos_invalidos_retorna_400(client, produtos):
    cliente_id = _criar_cliente(client)
    resposta = client.post("/pedidos", json={"cliente_id": cliente_id, "produtos": produtos})
    assert resposta.status_code == 400

def test_criar_pedido_sem_cliente_id_retorna_400(client):
    resposta = client.post("/pedidos", json={"produtos": [{"nome": "X", "preco": 1.0}]})
    assert resposta.status_code == 400

def test_consultar_pedido_inexistente_retorna_404(client):
    assert client.get("/pedidos/id-que-nao-existe").status_code == 404

def test_listar_pedidos_do_cliente_retorna_so_os_dele(client):
    ana = _criar_cliente(client, "Ana", "21999999999")
    outra_ana = _criar_cliente(client, "Ana", "21988888888")
    pedido_ana = _criar_pedido(client, ana)
    _criar_pedido(client, outra_ana)
    resposta = client.get(f"/clientes/{ana}/pedidos")
    assert resposta.status_code == 200
    assert [p["id"] for p in resposta.json] == [pedido_ana]


def test_listar_pedidos_de_cliente_inexistente_retorna_404(client):
    assert client.get("/clientes/nao-existe/pedidos").status_code == 404


def test_atualizar_status_entrega(client):
    pedido_id = _criar_pedido(client, _criar_cliente(client))

    resposta = client.patch(f"/pedidos/{pedido_id}/entrega", json={"status": "em_transito"})
    assert resposta.status_code == 200
    assert resposta.json["status"] == "em_transito"
    assert client.get(f"/pedidos/{pedido_id}").json["status_entrega"] == "em_transito"


def test_atualizar_status_entrega_invalido_retorna_400(client):
    pedido_id = _criar_pedido(client, _criar_cliente(client))
    resposta = client.patch(f"/pedidos/{pedido_id}/entrega", json={"status": "banana"})
    assert resposta.status_code == 400
    assert client.get(f"/pedidos/{pedido_id}").json["status_entrega"] == "pendente"


def test_atualizar_status_entrega_sem_status_retorna_400(client):
    pedido_id = _criar_pedido(client, _criar_cliente(client))
    assert client.patch(f"/pedidos/{pedido_id}/entrega", json={}).status_code == 400


def test_atualizar_status_entrega_de_pedido_inexistente_retorna_404(client):
    resposta = client.patch("/pedidos/nao-existe/entrega", json={"status": "entregue"})
    assert resposta.status_code == 404


def test_rota_inexistente_retorna_404_em_json(client):
    resposta = client.get("/rota-que-nao-existe")
    assert resposta.status_code == 404
    assert "erro" in resposta.json
