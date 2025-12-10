"""
Funcoes auxiliares e Page Objects para testes E2E.

Fornece helpers para interacoes comuns com a UI.
"""

from typing import Optional

from playwright.sync_api import Page, expect


class CadastroPage:
    """Page Object para a pagina de cadastro."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.url = f"{base_url}/cadastrar"

    def navegar(self) -> None:
        """Navega para a pagina de cadastro."""
        self.page.goto(self.url)

    def preencher_formulario(
        self,
        perfil: str,
        nome: str,
        email: str,
        senha: str,
        confirmar_senha: Optional[str] = None,
    ) -> None:
        """
        Preenche o formulario de cadastro.

        Args:
            perfil: "Estudante" ou "Recrutador"
            nome: Nome completo
            email: E-mail
            senha: Senha
            confirmar_senha: Confirmacao de senha (usa senha se nao informado)
        """
        if confirmar_senha is None:
            confirmar_senha = senha

        # Selecionar perfil (radio button com estilo de botao Bootstrap)
        # Precisamos clicar no label pois o input esta escondido
        self.page.locator(f'label[for="perfil_{perfil}"]').click()

        # Preencher campos
        self.page.fill('input[name="nome"]', nome)
        self.page.fill('input[name="email"]', email)
        self.page.fill('input[name="senha"]', senha)
        self.page.fill('input[name="confirmar_senha"]', confirmar_senha)

    def submeter(self) -> None:
        """Submete o formulario."""
        self.page.get_by_role("button", name="Criar Conta").click()

    def cadastrar(
        self,
        perfil: str,
        nome: str,
        email: str,
        senha: str,
        confirmar_senha: Optional[str] = None,
    ) -> None:
        """
        Realiza cadastro completo: preenche e submete.
        """
        self.preencher_formulario(perfil, nome, email, senha, confirmar_senha)
        self.submeter()

    def obter_mensagem_erro_campo(self, campo: str) -> Optional[str]:
        """
        Obtem mensagem de erro de um campo especifico.

        Args:
            campo: Nome do campo (nome, email, senha, confirmar_senha)

        Returns:
            Texto da mensagem de erro ou None
        """
        seletor = f'input[name="{campo}"] ~ .invalid-feedback'
        elemento = self.page.locator(seletor).first

        if elemento.is_visible():
            return elemento.text_content()
        return None

    def obter_mensagem_flash(self) -> Optional[str]:
        """
        Obtem mensagem flash (toast ou alert).

        Returns:
            Texto da mensagem ou None
        """
        toast = self.page.locator(".toast-body").first
        if toast.is_visible():
            return toast.text_content()

        alert = self.page.locator(".alert").first
        if alert.is_visible():
            return alert.text_content()

        return None

    def aguardar_navegacao_login(self, timeout: int = 5000) -> bool:
        """
        Aguarda redirecionamento para pagina de login.

        Args:
            timeout: Tempo maximo em ms

        Returns:
            True se redirecionou, False caso contrario
        """
        try:
            self.page.wait_for_url("**/login**", timeout=timeout)
            return True
        except Exception:
            return False


class LoginPage:
    """Page Object para a pagina de login."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.url = f"{base_url}/login"

    def navegar(self) -> None:
        """Navega para a pagina de login."""
        self.page.goto(self.url)

    def preencher_formulario(self, email: str, senha: str) -> None:
        """Preenche o formulario de login sem submeter."""
        self.page.wait_for_selector('input[name="email"]')
        self.page.fill('input[name="email"]', email)
        self.page.fill('input[name="senha"]', senha)

    def submeter(self) -> None:
        """Submete o formulario de login."""
        self.page.locator('form button[type="submit"]').first.click()

    def fazer_login(self, email: str, senha: str) -> None:
        """Preenche e submete formulario de login."""
        self.preencher_formulario(email, senha)
        self.submeter()

    def esta_na_pagina_login(self) -> bool:
        """Verifica se esta na pagina de login."""
        return "/login" in self.page.url

    def aguardar_navegacao_usuario(self, timeout: int = 10000) -> bool:
        """
        Aguarda redirecionamento para area do usuario.

        Args:
            timeout: Tempo maximo em ms

        Returns:
            True se redirecionou, False caso contrario
        """
        try:
            self.page.wait_for_url("**/usuario**", timeout=timeout)
            return True
        except Exception:
            # Pode ter ido para /home
            return "/usuario" in self.page.url or "/home" in self.page.url

    def obter_mensagem_flash(self) -> Optional[str]:
        """
        Obtem mensagem flash (toast ou alert).

        Returns:
            Texto da mensagem ou None
        """
        toast = self.page.locator(".toast-body").first
        if toast.is_visible():
            return toast.text_content()

        alert = self.page.locator(".alert").first
        if alert.is_visible():
            return alert.text_content()

        return None


class EsqueciSenhaPage:
    """Page Object para a pagina de esqueci senha."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.url = f"{base_url}/esqueci-senha"

    def navegar(self) -> None:
        """Navega para a pagina de esqueci senha."""
        self.page.goto(self.url)

    def preencher_email(self, email: str) -> None:
        """Preenche o campo de email."""
        self.page.fill('input[name="email"]', email)

    def submeter(self) -> None:
        """Submete o formulario."""
        self.page.locator('button[type="submit"]').click()

    def solicitar_recuperacao(self, email: str) -> None:
        """Solicita recuperacao de senha."""
        self.preencher_email(email)
        self.submeter()


class PerfilPage:
    """Page Object para paginas de perfil do usuario."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navegar_visualizar(self) -> None:
        """Navega para visualizar perfil."""
        self.page.goto(f"{self.base_url}/usuario/perfil/visualizar")

    def navegar_editar(self) -> None:
        """Navega para editar perfil."""
        self.page.goto(f"{self.base_url}/usuario/perfil/editar")

    def navegar_alterar_senha(self) -> None:
        """Navega para alterar senha."""
        self.page.goto(f"{self.base_url}/usuario/perfil/alterar-senha")

    def preencher_edicao(
        self,
        nome: str = "",
        data_nascimento: str = "",
        email: str = "",
        numero_documento: str = "",
        telefone: str = "",
    ) -> None:
        """Preenche formulario de edicao de perfil."""
        if nome:
            self.page.fill('input[name="nome"]', nome)
        if data_nascimento:
            self.page.fill('input[name="data_nascimento"]', data_nascimento)
        if email:
            self.page.fill('input[name="email"]', email)
        if numero_documento:
            self.page.fill('input[name="numero_documento"]', numero_documento)
        if telefone:
            self.page.fill('input[name="telefone"]', telefone)

    def preencher_alteracao_senha(
        self, senha_atual: str, senha_nova: str, confirmar_senha: str
    ) -> None:
        """Preenche formulario de alteracao de senha."""
        self.page.fill('input[name="senha_atual"]', senha_atual)
        self.page.fill('input[name="senha_nova"]', senha_nova)
        self.page.fill('input[name="confirmar_senha"]', confirmar_senha)

    def submeter(self) -> None:
        """Submete o formulario atual."""
        self.page.locator('button[type="submit"]').first.click()


class DashboardPage:
    """Page Object para o dashboard do usuario."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.url = f"{base_url}/usuario"

    def navegar(self) -> None:
        """Navega para o dashboard."""
        self.page.goto(self.url)

    def esta_no_dashboard(self) -> bool:
        """Verifica se esta no dashboard."""
        return "/usuario" in self.page.url


class VagasPublicasPage:
    """Page Object para a pagina publica de vagas."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.url = f"{base_url}/vagas"

    def navegar(self) -> None:
        """Navega para a lista de vagas."""
        self.page.goto(self.url)

    def buscar_por_termo(self, termo: str) -> None:
        """Busca vagas por termo."""
        self.page.fill('input[name="termo"]', termo)
        self.page.locator('button[type="submit"]').first.click()

    def selecionar_area(self, id_area: int) -> None:
        """Seleciona uma area no filtro."""
        self.page.select_option('select[name="id_area"]', str(id_area))
        self.page.locator('button[type="submit"]').first.click()

    def clicar_vaga(self, id_vaga: int) -> None:
        """Clica em uma vaga para ver detalhes."""
        self.page.click(f'a[href="/vagas/{id_vaga}"]')

    def navegar_detalhes(self, id_vaga: int) -> None:
        """Navega para detalhes de uma vaga."""
        self.page.goto(f"{self.base_url}/vagas/{id_vaga}")


class CandidaturasPage:
    """Page Object para paginas de candidaturas."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navegar_minhas(self) -> None:
        """Navega para minhas candidaturas."""
        self.page.goto(f"{self.base_url}/candidaturas/minhas")

    def candidatar(self, id_vaga: int) -> None:
        """Realiza candidatura a uma vaga."""
        self.page.goto(f"{self.base_url}/vagas/{id_vaga}")
        self.page.wait_for_timeout(500)
        botao = self.page.locator('form[action*="candidatar"] button[type="submit"]')
        if botao.is_visible():
            botao.click()

    def cancelar(self, id_candidatura: int) -> None:
        """Cancela uma candidatura."""
        self.page.locator(
            f'form[action*="cancelar/{id_candidatura}"] button[type="submit"]'
        ).click()


class RecrutadorVagasPage:
    """Page Object para paginas de vagas do recrutador."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navegar_listar(self) -> None:
        """Navega para lista de vagas do recrutador."""
        self.page.goto(f"{self.base_url}/recrutador/vagas/listar")

    def navegar_cadastrar(self) -> None:
        """Navega para cadastro de nova vaga."""
        self.page.goto(f"{self.base_url}/recrutador/vagas/cadastrar")

    def navegar_editar(self, id_vaga: int) -> None:
        """Navega para edicao de vaga."""
        self.page.goto(f"{self.base_url}/recrutador/vagas/editar/{id_vaga}")

    def navegar_candidatos(self, id_vaga: int) -> None:
        """Navega para ver candidatos de uma vaga."""
        self.page.goto(f"{self.base_url}/recrutador/vagas/{id_vaga}/candidatos")

    def preencher_vaga(
        self,
        titulo: str,
        descricao: str,
        id_area: int,
        numero_vagas: int = 1,
        salario: float = 0.0,
        requisitos: str = "",
        beneficios: str = "",
        carga_horaria: str = "",
        modalidade: str = "",
        cidade: str = "",
        uf: str = "",
    ) -> None:
        """Preenche formulario de vaga."""
        self.page.fill('input[name="titulo"]', titulo)
        self.page.fill('textarea[name="descricao"]', descricao)
        self.page.select_option('select[name="id_area"]', str(id_area))
        self.page.fill('input[name="numero_vagas"]', str(numero_vagas))
        self.page.fill('input[name="salario"]', str(salario))
        if requisitos:
            self.page.fill('textarea[name="requisitos"]', requisitos)
        if beneficios:
            self.page.fill('textarea[name="beneficios"]', beneficios)
        if carga_horaria:
            self.page.fill('input[name="carga_horaria"]', carga_horaria)
        if modalidade:
            self.page.select_option('select[name="modalidade"]', modalidade)
        if cidade:
            self.page.fill('input[name="cidade"]', cidade)
        if uf:
            self.page.select_option('select[name="uf"]', uf)

    def submeter(self) -> None:
        """Submete o formulario."""
        self.page.locator('button[type="submit"]').first.click()

    def alterar_status(self, id_vaga: int, novo_status: str) -> None:
        """Altera status de uma vaga."""
        form = self.page.locator(f'form[action*="alterar-status/{id_vaga}"]')
        form.locator(f'button[value="{novo_status}"]').click()


class ChamadosPage:
    """Page Object para paginas de chamados."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navegar_listar(self) -> None:
        """Navega para lista de chamados."""
        self.page.goto(f"{self.base_url}/chamados/listar")

    def navegar_cadastrar(self) -> None:
        """Navega para cadastro de chamado."""
        self.page.goto(f"{self.base_url}/chamados/cadastrar")

    def navegar_visualizar(self, id_chamado: int) -> None:
        """Navega para visualizar um chamado."""
        self.page.goto(f"{self.base_url}/chamados/{id_chamado}/visualizar")

    def preencher_chamado(
        self, titulo: str, descricao: str, prioridade: str = "Media"
    ) -> None:
        """Preenche formulario de chamado."""
        self.page.fill('input[name="titulo"]', titulo)
        self.page.fill('textarea[name="descricao"]', descricao)
        self.page.select_option('select[name="prioridade"]', prioridade)

    def preencher_resposta(self, mensagem: str) -> None:
        """Preenche campo de resposta."""
        self.page.fill('textarea[name="mensagem"]', mensagem)

    def submeter(self) -> None:
        """Submete o formulario."""
        self.page.locator('button[type="submit"]').first.click()

    def excluir(self, id_chamado: int) -> None:
        """Exclui um chamado."""
        self.page.locator(
            f'form[action*="{id_chamado}/excluir"] button[type="submit"]'
        ).click()


class AdminUsuariosPage:
    """Page Object para administracao de usuarios."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navegar_listar(self) -> None:
        """Navega para lista de usuarios."""
        self.page.goto(f"{self.base_url}/admin/usuarios/listar")

    def navegar_cadastrar(self) -> None:
        """Navega para cadastro de usuario."""
        self.page.goto(f"{self.base_url}/admin/usuarios/cadastrar")

    def navegar_editar(self, id_usuario: int) -> None:
        """Navega para edicao de usuario."""
        self.page.goto(f"{self.base_url}/admin/usuarios/editar/{id_usuario}")

    def preencher_usuario(
        self,
        nome: str,
        data_nascimento: str,
        email: str,
        numero_documento: str,
        telefone: str,
        senha: str = "",
        perfil: str = "Estudante",
        confirmado: bool = False,
    ) -> None:
        """Preenche formulario de usuario."""
        self.page.fill('input[name="nome"]', nome)
        self.page.fill('input[name="data_nascimento"]', data_nascimento)
        self.page.fill('input[name="email"]', email)
        self.page.fill('input[name="numero_documento"]', numero_documento)
        self.page.fill('input[name="telefone"]', telefone)
        if senha:
            self.page.fill('input[name="senha"]', senha)
        self.page.select_option('select[name="perfil"]', perfil)
        if confirmado:
            self.page.check('input[name="confirmado"]')

    def submeter(self) -> None:
        """Submete o formulario."""
        self.page.locator('button[type="submit"]').first.click()

    def excluir(self, id_usuario: int) -> None:
        """Exclui um usuario."""
        self.page.locator(
            f'form[action*="excluir/{id_usuario}"] button[type="submit"]'
        ).click()


class AdminVagasPage:
    """Page Object para administracao de vagas."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navegar_listar(self, status_filtro: str = "") -> None:
        """Navega para lista de vagas."""
        url = f"{self.base_url}/admin/vagas/listar"
        if status_filtro:
            url += f"?status_filtro={status_filtro}"
        self.page.goto(url)

    def aprovar(self, id_vaga: int) -> None:
        """Aprova uma vaga."""
        self.page.locator(
            f'form[action*="aprovar/{id_vaga}"] button[type="submit"]'
        ).click()

    def suspender(self, id_vaga: int) -> None:
        """Suspende uma vaga."""
        self.page.locator(
            f'form[action*="suspender/{id_vaga}"] button[type="submit"]'
        ).click()

    def excluir(self, id_vaga: int) -> None:
        """Exclui uma vaga."""
        self.page.locator(
            f'form[action*="excluir/{id_vaga}"] button[type="submit"]'
        ).click()


class AdminAreasPage:
    """Page Object para administracao de areas."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navegar_listar(self) -> None:
        """Navega para lista de areas."""
        self.page.goto(f"{self.base_url}/admin/areas/listar")

    def navegar_cadastrar(self) -> None:
        """Navega para cadastro de area."""
        self.page.goto(f"{self.base_url}/admin/areas/cadastrar")

    def navegar_editar(self, id_area: int) -> None:
        """Navega para edicao de area."""
        self.page.goto(f"{self.base_url}/admin/areas/editar/{id_area}")

    def preencher_area(self, nome: str, descricao: str = "") -> None:
        """Preenche formulario de area."""
        self.page.fill('input[name="nome"]', nome)
        if descricao:
            self.page.fill('textarea[name="descricao"]', descricao)

    def submeter(self) -> None:
        """Submete o formulario."""
        self.page.locator('button[type="submit"]').first.click()

    def excluir(self, id_area: int) -> None:
        """Exclui uma area."""
        self.page.locator(
            f'form[action*="excluir/{id_area}"] button[type="submit"]'
        ).click()


class AdminChamadosPage:
    """Page Object para administracao de chamados."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navegar_listar(self) -> None:
        """Navega para lista de chamados."""
        self.page.goto(f"{self.base_url}/admin/chamados/listar")

    def navegar_responder(self, id_chamado: int) -> None:
        """Navega para responder chamado."""
        self.page.goto(f"{self.base_url}/admin/chamados/{id_chamado}/responder")

    def preencher_resposta(self, mensagem: str, novo_status: str = "") -> None:
        """Preenche resposta do chamado."""
        self.page.fill('textarea[name="mensagem"]', mensagem)
        if novo_status:
            self.page.select_option('select[name="novo_status"]', novo_status)

    def submeter(self) -> None:
        """Submete o formulario."""
        self.page.locator('button[type="submit"]').first.click()

    def fechar(self, id_chamado: int) -> None:
        """Fecha um chamado."""
        self.page.locator(
            f'form[action*="{id_chamado}/fechar"] button[type="submit"]'
        ).click()

    def reabrir(self, id_chamado: int) -> None:
        """Reabre um chamado."""
        self.page.locator(
            f'form[action*="{id_chamado}/reabrir"] button[type="submit"]'
        ).click()


class AdminConfiguracoesPage:
    """Page Object para configuracoes do sistema."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navegar(self) -> None:
        """Navega para configuracoes."""
        self.page.goto(f"{self.base_url}/admin/configuracoes")

    def navegar_tema(self) -> None:
        """Navega para selecao de tema."""
        self.page.goto(f"{self.base_url}/admin/tema")


class AdminBackupsPage:
    """Page Object para gerenciamento de backups."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navegar_listar(self) -> None:
        """Navega para lista de backups."""
        self.page.goto(f"{self.base_url}/admin/backups/listar")

    def criar_backup(self) -> None:
        """Cria um novo backup."""
        self.page.locator('form[action*="criar"] button[type="submit"]').click()


class AdminAuditoriaPage:
    """Page Object para auditoria do sistema."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navegar(self, data: str = "", nivel: str = "") -> None:
        """Navega para pagina de auditoria."""
        url = f"{self.base_url}/admin/auditoria"
        params = []
        if data:
            params.append(f"data={data}")
        if nivel:
            params.append(f"nivel={nivel}")
        if params:
            url += "?" + "&".join(params)
        self.page.goto(url)


class PaginaPublicaPage:
    """Page Object para paginas publicas."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navegar_home(self) -> None:
        """Navega para home."""
        self.page.goto(self.base_url)

    def navegar_sobre(self) -> None:
        """Navega para pagina sobre."""
        self.page.goto(f"{self.base_url}/sobre")


# =============================================================================
# Funcoes auxiliares
# =============================================================================


def verificar_mensagem_sucesso_cadastro(page: Page) -> bool:
    """
    Verifica se a mensagem de sucesso do cadastro foi exibida.

    A mensagem esperada e: "Cadastro realizado com sucesso!"
    """
    try:
        toast = page.locator(".toast-body")
        if toast.is_visible():
            texto = toast.text_content() or ""
            return "cadastro realizado com sucesso" in texto.lower()

        alert = page.locator(".alert-success")
        if alert.is_visible():
            texto = alert.text_content() or ""
            return "cadastro realizado com sucesso" in texto.lower()
    except Exception:
        pass

    return False


def verificar_erro_email_duplicado(page: Page) -> bool:
    """
    Verifica se apareceu erro de e-mail duplicado.

    A mensagem esperada contem: "e-mail ja esta cadastrado"
    """
    try:
        conteudo = page.content().lower()
        return "e-mail" in conteudo and "cadastrado" in conteudo
    except Exception:
        return False


def verificar_erro_senhas_diferentes(page: Page) -> bool:
    """
    Verifica se apareceu erro de senhas nao coincidentes.

    A mensagem esperada: "As senhas nao coincidem."
    """
    try:
        conteudo = page.content().lower()
        return "senhas" in conteudo and "coincidem" in conteudo
    except Exception:
        return False


def verificar_mensagem_flash(page: Page, texto_esperado: str) -> bool:
    """
    Verifica se uma mensagem flash contem o texto esperado.
    """
    try:
        page.wait_for_timeout(500)
        conteudo = page.content().lower()
        return texto_esperado.lower() in conteudo
    except Exception:
        return False


def criar_usuario_e_logar(
    page: Page,
    base_url: str,
    email: str,
    senha: str,
    nome: str = "Usuario Teste Nome",
    perfil: str = "Estudante",
) -> bool:
    """
    Cria um usuario e faz login.
    Retorna True se login foi bem sucedido.
    """
    cadastro = CadastroPage(page, base_url)
    cadastro.navegar()
    cadastro.cadastrar(perfil=perfil, nome=nome, email=email, senha=senha)

    if not cadastro.aguardar_navegacao_login():
        return False

    login = LoginPage(page, base_url)
    login.fazer_login(email, senha)

    return login.aguardar_navegacao_usuario()


def fazer_logout(page: Page, base_url: str) -> None:
    """Faz logout do sistema."""
    page.goto(f"{base_url}/logout")
    page.wait_for_timeout(500)
