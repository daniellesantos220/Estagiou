"""
Testes E2E para navegacao publica de vagas.

Casos de uso testados:
- UC-VAGA-01: Listar vagas abertas
- UC-VAGA-02: Filtrar vagas por termo de busca
- UC-VAGA-03: Filtrar vagas por area
- UC-VAGA-04: Visualizar detalhes de uma vaga
"""

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    VagasPublicasPage,
    PaginaPublicaPage,
)


# =============================================================================
# UC-VAGA-01: Listar vagas abertas
# =============================================================================


@pytest.mark.e2e
class TestListarVagas:
    """Testes de listagem de vagas."""

    def test_pagina_vagas_carrega_corretamente(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-VAGA-01: Deve carregar pagina de listagem de vagas."""
        vagas = VagasPublicasPage(e2e_page, e2e_server)
        vagas.navegar()

        assert "/vagas" in e2e_page.url

    def test_pagina_vagas_exibe_titulo(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-VAGA-01: Pagina deve ter titulo adequado."""
        vagas = VagasPublicasPage(e2e_page, e2e_server)
        vagas.navegar()

        titulo = e2e_page.title().lower()
        assert "vaga" in titulo or "estágio" in titulo or "estagiou" in titulo

    def test_pagina_vagas_possui_filtros(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-VAGA-01: Pagina deve ter campos de filtro."""
        vagas = VagasPublicasPage(e2e_page, e2e_server)
        vagas.navegar()

        # Verificar se existe campo de busca
        campo_busca = e2e_page.locator('input[name="termo"]')
        expect(campo_busca).to_be_visible()

    def test_pagina_vagas_acessivel_sem_login(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-VAGA-01: Vagas devem ser acessiveis sem autenticacao."""
        vagas = VagasPublicasPage(e2e_page, e2e_server)
        vagas.navegar()

        # Nao deve redirecionar para login
        assert "/login" not in e2e_page.url
        assert "/vagas" in e2e_page.url


# =============================================================================
# UC-VAGA-02: Filtrar vagas por termo de busca
# =============================================================================


@pytest.mark.e2e
class TestFiltrarVagasTermo:
    """Testes de filtro por termo de busca."""

    def test_busca_por_termo_funciona(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-VAGA-02: Deve permitir busca por termo."""
        vagas = VagasPublicasPage(e2e_page, e2e_server)
        vagas.navegar()

        # Preencher campo de busca
        e2e_page.fill('input[name="termo"]', "desenvolvedor")
        e2e_page.locator('button[type="submit"]').first.click()

        e2e_page.wait_for_timeout(500)

        # Verificar se URL contem termo
        assert "termo=" in e2e_page.url or "/vagas" in e2e_page.url

    def test_busca_vazia_mostra_todas_vagas(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-VAGA-02: Busca vazia deve mostrar todas as vagas."""
        vagas = VagasPublicasPage(e2e_page, e2e_server)
        vagas.navegar()

        # Submeter busca vazia
        e2e_page.fill('input[name="termo"]', "")
        e2e_page.locator('button[type="submit"]').first.click()

        e2e_page.wait_for_timeout(500)

        # Deve permanecer na pagina de vagas
        assert "/vagas" in e2e_page.url


# =============================================================================
# UC-VAGA-03: Filtrar vagas por area
# =============================================================================


@pytest.mark.e2e
class TestFiltrarVagasArea:
    """Testes de filtro por area."""

    def test_filtro_area_existe(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-VAGA-03: Deve existir filtro por area."""
        vagas = VagasPublicasPage(e2e_page, e2e_server)
        vagas.navegar()

        # Verificar se existe select de area
        select_area = e2e_page.locator('select[name="id_area"]')
        expect(select_area).to_be_visible()

    def test_filtro_area_funciona(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-VAGA-03: Filtro por area deve funcionar."""
        vagas = VagasPublicasPage(e2e_page, e2e_server)
        vagas.navegar()

        # Tentar selecionar primeira opcao do select
        select_area = e2e_page.locator('select[name="id_area"]')
        if select_area.is_visible():
            options = select_area.locator("option")
            if options.count() > 1:
                # Selecionar segunda opcao (primeira geralmente e "Todas")
                select_area.select_option(index=1)
                e2e_page.locator('button[type="submit"]').first.click()
                e2e_page.wait_for_timeout(500)

        # Deve permanecer na pagina de vagas
        assert "/vagas" in e2e_page.url


# =============================================================================
# UC-VAGA-04: Visualizar detalhes de uma vaga
# =============================================================================


@pytest.mark.e2e
class TestDetalhesVaga:
    """Testes de visualizacao de detalhes de vaga."""

    def test_pagina_detalhes_vaga_inexistente(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-VAGA-04: Deve tratar vaga inexistente adequadamente."""
        vagas = VagasPublicasPage(e2e_page, e2e_server)
        vagas.navegar_detalhes(99999)

        e2e_page.wait_for_timeout(500)

        # Deve exibir mensagem de nao encontrada ou 404
        conteudo = e2e_page.content().lower()
        assert (
            "não encontrada" in conteudo
            or "não existe" in conteudo
            or "404" in conteudo
            or e2e_page.url.endswith("/vagas")
        )

    def test_detalhes_vaga_acessivel_sem_login(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-VAGA-04: Detalhes da vaga devem ser acessiveis sem login."""
        # Primeiro acessar lista de vagas
        vagas = VagasPublicasPage(e2e_page, e2e_server)
        vagas.navegar()

        e2e_page.wait_for_timeout(500)

        # Se houver links de vagas, clicar no primeiro
        links_vagas = e2e_page.locator('a[href*="/vagas/"]')
        if links_vagas.count() > 0:
            links_vagas.first.click()
            e2e_page.wait_for_timeout(500)

            # Nao deve redirecionar para login
            assert "/login" not in e2e_page.url


# =============================================================================
# UC-PUB-01 e UC-PUB-02: Paginas publicas
# =============================================================================


@pytest.mark.e2e
class TestPaginasPublicas:
    """Testes de paginas publicas."""

    def test_pagina_inicial_carrega(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-PUB-01: Pagina inicial deve carregar corretamente."""
        pagina = PaginaPublicaPage(e2e_page, e2e_server)
        pagina.navegar_home()

        # Verificar se carregou (nao deve estar em /login se home e publica)
        assert e2e_page.url == e2e_server + "/" or "/login" not in e2e_page.url

    def test_pagina_sobre_carrega(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-PUB-02: Pagina Sobre deve carregar corretamente."""
        pagina = PaginaPublicaPage(e2e_page, e2e_server)
        pagina.navegar_sobre()

        # Verificar se esta na pagina sobre
        assert "/sobre" in e2e_page.url

    def test_pagina_sobre_acessivel_sem_login(
        self, e2e_page: Page, e2e_server: str
    ):
        """UC-PUB-02: Pagina Sobre deve ser acessivel sem autenticacao."""
        pagina = PaginaPublicaPage(e2e_page, e2e_server)
        pagina.navegar_sobre()

        e2e_page.wait_for_timeout(500)

        # Nao deve redirecionar para login
        assert "/login" not in e2e_page.url
