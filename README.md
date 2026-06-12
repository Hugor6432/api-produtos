# API de Produtos

API REST para gerenciamento de produtos, desenvolvida com FastAPI e PostgreSQL.

## Como executar os testes

### 1. Subir o banco de dados de teste

```bash
docker-compose up -d db_test
```

Aguarde alguns segundos para o banco iniciar.

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Rodar os testes

```bash
python -m pytest --cov=main -v
```

## Saída esperada

```
tests/test_produtos.py::test_listar_produtos_banco_vazio PASSED
tests/test_produtos.py::test_criar_produto_retorna_id PASSED
tests/test_produtos.py::test_produto_criado_aparece_na_listagem PASSED
tests/test_produtos.py::test_buscar_produto_por_id PASSED
tests/test_produtos.py::test_buscar_produto_inexistente_retorna_404 PASSED
tests/test_produtos.py::test_deletar_produto_retorna_204 PASSED
tests/test_produtos.py::test_deletar_produto_confirma_remocao PASSED
tests/test_produtos.py::test_deletar_produto_inexistente_retorna_404 PASSED
tests/test_produtos.py::test_payload_invalido_retorna_422[...] PASSED (x4)
tests/test_produtos.py::test_banco_isolado_entre_testes PASSED
```

## Como o isolamento funciona

Cada teste recebe um banco limpo. A fixture `client` no `conftest.py` cria as tabelas antes do teste com `create_all` e destrói tudo depois com `drop_all`. Isso garante que nenhum dado de um teste interfere no próximo.
