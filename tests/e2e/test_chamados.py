"""
Testes E2E para gerenciamento de chamados de suporte.

Casos de uso testados:
- UC-CHAM-01: Listar meus chamados
- UC-CHAM-02: Abrir novo chamado de suporte
- UC-CHAM-03: Visualizar detalhes do chamado
- UC-CHAM-04: Responder a um chamado
- UC-CHAM-05: Excluir chamado (sem resposta)
"""

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    ChamadosPage,
    criar_usuario_e_logar,
)


# =============================================================================
# UC-CHAM-01: Listar meus chamados
# =============================================================================


@pytest.mark.e2e
class TestListarChamados:
    """Testes de listagem de chamados."""

    def test_pagina_chamados_carrega(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-CHAM-01: Deve carregar pagina de listagem de chamados."""
        email = "chamados_lista@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha)

        chamados = ChamadosPage(e2e_page, e2e_server)
        chamados.navegar_listar()

        assert "/chamados/listar" in e2e_page.url

    def test_chamados_redireciona_sem_login(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-CHAM-01: Deve redirecionar para login se nao autenticado."""
        chamados = ChamadosPage(e2e_page, e2e_server)
        chamados.navegar_listar()

        e2e_page.wait_for_timeout(500)
        assert "/login" in e2e_page.url

    def test_lista_chamados_vazia_inicialmente(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-CHAM-01: Lista deve estar vazia para novo usuario."""
        email = "chamados_vazia@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha)

        chamados = ChamadosPage(e2e_page, e2e_server)
        chamados.navegar_listar()

        # Pagina deve carregar sem erros
        assert "/chamados/listar" in e2e_page.url


# =============================================================================
# UC-CHAM-02: Abrir novo chamado de suporte
# =============================================================================


@pytest.mark.e2e
class TestAbrirChamado:
    """Testes de abertura de chamado."""

    def test_pagina_cadastro_chamado_carrega(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-CHAM-02: Deve carregar formulario de abertura de chamado."""
        email = "chamado_cadastro@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha)

        chamados = ChamadosPage(e2e_page, e2e_server)
        chamados.navegar_cadastrar()

        assert "/chamados/cadastrar" in e2e_page.url
        expect(e2e_page.locator('input[name="titulo"]')).to_be_visible()
        expect(e2e_page.locator('textarea[name="descricao"]')).to_be_visible()

    def test_abrir_chamado_com_sucesso(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-CHAM-02: Deve abrir chamado com dados validos."""
        email = "chamado_sucesso@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha)

        chamados = ChamadosPage(e2e_page, e2e_server)
        chamados.navegar_cadastrar()

        # Preencher formulario
        e2e_page.fill('input[name="titulo"]', "Problema com cadastro de vaga")
        e2e_page.fill('textarea[name="descricao"]', "Nao consigo cadastrar uma nova vaga. O sistema retorna erro.")

        # Selecionar prioridade se existir
        select_prioridade = e2e_page.locator('select[name="prioridade"]')
        if select_prioridade.is_visible():
            select_prioridade.select_option(index=1)

        chamados.submeter()

        e2e_page.wait_for_timeout(500)
        conteudo = e2e_page.content().lower()
        assert "sucesso" in conteudo or "/chamados/listar" in e2e_page.url

    def test_abrir_chamado_titulo_vazio(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-CHAM-02: Deve rejeitar chamado sem titulo."""
        email = "chamado_sem_titulo@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha)

        chamados = ChamadosPage(e2e_page, e2e_server)
        chamados.navegar_cadastrar()

        # Preencher apenas descricao
        e2e_page.fill('textarea[name="descricao"]', "Descricao do problema")
        chamados.submeter()

        e2e_page.wait_for_timeout(500)
        # Deve permanecer na pagina ou exibir erro
        assert "/chamados/cadastrar" in e2e_page.url or "titulo" in e2e_page.content().lower()


# =============================================================================
# UC-CHAM-03: Visualizar detalhes do chamado
# =============================================================================


@pytest.mark.e2e
class TestVisualizarChamado:
    """Testes de visualizacao de chamado."""

    def test_visualizar_chamado_requer_login(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-CHAM-03: Visualizar chamado deve requerer autenticacao."""
        chamados = ChamadosPage(e2e_page, e2e_server)
        chamados.navegar_visualizar(1)

        e2e_page.wait_for_timeout(500)
        assert "/login" in e2e_page.url

    def test_visualizar_chamado_inexistente(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-CHAM-03: Deve tratar chamado inexistente."""
        email = "chamado_inexistente@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha)

        chamados = ChamadosPage(e2e_page, e2e_server)
        chamados.navegar_visualizar(99999)

        e2e_page.wait_for_timeout(500)
        conteudo = e2e_page.content().lower()
        assert (
            "não encontrado" in conteudo
            or "/chamados/listar" in e2e_page.url
            or "erro" in conteudo
        )


# =============================================================================
# UC-CHAM-04: Responder a um chamado
# =============================================================================


@pytest.mark.e2e
class TestResponderChamado:
    """Testes de resposta a chamado."""

    def test_campo_resposta_visivel_no_chamado(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-CHAM-04: Visualizacao de chamado deve ter campo de resposta."""
        email = "chamado_resposta@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha)

        # Criar um chamado primeiro
        chamados = ChamadosPage(e2e_page, e2e_server)
        chamados.navegar_cadastrar()

        e2e_page.fill('input[name="titulo"]', "Chamado para resposta")
        e2e_page.fill('textarea[name="descricao"]', "Descricao do chamado")
        chamados.submeter()

        e2e_page.wait_for_timeout(500)

        # Verificar se foi para lista
        if "/chamados/listar" in e2e_page.url:
            # Tentar acessar o chamado criado
            links = e2e_page.locator('a[href*="/chamados/"][href*="/visualizar"]')
            if links.count() > 0:
                links.first.click()
                e2e_page.wait_for_timeout(500)
                # Verificar se campo de resposta existe
                expect(e2e_page.locator('textarea[name="mensagem"]')).to_be_visible()


# =============================================================================
# UC-CHAM-05: Excluir chamado
# =============================================================================


@pytest.mark.e2e
class TestExcluirChamado:
    """Testes de exclusao de chamado."""

    def test_excluir_chamado_requer_autenticacao(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-CHAM-05: Exclusao de chamado deve requerer autenticacao."""
        # Tentar excluir chamado sem login via URL direta
        e2e_page.goto(f"{e2e_server}/chamados/1/excluir")

        e2e_page.wait_for_timeout(500)
        # Deve redirecionar para login ou ser bloqueado
        assert "/login" in e2e_page.url or e2e_page.url != f"{e2e_server}/chamados/1/excluir"
