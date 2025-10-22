from util.logger_config import logger
from typing import Optional
from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from repo import area_repo
from util.auth_decorator import requer_autenticacao
from util.flash_messages import informar_erro, informar_sucesso
from util.perfis import Perfil
from util.template_util import criar_templates


router = APIRouter(prefix="/admin/areas")
templates = criar_templates("templates/admin/areas")

@router.post("/excluir/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui uma área"""
    assert usuario_logado is not None

    area = area_repo.obter_por_id(id)
    if not area:
        informar_erro(request, "Área não encontrada")
        return RedirectResponse("/admin/areas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se área está sendo usada por vagas
    quantidade_vagas = area_repo.verificar_uso(id)
    if quantidade_vagas > 0:
        informar_erro(
            request,
            f"Não é possível excluir esta área pois existem {quantidade_vagas} vaga(s) vinculada(s) a ela"
        )
        logger.warning(
            f"Admin {usuario_logado['id']} tentou excluir área {id} com {quantidade_vagas} vaga(s) vinculada(s)"
        )
        return RedirectResponse("/admin/areas/listar", status_code=status.HTTP_303_SEE_OTHER)

    area_repo.excluir(id)
    logger.info(f"Área {id} ('{area.nome}') excluída por admin {usuario_logado['id']}")
    informar_sucesso(request, "Área excluída com sucesso!")

    return RedirectResponse("/admin/areas/listar", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as áreas cadastradas no sistema"""
    areas = area_repo.obter_todas()
    return templates.TemplateResponse(
        "admin/areas/listar.html",
        {"request": request, "areas": areas}
    )

@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de área"""
    return templates.TemplateResponse(
        "admin/areas/cadastro.html",
        {"request": request}
    )

@router.post("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(""),
    usuario_logado: Optional[dict] = None
):
    """Cadastra uma nova área"""
    assert usuario_logado is not None

    dados_formulario: dict = {"nome": nome, "descricao": descricao}

    try:
        # Validar com DTO
        dto = CriarAreaDTO(nome=nome, descricao=descricao)

        # Verificar se área com mesmo nome já existe
        area_existente = area_repo.obter_por_nome(dto.nome)
        if area_existente:
            informar_erro(request, "Já existe uma área cadastrada com este nome")
            return templates.TemplateResponse(
                "admin/areas/cadastro.html",
                {"request": request, "dados": dados_formulario}
            )

        # Criar área
        area = Area(id_area=0, nome=dto.nome, descricao=dto.descricao)
        area_repo.inserir(area)

        logger.info(f"Área '{dto.nome}' cadastrada por admin {usuario_logado['id']}")
        informar_sucesso(request, "Área cadastrada com sucesso!")

        return RedirectResponse("/admin/areas/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        raise FormValidationError(
            validation_error=e,
            template_path="admin/areas/cadastro.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )