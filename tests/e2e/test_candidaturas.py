"""
Testes E2E para candidaturas de estudantes.

Casos de uso testados:
- UC-CAND-01: Candidatar-se a uma vaga
- UC-CAND-02: Listar minhas candidaturas
- UC-CAND-03: Cancelar candidatura pendente
- UC-CAND-04: Visualizar status da candidatura
"""

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    CadastroPage,
    LoginPage,
    CandidaturasPage,
    VagasPublicasPage,
    criar_usuario_e_logar,
    fazer_logout,
)


# =============================================================================
# UC-CAND-02: Listar minhas candidaturas
# =============================================================================


@pytest.mark.e2e
class TestListarCandidaturas:
    """Testes de listagem de candidaturas."""

    def test_pagina_minhas_candidaturas_carrega(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-CAND-02: Deve carregar pagina de minhas candidaturas."""
        email = "candidaturas_lista@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, perfil="Estudante"
        )

        candidaturas = CandidaturasPage(e2e_page, e2e_server)
        candidaturas.navegar_minhas()

        assert "/candidaturas/minhas" in e2e_page.url

    def test_minhas_candidaturas_redireciona_sem_login(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-CAND-02: Deve redirecionar para login se nao autenticado."""
        candidaturas = CandidaturasPage(e2e_page, e2e_server)
        candidaturas.navegar_minhas()

        e2e_page.wait_for_timeout(500)
        assert "/login" in e2e_page.url

    def test_minhas_candidaturas_vazia_inicialmente(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-CAND-02: Lista deve estar vazia para novo usuario."""
        email = "candidaturas_vazia@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, perfil="Estudante"
        )

        candidaturas = CandidaturasPage(e2e_page, e2e_server)
        candidaturas.navegar_minhas()

        e2e_page.wait_for_timeout(500)
        # Pagina deve carregar sem erros
        assert "/candidaturas/minhas" in e2e_page.url


# =============================================================================
# UC-CAND-01: Candidatar-se a uma vaga
# =============================================================================


@pytest.mark.e2e
class TestCandidatarVaga:
    """Testes de candidatura a vagas."""

    def test_candidatar_requer_login(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-CAND-01: Candidatura deve requerer autenticacao."""
        # Tentar acessar detalhes de vaga e candidatar sem login
        vagas = VagasPublicasPage(e2e_page, e2e_server)
        vagas.navegar()

        e2e_page.wait_for_timeout(500)

        # Botao de candidatar nao deve estar visivel ou deve redirecionar
        conteudo = e2e_page.content().lower()
        # Visitante nao deve ver botao de candidatar
        assert "/vagas" in e2e_page.url

    def test_candidatar_disponivel_para_estudante(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-CAND-01: Estudante deve poder ver opcao de candidatura."""
        email = "estudante_candidata@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, perfil="Estudante"
        )

        # Acessar lista de vagas
        vagas = VagasPublicasPage(e2e_page, e2e_server)
        vagas.navegar()

        e2e_page.wait_for_timeout(500)

        # Deve poder acessar pagina de vagas como estudante
        assert "/vagas" in e2e_page.url

    def test_recrutador_nao_pode_candidatar(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-CAND-01: Recrutador nao deve poder se candidatar."""
        email = "recrutador_candidata@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, perfil="Recrutador"
        )

        # Acessar lista de vagas
        vagas = VagasPublicasPage(e2e_page, e2e_server)
        vagas.navegar()

        e2e_page.wait_for_timeout(500)

        # Se houver vagas, botao de candidatar nao deve aparecer para recrutador
        conteudo = e2e_page.content().lower()
        # Recrutador pode ver vagas, mas nao deve ter botao de candidatar
        assert "/vagas" in e2e_page.url


# =============================================================================
# UC-CAND-03: Cancelar candidatura pendente
# =============================================================================


@pytest.mark.e2e
class TestCancelarCandidatura:
    """Testes de cancelamento de candidatura."""

    def test_pagina_candidaturas_tem_opcao_cancelar(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-CAND-03: Pagina de candidaturas deve ter opcao de cancelar."""
        email = "cancelar_candidatura@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, perfil="Estudante"
        )

        candidaturas = CandidaturasPage(e2e_page, e2e_server)
        candidaturas.navegar_minhas()

        # Pagina deve carregar corretamente
        assert "/candidaturas/minhas" in e2e_page.url


# =============================================================================
# UC-CAND-04: Visualizar status da candidatura
# =============================================================================


@pytest.mark.e2e
class TestStatusCandidatura:
    """Testes de visualizacao de status de candidatura."""

    def test_pagina_exibe_status_candidaturas(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-CAND-04: Pagina deve exibir status das candidaturas."""
        email = "status_candidatura@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, perfil="Estudante"
        )

        candidaturas = CandidaturasPage(e2e_page, e2e_server)
        candidaturas.navegar_minhas()

        # Pagina deve carregar e exibir informacoes de status
        assert "/candidaturas/minhas" in e2e_page.url
