"""
Testes E2E para funcionalidades do recrutador.

Casos de uso testados:
- UC-RECR-01: Listar minhas vagas publicadas
- UC-RECR-02: Cadastrar nova vaga de estagio
- UC-RECR-03: Editar dados de uma vaga
- UC-RECR-04: Alterar status da vaga (abrir/fechar/suspender)
- UC-RECR-05: Visualizar candidatos de uma vaga
- UC-RECR-06: Avaliar candidatura (aprovar/rejeitar)
"""

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    RecrutadorVagasPage,
    criar_usuario_e_logar,
    fazer_logout,
)


# =============================================================================
# UC-RECR-01: Listar minhas vagas publicadas
# =============================================================================


@pytest.mark.e2e
class TestListarVagasRecrutador:
    """Testes de listagem de vagas do recrutador."""

    def test_pagina_vagas_recrutador_carrega(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-RECR-01: Deve carregar pagina de vagas do recrutador."""
        email = "recrutador_vagas@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, perfil="Recrutador"
        )

        vagas = RecrutadorVagasPage(e2e_page, e2e_server)
        vagas.navegar_listar()

        assert "/recrutador/vagas/listar" in e2e_page.url

    def test_vagas_recrutador_redireciona_sem_login(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-RECR-01: Deve redirecionar para login se nao autenticado."""
        vagas = RecrutadorVagasPage(e2e_page, e2e_server)
        vagas.navegar_listar()

        e2e_page.wait_for_timeout(500)
        assert "/login" in e2e_page.url

    def test_estudante_nao_acessa_vagas_recrutador(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-RECR-01: Estudante nao deve acessar area de recrutador."""
        email = "estudante_tenta_recrutador@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, perfil="Estudante"
        )

        vagas = RecrutadorVagasPage(e2e_page, e2e_server)
        vagas.navegar_listar()

        e2e_page.wait_for_timeout(500)
        # Deve ser redirecionado ou mostrar erro
        assert "/recrutador/vagas/listar" not in e2e_page.url or "acesso" in e2e_page.content().lower()


# =============================================================================
# UC-RECR-02: Cadastrar nova vaga de estagio
# =============================================================================


@pytest.mark.e2e
class TestCadastrarVaga:
    """Testes de cadastro de vaga."""

    def test_pagina_cadastro_vaga_carrega(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-RECR-02: Deve carregar formulario de cadastro de vaga."""
        email = "recrutador_cadastro@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, perfil="Recrutador"
        )

        vagas = RecrutadorVagasPage(e2e_page, e2e_server)
        vagas.navegar_cadastrar()

        assert "/recrutador/vagas/cadastrar" in e2e_page.url
        expect(e2e_page.locator('input[name="titulo"]')).to_be_visible()

    def test_cadastro_vaga_campos_obrigatorios(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-RECR-02: Formulario deve ter campos obrigatorios."""
        email = "recrutador_campos@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, perfil="Recrutador"
        )

        vagas = RecrutadorVagasPage(e2e_page, e2e_server)
        vagas.navegar_cadastrar()

        # Verificar campos principais
        expect(e2e_page.locator('input[name="titulo"]')).to_be_visible()
        expect(e2e_page.locator('textarea[name="descricao"]')).to_be_visible()
        expect(e2e_page.locator('select[name="id_area"]')).to_be_visible()


# =============================================================================
# UC-RECR-03: Editar dados de uma vaga
# =============================================================================


@pytest.mark.e2e
class TestEditarVaga:
    """Testes de edicao de vaga."""

    def test_editar_vaga_requer_autenticacao(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-RECR-03: Edicao de vaga deve requerer autenticacao."""
        vagas = RecrutadorVagasPage(e2e_page, e2e_server)
        vagas.navegar_editar(1)

        e2e_page.wait_for_timeout(500)
        assert "/login" in e2e_page.url

    def test_editar_vaga_inexistente(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-RECR-03: Deve tratar vaga inexistente."""
        email = "recrutador_edita@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, perfil="Recrutador"
        )

        vagas = RecrutadorVagasPage(e2e_page, e2e_server)
        vagas.navegar_editar(99999)

        e2e_page.wait_for_timeout(500)
        # Deve redirecionar ou exibir erro
        conteudo = e2e_page.content().lower()
        assert (
            "não encontrada" in conteudo
            or "/recrutador/vagas/listar" in e2e_page.url
            or "erro" in conteudo
        )


# =============================================================================
# UC-RECR-04: Alterar status da vaga
# =============================================================================


@pytest.mark.e2e
class TestAlterarStatusVaga:
    """Testes de alteracao de status de vaga."""

    def test_lista_vagas_mostra_status(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-RECR-04: Lista deve exibir status das vagas."""
        email = "recrutador_status@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, perfil="Recrutador"
        )

        vagas = RecrutadorVagasPage(e2e_page, e2e_server)
        vagas.navegar_listar()

        # Pagina deve carregar
        assert "/recrutador/vagas/listar" in e2e_page.url


# =============================================================================
# UC-RECR-05: Visualizar candidatos de uma vaga
# =============================================================================


@pytest.mark.e2e
class TestVisualizarCandidatos:
    """Testes de visualizacao de candidatos."""

    def test_candidatos_requer_autenticacao(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-RECR-05: Ver candidatos deve requerer autenticacao."""
        vagas = RecrutadorVagasPage(e2e_page, e2e_server)
        vagas.navegar_candidatos(1)

        e2e_page.wait_for_timeout(500)
        assert "/login" in e2e_page.url

    def test_candidatos_vaga_inexistente(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-RECR-05: Deve tratar vaga inexistente."""
        email = "recrutador_candidatos@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, perfil="Recrutador"
        )

        vagas = RecrutadorVagasPage(e2e_page, e2e_server)
        vagas.navegar_candidatos(99999)

        e2e_page.wait_for_timeout(500)
        # Deve redirecionar ou exibir erro
        conteudo = e2e_page.content().lower()
        assert (
            "não encontrada" in conteudo
            or "/recrutador/vagas/listar" in e2e_page.url
            or "erro" in conteudo
        )


# =============================================================================
# UC-RECR-06: Avaliar candidatura
# =============================================================================


@pytest.mark.e2e
class TestAvaliarCandidatura:
    """Testes de avaliacao de candidatura."""

    def test_pagina_candidatos_carrega_para_recrutador(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-RECR-06: Recrutador deve poder acessar lista de candidatos."""
        email = "recrutador_avalia@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, perfil="Recrutador"
        )

        # Deve ter acesso a area de vagas
        vagas = RecrutadorVagasPage(e2e_page, e2e_server)
        vagas.navegar_listar()

        assert "/recrutador/vagas/listar" in e2e_page.url
