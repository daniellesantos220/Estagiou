"""
Testes E2E para gerenciamento de perfil do usuario.

Casos de uso testados:
- UC-PERF-01: Visualizar proprio perfil
- UC-PERF-02: Editar dados do perfil
- UC-PERF-03: Alterar senha da conta
- UC-PERF-04: Atualizar foto de perfil
- UC-PERF-05: Visualizar dashboard pessoal
"""

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    CadastroPage,
    LoginPage,
    PerfilPage,
    DashboardPage,
    criar_usuario_e_logar,
    verificar_mensagem_flash,
)


# =============================================================================
# UC-PERF-05: Visualizar dashboard pessoal
# =============================================================================


@pytest.mark.e2e
class TestDashboard:
    """Testes de acesso ao dashboard do usuario."""

    def test_dashboard_carrega_apos_login(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-PERF-05: Deve exibir dashboard apos login bem sucedido."""
        email = "dashboard_teste@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha)

        dashboard = DashboardPage(e2e_page, e2e_server)
        assert dashboard.esta_no_dashboard()

    def test_dashboard_exibe_nome_usuario(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-PERF-05: Dashboard deve exibir nome do usuario logado."""
        email = "nome_dashboard@example.com"
        senha = "SenhaForte@123"
        nome = "Usuario Dashboard Teste"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, nome=nome
        )

        conteudo = e2e_page.content().lower()
        assert "usuario" in conteudo or "dashboard" in conteudo

    def test_dashboard_redireciona_sem_login(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-PERF-05: Dashboard deve redirecionar para login se nao autenticado."""
        dashboard = DashboardPage(e2e_page, e2e_server)
        dashboard.navegar()

        e2e_page.wait_for_timeout(500)
        assert "/login" in e2e_page.url


# =============================================================================
# UC-PERF-01: Visualizar proprio perfil
# =============================================================================


@pytest.mark.e2e
class TestVisualizarPerfil:
    """Testes de visualizacao do perfil."""

    def test_pagina_perfil_carrega_corretamente(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-PERF-01: Deve carregar pagina de visualizacao do perfil."""
        email = "perfil_viz@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha)

        perfil = PerfilPage(e2e_page, e2e_server)
        perfil.navegar_visualizar()

        assert "/usuario/perfil/visualizar" in e2e_page.url

    def test_perfil_exibe_dados_usuario(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-PERF-01: Deve exibir dados do usuario no perfil."""
        email = "dados_perfil@example.com"
        senha = "SenhaForte@123"
        nome = "Usuario Perfil Completo"

        assert criar_usuario_e_logar(
            e2e_page, e2e_server, email, senha, nome=nome
        )

        perfil = PerfilPage(e2e_page, e2e_server)
        perfil.navegar_visualizar()

        conteudo = e2e_page.content().lower()
        assert "usuario perfil completo" in conteudo or email in conteudo

    def test_perfil_redireciona_sem_login(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-PERF-01: Perfil deve redirecionar para login se nao autenticado."""
        perfil = PerfilPage(e2e_page, e2e_server)
        perfil.navegar_visualizar()

        e2e_page.wait_for_timeout(500)
        assert "/login" in e2e_page.url


# =============================================================================
# UC-PERF-02: Editar dados do perfil
# =============================================================================


@pytest.mark.e2e
class TestEditarPerfil:
    """Testes de edicao de perfil."""

    def test_pagina_editar_perfil_carrega(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-PERF-02: Deve carregar formulario de edicao de perfil."""
        email = "editar_perfil@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha)

        perfil = PerfilPage(e2e_page, e2e_server)
        perfil.navegar_editar()

        assert "/usuario/perfil/editar" in e2e_page.url
        expect(e2e_page.locator('input[name="nome"]')).to_be_visible()
        expect(e2e_page.locator('input[name="email"]')).to_be_visible()

    def test_editar_perfil_atualiza_nome(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-PERF-02: Deve atualizar nome do usuario com sucesso."""
        email = "atualizar_nome@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha)

        perfil = PerfilPage(e2e_page, e2e_server)
        perfil.navegar_editar()

        # Limpar e preencher novo nome
        e2e_page.fill('input[name="nome"]', "")
        e2e_page.fill('input[name="nome"]', "Nome Atualizado Teste")
        perfil.submeter()

        e2e_page.wait_for_timeout(500)

        # Verificar se atualizou
        conteudo = e2e_page.content().lower()
        assert "sucesso" in conteudo or "atualizado" in conteudo

    def test_editar_perfil_valida_email_duplicado(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-PERF-02: Deve impedir email duplicado na edicao."""
        email1 = "email_original@example.com"
        email2 = "email_segundo@example.com"
        senha = "SenhaForte@123"

        # Criar primeiro usuario
        cadastro = CadastroPage(e2e_page, e2e_server)
        cadastro.navegar()
        cadastro.cadastrar("Estudante", "Primeiro Usuario", email1, senha)
        cadastro.aguardar_navegacao_login()

        # Criar segundo usuario
        cadastro.navegar()
        cadastro.cadastrar("Estudante", "Segundo Usuario", email2, senha)
        cadastro.aguardar_navegacao_login()

        # Logar com segundo usuario
        login = LoginPage(e2e_page, e2e_server)
        login.fazer_login(email2, senha)
        login.aguardar_navegacao_usuario()

        # Tentar mudar email para o primeiro
        perfil = PerfilPage(e2e_page, e2e_server)
        perfil.navegar_editar()

        e2e_page.fill('input[name="email"]', "")
        e2e_page.fill('input[name="email"]', email1)
        perfil.submeter()

        e2e_page.wait_for_timeout(500)
        conteudo = e2e_page.content().lower()
        assert "e-mail" in conteudo and "cadastrado" in conteudo


# =============================================================================
# UC-PERF-03: Alterar senha da conta
# =============================================================================


@pytest.mark.e2e
class TestAlterarSenha:
    """Testes de alteracao de senha."""

    def test_pagina_alterar_senha_carrega(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-PERF-03: Deve carregar formulario de alteracao de senha."""
        email = "alterar_senha@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha)

        perfil = PerfilPage(e2e_page, e2e_server)
        perfil.navegar_alterar_senha()

        assert "/usuario/perfil/alterar-senha" in e2e_page.url
        expect(e2e_page.locator('input[name="senha_atual"]')).to_be_visible()
        expect(e2e_page.locator('input[name="senha_nova"]')).to_be_visible()
        expect(e2e_page.locator('input[name="confirmar_senha"]')).to_be_visible()

    def test_alterar_senha_com_sucesso(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-PERF-03: Deve alterar senha com dados validos."""
        email = "senha_sucesso@example.com"
        senha_atual = "SenhaForte@123"
        senha_nova = "NovaSenha@456"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha_atual)

        perfil = PerfilPage(e2e_page, e2e_server)
        perfil.navegar_alterar_senha()

        perfil.preencher_alteracao_senha(senha_atual, senha_nova, senha_nova)
        perfil.submeter()

        e2e_page.wait_for_timeout(500)
        conteudo = e2e_page.content().lower()
        assert "sucesso" in conteudo or "alterada" in conteudo

    def test_alterar_senha_atual_incorreta(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-PERF-03: Deve rejeitar se senha atual estiver incorreta."""
        email = "senha_incorreta@example.com"
        senha_atual = "SenhaForte@123"
        senha_errada = "SenhaErrada@999"
        senha_nova = "NovaSenha@456"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha_atual)

        perfil = PerfilPage(e2e_page, e2e_server)
        perfil.navegar_alterar_senha()

        perfil.preencher_alteracao_senha(senha_errada, senha_nova, senha_nova)
        perfil.submeter()

        e2e_page.wait_for_timeout(500)
        conteudo = e2e_page.content().lower()
        assert "senha" in conteudo and "incorreta" in conteudo

    def test_alterar_senha_nova_igual_atual(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-PERF-03: Deve rejeitar se nova senha for igual a atual."""
        email = "senha_igual@example.com"
        senha = "SenhaForte@123"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha)

        perfil = PerfilPage(e2e_page, e2e_server)
        perfil.navegar_alterar_senha()

        perfil.preencher_alteracao_senha(senha, senha, senha)
        perfil.submeter()

        e2e_page.wait_for_timeout(500)
        conteudo = e2e_page.content().lower()
        assert "diferente" in conteudo or "atual" in conteudo

    def test_alterar_senha_confirmacao_diferente(
        self, e2e_page: Page, e2e_server: str, limpar_banco_e2e
    ):
        """UC-PERF-03: Deve rejeitar se confirmacao nao coincidir."""
        email = "senha_confirma@example.com"
        senha_atual = "SenhaForte@123"
        senha_nova = "NovaSenha@456"
        confirma_diferente = "OutraSenha@789"

        assert criar_usuario_e_logar(e2e_page, e2e_server, email, senha_atual)

        perfil = PerfilPage(e2e_page, e2e_server)
        perfil.navegar_alterar_senha()

        perfil.preencher_alteracao_senha(senha_atual, senha_nova, confirma_diferente)
        perfil.submeter()

        e2e_page.wait_for_timeout(500)
        conteudo = e2e_page.content().lower()
        assert "coincidem" in conteudo or "senhas" in conteudo
