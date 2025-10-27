# Testes - DefaultWebApp

Estrutura de testes automatizados usando pytest e TestClient do FastAPI.

## Estrutura

```
tests/
├── conftest.py          # Fixtures e configurações pytest
├── test_auth.py         # Testes de autenticação e autorização
├── test_tarefas.py      # Testes do CRUD de tarefas
└── README.md           # Este arquivo
```

## Instalação de Dependências

```bash
pip install pytest pytest-asyncio httpx
```

Ou adicione ao `requirements.txt`:
```
pytest==7.4.0
pytest-asyncio==0.21.0
httpx==0.24.1
```

## Executar Testes

### Todos os testes
```bash
pytest
```

### Testes específicos
```bash
# Apenas testes de autenticação
pytest tests/test_auth.py

# Apenas testes de tarefas
pytest tests/test_tarefas.py

# Teste específico
pytest tests/test_auth.py::TestLogin::test_login_com_credenciais_validas
```

### Com verbosidade
```bash
pytest -v              # Verbose
pytest -vv             # Mais verbose
pytest -s              # Mostra prints
pytest -v -s           # Combinado
```

### Parar no primeiro erro
```bash
pytest -x
```

### Executar testes por markers
```bash
pytest -m auth         # Apenas testes de autenticação
pytest -m crud         # Apenas testes CRUD
pytest -m "not slow"   # Pular testes lentos
```

### Com coverage (se instalado)
```bash
pytest --cov=. --cov-report=html
pytest --cov=. --cov-report=term-missing
```

## Estrutura dos Testes

### conftest.py
Contém fixtures reutilizáveis:

- `client`: Cliente de teste FastAPI
- `usuario_teste`: Dados de usuário padrão
- `admin_teste`: Dados de admin padrão
- `criar_usuario`: Função para criar usuários
- `fazer_login`: Função para fazer login
- `cliente_autenticado`: Cliente já autenticado como usuário
- `admin_autenticado`: Cliente já autenticado como admin
- `tarefa_teste`: Dados de tarefa padrão
- `criar_tarefa`: Função para criar tarefas

### test_auth.py
Testes de autenticação:

**TestLogin**
- Login com credenciais válidas/inválidas
- Validação de campos
- Rate limiting
- Redirecionamentos

**TestCadastro**
- Cadastro com dados válidos
- Validação de e-mail duplicado
- Validação de senha forte
- Confirmação de senha
- Criação com perfil correto

**TestLogout**
- Limpeza de sessão
- Desautenticação

**TestRecuperacaoSenha**
- Solicitação de recuperação
- Validação de token
- Redefinição de senha

**TestAutorizacao**
- Proteção de rotas
- Controle de acesso por perfil
- Áreas administrativas

**TestRateLimiting**
- Bloqueio por múltiplas tentativas

### test_tarefas.py
Testes do CRUD de tarefas:

**TestListarTarefas**
- Listagem requer autenticação
- Lista inicial vazia

**TestCriarTarefa**
- Criação com dados válidos
- Validações de título
- Descrição opcional
- Tarefa aparece na listagem
- Tarefa pertence ao usuário

**TestConcluirTarefa**
- Conclusão de tarefa própria
- Bloqueio sem autenticação
- Tratamento de tarefa inexistente

**TestExcluirTarefa**
- Confirmação de exclusão
- Exclusão de tarefa própria
- Proteções de acesso

**TestIsolamentoTarefas**
- Isolamento entre usuários
- Um usuário não vê/edita/exclui tarefas de outro

**TestValidacoesTarefa**
- Múltiplas tarefas
- Estado inicial não concluída
- Data de criação

## Banco de Dados de Teste

Os testes usam banco de dados temporário separado:
- Criado automaticamente antes dos testes
- Isolado do banco de produção
- Removido após todos os testes
- Cada teste tem sessão limpa

## Boas Práticas

1. **Isolamento**: Cada teste deve ser independente
2. **Fixtures**: Reutilize fixtures do conftest.py
3. **Nomenclatura**: Nomes descritivos (`test_verbo_cenario`)
4. **Assertions**: Use assertions claras e específicas
5. **Arrange-Act-Assert**: Organize testes neste padrão
6. **Cleanup**: Confie nas fixtures para limpeza automática

## Exemplo de Teste

```python
def test_criar_tarefa_com_dados_validos(cliente_autenticado, tarefa_teste):
    """Deve criar tarefa com dados válidos"""
    # Arrange (preparar) - já feito pelas fixtures

    # Act (agir)
    response = cliente_autenticado.post("/tarefas/cadastrar", data={
        "titulo": tarefa_teste["titulo"],
        "descricao": tarefa_teste["descricao"]
    })

    # Assert (verificar)
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/tarefas"
```

## Adicionar Novos Testes

1. Crie arquivo `test_nome.py` em `/tests/`
2. Importe pytest e fixtures necessárias
3. Organize em classes por funcionalidade
4. Use fixtures do conftest.py
5. Siga padrão de nomenclatura
6. Execute e verifique

## Troubleshooting

### Erro: "No module named 'main'"
- Certifique-se de estar no diretório raiz
- `pytest.ini` deve estar no diretório raiz

### Testes falhando com erro de sessão
- Verifique se está usando as fixtures corretas
- `cliente_autenticado` já tem sessão ativa

### Banco de dados não limpa entre testes
- Fixture `client` cria novo cliente a cada teste
- Banco temporário é recriado a cada sessão

## Métricas de Cobertura

Para gerar relatório de cobertura:

```bash
pip install pytest-cov
pytest --cov=. --cov-report=html --cov-report=term-missing
```

Abra `htmlcov/index.html` no navegador.

## CI/CD

Exemplo para GitHub Actions:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest -v
```

## Contato

Para dúvidas sobre os testes, consulte a documentação do projeto ou PLAN.md.
