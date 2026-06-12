import pytest


def test_listar_produtos_banco_vazio(client):
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == []


def test_criar_produto_retorna_id(client):
    response = client.post(
        "/produtos",
        json={"nome": "Borracha", "preco": 2.50, "estoque": 30}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Borracha"
    assert data["preco"] == 2.50
    assert "id" in data


def test_produto_criado_aparece_na_listagem(client):
    client.post("/produtos", json={"nome": "Régua", "preco": 1.90})
    response = client.get("/produtos")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_buscar_produto_por_id(client, produto_existente):
    produto_id = produto_existente["id"]
    response = client.get(f"/produtos/{produto_id}")
    assert response.status_code == 200
    assert response.json()["nome"] == "Produto Teste"


def test_buscar_produto_inexistente_retorna_404(client):
    response = client.get("/produtos/9999")
    assert response.status_code == 404


def test_deletar_produto_retorna_204(client, produto_existente):
    produto_id = produto_existente["id"]
    response = client.delete(f"/produtos/{produto_id}")
    assert response.status_code == 204


def test_deletar_produto_confirma_remocao(client, produto_existente):
    produto_id = produto_existente["id"]
    client.delete(f"/produtos/{produto_id}")
    response = client.get(f"/produtos/{produto_id}")
    assert response.status_code == 404


def test_deletar_produto_inexistente_retorna_404(client):
    response = client.delete("/produtos/9999")
    assert response.status_code == 404


@pytest.mark.parametrize("payload", [
    {"nome": "Produto sem preco"},
    {"preco": 10.0},
    {"nome": "", "preco": "texto"},
    {"nome": "Produto", "preco": "abc"},
])
def test_payload_invalido_retorna_422(client, payload):
    response = client.post("/produtos", json=payload)
    assert response.status_code == 422


def test_banco_isolado_entre_testes(client):
    client.post("/produtos", json={"nome": "Caderno", "preco": 8.00})
    response = client.get("/produtos")
    assert len(response.json()) == 1
