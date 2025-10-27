# Exemplos de Uso dos Testes

Este documento mostra exemplos práticos de como usar a estrutura de testes.

## Exemplo 1: Executar Todos os Testes

```bash
# Na raiz do projeto (/mnt/c/Projetos/DefaultWebApp)
pytest

# Com mais detalhes
pytest -v

# Com prints e detalhes
pytest -v -s
```

**Saída esperada:**
```
================================ test session starts =================================
tests/test_auth.py::TestLogin::test_get_login_retorna_formulario PASSED       [ 2%]
tests/test_auth.py::TestLogin::test_login_com_credenciais_validas PASSED      [ 4%]
...
================================ 48 passed in 5.23s =================================
```

## Exemplo 2: Executar Apenas Testes de Autenticação

```bash
pytest tests/test_auth.py -v
```

**Saída esperada:**
```
tests/test_auth.py::TestLogin::test_get_login_retorna_formulario PASSED
tests/test_auth.py::TestLogin::test_login_com_credenciais_validas PASSED
tests/test_auth.py::TestLogin::test_login_com_email_invalido PASSED
...
======================= 23 passed in 2.45s ========================
```

## Exemplo 3: Executar Apenas Testes de Tarefas

```bash
pytest tests/test_tarefas.py -v
```

## Exemplo 4: Executar Teste Específico

```bash
# Executar apenas um teste específico
pytest tests/test_auth.py::TestLogin::test_login_com_credenciais_validas -v

# Executar todos os testes de uma classe
pytest tests/test_auth.py::TestLogin -v

# Executar testes que contenham "cadastro" no nome
pytest -k "cadastro" -v
```

## Exemplo 5: Parar no Primeiro Erro

```bash
# Útil para debug
pytest -x -v
```

## Exemplo 6: Ver Detalhes de Variáveis em Falhas

```bash
# Mostra valores de variáveis quando teste falha
pytest -v --tb=long

# Mostra apenas traceback curto (padrão)
pytest -v --tb=short

# Mostra traceback muito detalhado
pytest -vv --tb=long
```

## Exemplo 7: Executar com Cobertura de Código

```bash
# Instalar pytest-cov primeiro
pip install pytest-cov

# Executar com cobertura
pytest --cov=. --cov-report=term-missing

# Gerar relatório HTML
pytest --cov=. --cov-report=html

# Abrir relatório (o arquivo estará em htmlcov/index.html)
```

**Saída esperada:**
```
---------- coverage: platform linux, python 3.10.x -----------
Name                               Stmts   Miss  Cover   Missing
----------------------------------------------------------------
main.py                               45      5    89%   23-27
repo/usuario_repo.py                  56      2    96%   45, 67
routes/auth_routes.py                 89      3    97%   156-158
tests/conftest.py                     42      0   100%
tests/test_auth.py                   156      0   100%
tests/test_tarefas.py                178      0   100%
----------------------------------------------------------------
TOTAL                                566     10    98%
```

## Exemplo 8: Executar Testes com Marcadores

```bash
# Executar apenas testes marcados como "auth"
pytest -m auth -v

# Executar tudo exceto testes lentos
pytest -m "not slow" -v

# Executar testes de CRUD
pytest -m crud -v
```

## Exemplo 9: Modo Watch (Executar ao Salvar)

```bash
# Instalar pytest-watch
pip install pytest-watch

# Executar em modo watch
ptw
```

## Exemplo 10: Testes em Paralelo (Mais Rápido)

```bash
# Instalar pytest-xdist
pip install pytest-xdist

# Executar em paralelo (4 workers)
pytest -n 4

# Executar usando todos os cores disponíveis
pytest -n auto
```

## Exemplo 11: Criar Novo Teste

Arquivo: `tests/test_perfil.py`

```python
"""Testes de perfil de usuário"""
import pytest
from fastapi import status


class TestPerfilUsuario:
    """Testes de visualização e edição de perfil"""

    def test_visualizar_perfil_requer_autenticacao(self, client):
        """Deve exigir autenticação para visualizar perfil"""
        response = client.get("/perfil", follow_redirects=False)
        assert response.status_code == status.HTTP_303_SEE_OTHER

    def test_usuario_autenticado_visualiza_perfil(self, cliente_autenticado):
        """Usuário autenticado deve visualizar seu perfil"""
        response = cliente_autenticado.get("/perfil")
        assert response.status_code == status.HTTP_200_OK
        assert "perfil" in response.text.lower()

    def test_editar_nome_usuario(self, cliente_autenticado):
        """Deve permitir editar nome do usuário"""
        response = cliente_autenticado.post("/perfil/editar", data={
            "nome": "Novo Nome"
        }, follow_redirects=False)

        assert response.status_code == status.HTTP_303_SEE_OTHER

        # Verificar que nome foi alterado
        from repo import usuario_repo
        usuario = usuario_repo.obter_por_id(1)
        assert usuario.nome == "Novo Nome"
```

Executar:
```bash
pytest tests/test_perfil.py -v
```

## Exemplo 12: Usar Fixtures Personalizadas

```python
# No seu teste
def test_criar_multiplos_usuarios(client, criar_usuario):
    """Teste que cria múltiplos usuários"""
    usuarios = [
        ("Usuario 1", "user1@test.com", "Senha@123"),
        ("Usuario 2", "user2@test.com", "Senha@123"),
        ("Usuario 3", "user3@test.com", "Senha@123"),
    ]

    for nome, email, senha in usuarios:
        response = criar_usuario(nome, email, senha)
        assert response.status_code == status.HTTP_303_SEE_OTHER

    # Verificar que todos foram criados
    from repo import usuario_repo
    todos = usuario_repo.obter_todos()
    assert len(todos) >= 3
```

## Exemplo 13: Testar com Dados Inválidos

```python
import pytest

@pytest.mark.parametrize("email,senha", [
    ("", "Senha@123"),                    # E-mail vazio
    ("invalido", "Senha@123"),            # E-mail inválido
    ("teste@test.com", ""),               # Senha vazia
    ("teste@test.com", "123"),            # Senha fraca
    ("", ""),                             # Ambos vazios
])
def test_login_com_dados_invalidos(client, email, senha):
    """Deve rejeitar login com dados inválidos"""
    response = client.post("/login", data={
        "email": email,
        "senha": senha
    }, follow_redirects=True)

    # Não deve fazer login com sucesso
    assert "inválid" in response.text.lower() or response.status_code == 422
```

Executar:
```bash
pytest tests/test_auth.py::test_login_com_dados_invalidos -v
```

## Exemplo 14: Testar Fluxo Completo

```python
def test_fluxo_completo_usuario(client):
    """Testa fluxo completo: cadastro > login > criar tarefa > logout"""

    # 1. Cadastrar usuário
    response = client.post("/cadastro", data={
        "nome": "Usuario Completo",
        "email": "completo@test.com",
        "senha": "Senha@123",
        "confirmar_senha": "Senha@123"
    }, follow_redirects=False)
    assert response.status_code == status.HTTP_303_SEE_OTHER

    # 2. Fazer login
    response = client.post("/login", data={
        "email": "completo@test.com",
        "senha": "Senha@123"
    }, follow_redirects=False)
    assert response.status_code == status.HTTP_303_SEE_OTHER

    # 3. Criar tarefa
    response = client.post("/tarefas/cadastrar", data={
        "titulo": "Minha Primeira Tarefa",
        "descricao": "Descrição da tarefa"
    }, follow_redirects=False)
    assert response.status_code == status.HTTP_303_SEE_OTHER

    # 4. Listar tarefas
    response = client.get("/tarefas")
    assert "Minha Primeira Tarefa" in response.text

    # 5. Fazer logout
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == status.HTTP_303_SEE_OTHER

    # 6. Verificar que não tem mais acesso
    response = client.get("/tarefas", follow_redirects=False)
    assert response.status_code == status.HTTP_303_SEE_OTHER
```

## Exemplo 15: Debug de Teste Falhando

```bash
# Executar com print de variáveis
pytest tests/test_auth.py::test_login_com_credenciais_validas -v -s

# Executar com pdb (debugger Python)
pytest tests/test_auth.py::test_login_com_credenciais_validas --pdb

# Executar e parar no primeiro erro com pdb
pytest -x --pdb
```

## Exemplo 16: Gerar Relatório JUnit (para CI/CD)

```bash
# Gerar relatório XML para Jenkins, GitLab CI, etc.
pytest --junitxml=test-results.xml

# Com cobertura e relatório
pytest --cov=. --cov-report=xml --junitxml=test-results.xml
```

## Exemplo 17: Ver Quais Fixtures Estão Disponíveis

```bash
# Listar todas as fixtures
pytest --fixtures

# Listar fixtures do conftest
pytest --fixtures tests/conftest.py

# Buscar fixture específica
pytest --fixtures | grep "autenticado"
```

## Exemplo 18: Executar Apenas Testes que Falharam

```bash
# Primeira execução (alguns testes falham)
pytest

# Executar apenas os que falharam
pytest --lf

# Executar primeiro os que falharam, depois os outros
pytest --ff
```

## Dicas Importantes

### 1. Sempre execute da raiz do projeto
```bash
cd /mnt/c/Projetos/DefaultWebApp
pytest
```

### 2. Use -v para ver detalhes
```bash
pytest -v  # verbose
pytest -vv # muito verbose
```

### 3. Use -s para ver prints
```bash
pytest -s  # mostra print()
```

### 4. Combine opções
```bash
pytest -v -s -x  # verbose + prints + parar no erro
```

### 5. Filtrar por nome
```bash
pytest -k "login"  # testes com "login" no nome
pytest -k "not slow"  # excluir testes lentos
```

## Troubleshooting Comum

### Erro: "No module named 'main'"
**Solução:** Execute do diretório raiz
```bash
cd /mnt/c/Projetos/DefaultWebApp
pytest
```

### Erro: "fixture 'client' not found"
**Solução:** Certifique-se que conftest.py está em tests/
```bash
ls tests/conftest.py  # deve existir
```

### Testes passam individualmente mas falham juntos
**Solução:** Problema de isolamento, verifique fixtures
```bash
# Executar com seed fixo
pytest --randomly-seed=1234
```

### Banco de dados não limpa
**Solução:** Fixture client cria novo banco a cada teste
```python
def test_exemplo(client):  # Não reutilizar client entre testes
    # seu teste
```

## Recursos Adicionais

- Documentação pytest: https://docs.pytest.org/
- TestClient FastAPI: https://fastapi.tiangolo.com/tutorial/testing/
- Fixtures: https://docs.pytest.org/en/stable/fixture.html
- Parametrize: https://docs.pytest.org/en/stable/parametrize.html
