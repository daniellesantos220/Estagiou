"""
Configurações e fixtures para testes pytest.

Fornece fixtures reutilizáveis e helpers para testes da aplicação.
"""
# ============================================================
# CRÍTICO: Configurar banco de dados ANTES de qualquer import
# que possa carregar db_util.py (via repos ou outros módulos)
# ============================================================
import os
import tempfile

# Criar arquivo temporário para o banco de testes
_test_db = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db')
_TEST_DB_PATH = _test_db.name
_test_db.close()

# Configurar variáveis de ambiente ANTES de importar qualquer módulo da aplicação
os.environ['DATABASE_PATH'] = _TEST_DB_PATH
os.environ['RESEND_API_KEY'] = ''
os.environ['LOG_LEVEL'] = 'ERROR'

# ============================================================
# Agora sim, importar o resto (db_util já lerá o valor correto)
# ============================================================
import asyncio
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from fastapi import status
from typing import Optional
from util.perfis import Perfil


@pytest.fixture(scope="session")
def event_loop():
    """
    Cria um event loop de escopo de sessão para testes async.

    Isso evita conflitos entre o event loop do TestClient e os testes
    marcados com @pytest.mark.asyncio quando executados em sequência.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Garante que o banco de teste está configurado e limpa ao final.

    O banco já foi configurado no nível de módulo (acima), esta fixture
    cria as tabelas necessárias e gerencia o cleanup ao final da sessão.
    """
    # Criar todas as tabelas necessárias para os testes
    from repo import (
        usuario_repo, configuracao_repo, chamado_repo,
        area_repo, empresa_repo, vaga_repo, candidatura_repo,
        endereco_repo, avaliacao_repo, curtida_repo
    )

    # Tabelas do upstream
    usuario_repo.criar_tabela()
    configuracao_repo.criar_tabela()
    chamado_repo.criar_tabela()

    # Tabelas específicas do projeto Estagiou
    area_repo.criar_tabela()
    empresa_repo.criar_tabela()
    vaga_repo.criar_tabela()
    candidatura_repo.criar_tabela()
    endereco_repo.criar_tabela()
    avaliacao_repo.criar_tabela()
    curtida_repo.criar_tabela()

    yield _TEST_DB_PATH

    # Limpar: remover arquivo de banco após todos os testes
    try:
        os.unlink(_TEST_DB_PATH)
    except Exception:
        pass


@pytest.fixture(scope="function", autouse=True)
def limpar_rate_limiter():
    """Limpa o rate limiter antes de cada teste para evitar bloqueios"""
    # Importar após configuração do banco de dados
    from routes.auth_routes import login_limiter, cadastro_limiter, esqueci_senha_limiter
    from routes.admin_usuarios_routes import admin_usuarios_limiter
    from routes.admin_backups_routes import admin_backups_limiter, backup_download_limiter
    from routes.admin_configuracoes_routes import admin_config_limiter
    from routes.chamados_routes import chamado_criar_limiter, chamado_responder_limiter
    from routes.admin_chamados_routes import admin_chamado_responder_limiter
    from routes.usuario_routes import (
        upload_foto_limiter, alterar_senha_limiter, form_get_limiter
    )
    from routes.chat_routes import (
        chat_mensagem_limiter, chat_sala_limiter,
        busca_usuarios_limiter, chat_listagem_limiter
    )
    from routes.public_routes import public_limiter
    from routes.examples_routes import examples_limiter

    # Lista de todos os limiters
    limiters = [
        login_limiter,
        cadastro_limiter,
        esqueci_senha_limiter,
        admin_usuarios_limiter,
        admin_backups_limiter,
        backup_download_limiter,
        admin_config_limiter,
        chamado_criar_limiter,
        chamado_responder_limiter,
        admin_chamado_responder_limiter,
        upload_foto_limiter,
        alterar_senha_limiter,
        form_get_limiter,
        chat_mensagem_limiter,
        chat_sala_limiter,
        busca_usuarios_limiter,
        chat_listagem_limiter,
        public_limiter,
        examples_limiter,
    ]

    # Limpar antes do teste
    for limiter in limiters:
        limiter.limpar()

    yield

    # Limpar depois do teste também
    for limiter in limiters:
        limiter.limpar()


@pytest.fixture(scope="function", autouse=True)
def limpar_config_cache():
    """Limpa o cache de configurações antes de cada teste para evitar interferência"""
    from util.config_cache import config

    # Limpar antes do teste
    config.limpar()

    yield

    # Limpar depois do teste também
    config.limpar()


@pytest.fixture(scope="function", autouse=True)
def limpar_chat_manager():
    """Limpa o gerenciador de chat antes de cada teste para evitar interferência"""
    from util.chat_manager import gerenciador_chat

    # Limpar antes do teste
    gerenciador_chat._connections.clear()
    gerenciador_chat._active_connections.clear()

    yield

    # Limpar depois do teste também
    gerenciador_chat._connections.clear()
    gerenciador_chat._active_connections.clear()


@pytest.fixture(scope="function", autouse=True)
def limpar_banco_dados(setup_test_database):
    """Limpa todas as tabelas do banco antes de cada teste para evitar interferência"""
    # Importar após configuração do banco de dados
    from util.db_util import obter_conexao

    def _limpar_tabelas():
        """Limpa tabelas se elas existirem e reseta autoincrement"""
        with obter_conexao() as conn:
            cursor = conn.cursor()

            # Lista de todas as tabelas do projeto (ordem de exclusão respeitando FKs)
            # Tabelas filhas primeiro, depois tabelas pai
            todas_tabelas = [
                # Tabelas de chat
                'chat_mensagem',
                'chat_participante',
                'chat_sala',
                # Tabelas específicas do projeto Estagiou
                'avaliacao',
                'curtida',
                'candidatura',
                'vaga',
                'endereco',
                'empresa',
                'area',
                # Tabelas do upstream
                'chamado_interacao',
                'chamado',
                'usuario',
                'configuracao'
            ]

            # Verificar quais tabelas existem
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
            tabelas_existentes = [row[0] for row in cursor.fetchall()]

            # Desabilitar temporariamente as foreign keys para facilitar a limpeza
            cursor.execute("PRAGMA foreign_keys = OFF")

            # Limpar apenas tabelas que existem (na ordem correta para respeitar FKs)
            for tabela in todas_tabelas:
                if tabela in tabelas_existentes:
                    try:
                        cursor.execute(f"DELETE FROM {tabela}")
                    except Exception:
                        pass  # Ignora erros se a tabela não existe mais

            # Resetar autoincrement (limpar sqlite_sequence se existir)
            try:
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'"
                )
                if cursor.fetchone():
                    cursor.execute("DELETE FROM sqlite_sequence")
            except Exception:
                pass

            # Reabilitar foreign keys
            cursor.execute("PRAGMA foreign_keys = ON")

            conn.commit()

    # Limpar antes do teste
    _limpar_tabelas()

    yield

    # Limpar depois do teste também
    _limpar_tabelas()


@pytest.fixture(scope="function")
def client():
    """
    Cliente de teste FastAPI com sessão limpa para cada teste
    Importa app DEPOIS de configurar o banco de dados
    """
    # Importar aqui para garantir que as configurações de teste sejam aplicadas
    from main import app

    # Criar cliente de teste
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def usuario_teste():
    """Dados de um usuário de teste padrão"""
    return {
        "nome": "Usuario Teste",
        "email": "teste@example.com",
        "senha": "Senha@123",
        "perfil": Perfil.CLIENTE.value  # Usa Enum Perfil
    }


@pytest.fixture
def admin_teste():
    """Dados de um admin de teste"""
    return {
        "nome": "Admin Teste",
        "email": "admin@example.com",
        "senha": "Admin@123",
        "perfil": Perfil.ADMIN.value  # Usa Enum Perfil
    }


@pytest.fixture
def criar_usuario(client):
    """
    Fixture que retorna uma função para criar usuários
    Útil para criar múltiplos usuários em um teste
    """
    def _criar_usuario(nome: str, email: str, senha: str, perfil: str = Perfil.CLIENTE.value):
        """Cadastra um usuário via endpoint de cadastro"""
        response = client.post("/cadastrar", data={
            "perfil": perfil,
            "nome": nome,
            "email": email,
            "senha": senha,
            "confirmar_senha": senha
        }, follow_redirects=False)
        return response

    return _criar_usuario


@pytest.fixture
def fazer_login(client):
    """
    Fixture que retorna uma função para fazer login
    Retorna o cliente já autenticado
    """
    def _fazer_login(email: str, senha: str):
        """Faz login e retorna o cliente autenticado"""
        response = client.post("/login", data={
            "email": email,
            "senha": senha
        }, follow_redirects=False)
        return response

    return _fazer_login


@pytest.fixture
def cliente_autenticado(client, criar_usuario, fazer_login, usuario_teste):
    """
    Fixture que retorna um cliente já autenticado
    Cria um usuário e faz login automaticamente
    """
    # Criar usuário
    criar_usuario(
        usuario_teste["nome"],
        usuario_teste["email"],
        usuario_teste["senha"]
    )

    # Fazer login
    fazer_login(usuario_teste["email"], usuario_teste["senha"])

    # Retornar cliente autenticado
    return client


@pytest.fixture
def admin_autenticado(client, criar_usuario, fazer_login, admin_teste):
    """
    Fixture que retorna um cliente autenticado como admin
    """
    # Importar para manipular diretamente o banco
    from repo import usuario_repo
    from model.usuario_model import Usuario
    from util.security import criar_hash_senha

    # Criar admin diretamente no banco (pular validações de cadastro público)
    admin = Usuario(
        id=0,
        nome=admin_teste["nome"],
        email=admin_teste["email"],
        senha=criar_hash_senha(admin_teste["senha"]),
        perfil=Perfil.ADMIN.value  # Usa Enum Perfil
    )
    usuario_repo.inserir(admin)

    # Fazer login
    fazer_login(admin_teste["email"], admin_teste["senha"])

    # Retornar cliente autenticado
    return client


@pytest.fixture
def vendedor_teste():
    """Dados de um vendedor de teste"""
    return {
        "nome": "Vendedor Teste",
        "email": "vendedor@example.com",
        "senha": "Vendedor@123",
        "perfil": Perfil.VENDEDOR.value
    }


@pytest.fixture
def recrutador_teste():
    """Dados de um recrutador de teste"""
    return {
        "nome": "Recrutador Teste",
        "email": "recrutador@example.com",
        "senha": "Recrutador@123",
        "perfil": Perfil.RECRUTADOR.value
    }


@pytest.fixture
def vendedor_autenticado(client, criar_usuario, fazer_login, vendedor_teste):
    """
    Fixture que retorna um cliente autenticado como vendedor
    """
    # Importar para manipular diretamente o banco
    from repo import usuario_repo
    from model.usuario_model import Usuario
    from util.security import criar_hash_senha

    # Criar vendedor diretamente no banco
    vendedor = Usuario(
        id=0,
        nome=vendedor_teste["nome"],
        email=vendedor_teste["email"],
        senha=criar_hash_senha(vendedor_teste["senha"]),
        perfil=Perfil.VENDEDOR.value
    )
    usuario_repo.inserir(vendedor)

    # Fazer login
    fazer_login(vendedor_teste["email"], vendedor_teste["senha"])

    # Retornar cliente autenticado
    return client


@pytest.fixture
def recrutador_autenticado(client, criar_usuario, fazer_login, recrutador_teste):
    """
    Fixture que retorna um cliente autenticado como recrutador
    """
    # Importar para manipular diretamente o banco
    from repo import usuario_repo
    from model.usuario_model import Usuario
    from util.security import criar_hash_senha

    # Criar recrutador diretamente no banco
    recrutador = Usuario(
        id=0,
        nome=recrutador_teste["nome"],
        email=recrutador_teste["email"],
        senha=criar_hash_senha(recrutador_teste["senha"]),
        perfil=Perfil.RECRUTADOR.value
    )
    usuario_repo.inserir(recrutador)

    # Fazer login
    fazer_login(recrutador_teste["email"], recrutador_teste["senha"])

    # Retornar cliente autenticado
    return client


@pytest.fixture
def foto_teste_base64():
    """
    Retorna uma imagem 1x1 pixel PNG válida em base64
    Útil para testes de upload de foto
    """
    # PNG 1x1 pixel transparente em base64
    return (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
        "AAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )


@pytest.fixture
def criar_backup():
    """
    Fixture que retorna uma função para criar backup de teste
    """
    def _criar_backup():
        """Cria um backup via util/backup_util"""
        from util import backup_util
        sucesso, mensagem = backup_util.criar_backup()
        return sucesso, mensagem

    return _criar_backup


# ===== FIXTURES AVANÇADAS =====

@pytest.fixture
def dois_usuarios(client, criar_usuario):
    """
    Fixture que cria dois usuários de teste.

    Útil para testes que verificam isolamento de dados entre usuários.

    Returns:
        Tuple com dados dos dois usuários (dict, dict)
    """
    usuario1 = {
        "nome": "Usuario Um",
        "email": "usuario1@example.com",
        "senha": "Senha@123",
        "perfil": Perfil.CLIENTE.value
    }
    usuario2 = {
        "nome": "Usuario Dois",
        "email": "usuario2@example.com",
        "senha": "Senha@456",
        "perfil": Perfil.CLIENTE.value
    }

    # Criar ambos usuários
    criar_usuario(usuario1["nome"], usuario1["email"], usuario1["senha"])
    criar_usuario(usuario2["nome"], usuario2["email"], usuario2["senha"])

    return usuario1, usuario2


@pytest.fixture
def usuario_com_foto(cliente_autenticado, foto_teste_base64):
    """
    Fixture que retorna um cliente autenticado com foto de perfil.

    Returns:
        TestClient autenticado com foto já salva
    """
    # Atualizar foto do perfil
    response = cliente_autenticado.post(
        "/perfil/foto/atualizar",
        json={"imagem": foto_teste_base64},
        follow_redirects=False
    )

    # Verificar se foto foi salva com sucesso
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_303_SEE_OTHER]

    return cliente_autenticado


@pytest.fixture
def obter_ultimo_backup():
    """
    Fixture que retorna função para obter último backup criado.

    Returns:
        Função que retorna dict com dados do último backup ou None
    """
    def _obter_ultimo_backup() -> Optional[dict]:
        """Obtém informações do último backup na pasta backups/"""
        from util import backup_util

        backups = backup_util.listar_backups()
        if not backups:
            return None

        # Retornar o mais recente (primeiro da lista)
        return backups[0]

    return _obter_ultimo_backup


@pytest.fixture
def criar_usuario_direto():
    """
    Fixture que retorna função para criar usuário diretamente no banco.

    Útil para testes que precisam criar usuários sem passar pelo endpoint
    de cadastro (ex: testes de chat, admin, etc).

    Returns:
        Função que cria usuário e retorna o ID
    """
    from repo import usuario_repo
    from model.usuario_model import Usuario
    from util.security import criar_hash_senha

    def _criar_usuario_direto(
        nome: str,
        email: str,
        senha: str,
        perfil: str = Perfil.CLIENTE.value
    ) -> int:
        """
        Cria usuário diretamente no banco.

        Args:
            nome: Nome do usuário
            email: Email do usuário
            senha: Senha (será hasheada)
            perfil: Perfil do usuário (padrão: Cliente)

        Returns:
            ID do usuário criado
        """
        usuario = Usuario(
            id=0,
            nome=nome,
            email=email,
            senha=criar_hash_senha(senha),
            perfil=perfil
        )
        return usuario_repo.inserir(usuario)

    return _criar_usuario_direto


@pytest.fixture
def bloquear_rate_limiter():
    """
    Fixture que retorna função para mockar rate limiter como bloqueado.

    Útil para testes de rate limiting onde se quer simular
    que o limite foi excedido.

    Returns:
        Context manager que mocka o limiter especificado
    """
    from unittest.mock import patch

    def _bloquear_limiter(limiter_path: str):
        """
        Retorna context manager que bloqueia o limiter.

        Args:
            limiter_path: Caminho do limiter (ex: 'routes.auth_routes.login_limiter')

        Returns:
            Context manager do patch
        """
        return patch(f'{limiter_path}.verificar', return_value=False)

    return _bloquear_limiter
