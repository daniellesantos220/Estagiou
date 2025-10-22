from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from model.area_model import Area
from repo import area_repo
from dtos.area_dto import CriarAreaDTO, AlterarAreaDTO
from util.auth_decorator import exigir_login, exigir_perfil
from util.perfis import Perfil
from util.flash_messages import informar_sucesso, informar_erro
from util.template_util import criar_templates
from util.logger_config import logger
from util.exceptions import FormValidationError

router = APIRouter(prefix="/admin/areas")
templates = criar_templates("templates/admin/areas")

@router.get("/")
@exigir_login
@exigir_perfil(Perfil.ADMIN)
async def listar_areas(request: Request):
    """Lista todas as áreas."""
    areas = area_repo.obter_todas()
    return templates.TemplateResponse("listar.html", {
        "request": request,
        "areas": areas
    })

@router.get("/nova")
@exigir_login
@exigir_perfil(Perfil.ADMIN)
async def nova_area(request: Request):
    """Exibe formulário para nova área."""
    return templates.TemplateResponse("form.html", {
        "request": request,
        "area": None
    })

@router.post("/nova")
@exigir_login
@exigir_perfil(Perfil.ADMIN)
async def criar_area(
    request: Request,
    nome: str = Form(),
    descricao: str = Form()
):
    """Cria uma nova área."""
    dados_formulario = {"nome": nome, "descricao": descricao}

    try:
        # Validar com DTO
        dto = CriarAreaDTO(nome=nome, descricao=descricao)

        # Verificar se área já existe
        if area_repo.obter_por_nome(dto.nome):
            informar_erro(request, "Já existe uma área com este nome")
            return templates.TemplateResponse("form.html", {
                "request": request,
                "area": None,
                "dados": dados_formulario
            })

        # Criar área
        area = Area(id_area=0, nome=dto.nome, descricao=dto.descricao)
        area_id = area_repo.inserir(area)

        if area_id:
            logger.info(f"Área '{dto.nome}' criada com sucesso")
            informar_sucesso(request, "Área criada com sucesso!")
            return RedirectResponse("/admin/areas", status_code=status.HTTP_303_SEE_OTHER)
        else:
            informar_erro(request, "Erro ao criar área")
            return templates.TemplateResponse("form.html", {
                "request": request,
                "area": None,
                "dados": dados_formulario
            })

    except ValidationError as e:
        raise FormValidationError(
            validation_error=e,
            template_path="admin/areas/form.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome"
        )

@router.get("/{id_area}/editar")
@exigir_login
@exigir_perfil(Perfil.ADMIN)
async def editar_area(request: Request, id_area: int):
    """Exibe formulário para editar área."""
    area = area_repo.obter_por_id(id_area)
    if not area:
        informar_erro(request, "Área não encontrada")
        return RedirectResponse("/admin/areas", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("form.html", {
        "request": request,
        "area": area
    })

@router.post("/{id_area}/editar")
@exigir_login
@exigir_perfil(Perfil.ADMIN)
async def salvar_area(
    request: Request,
    id_area: int,
    nome: str = Form(),
    descricao: str = Form()
):
    """Salva alterações da área."""
    dados_formulario = {"nome": nome, "descricao": descricao}

    try:
        # Validar com DTO
        dto = AlterarAreaDTO(id_area=id_area, nome=nome, descricao=descricao)

        # Criar objeto Area
        area = Area(id_area=dto.id_area, nome=dto.nome, descricao=dto.descricao)

        # Alterar no banco
        if area_repo.alterar(area):
            logger.info(f"Área {id_area} alterada com sucesso")
            informar_sucesso(request, "Área alterada com sucesso!")
            return RedirectResponse("/admin/areas", status_code=status.HTTP_303_SEE_OTHER)
        else:
            informar_erro(request, "Erro ao alterar área")
            return templates.TemplateResponse("form.html", {
                "request": request,
                "area": area,
                "dados": dados_formulario
            })

    except ValidationError as e:
        raise FormValidationError(
            validation_error=e,
            template_path="admin/areas/form.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome"
        )

@router.post("/{id_area}/excluir")
@exigir_login
@exigir_perfil(Perfil.ADMIN)
async def excluir_area(request: Request, id_area: int):
    """Exclui uma área."""
    # Verificar se área está sendo usada
    if area_repo.verificar_uso(id_area) > 0:
        informar_erro(request, "Não é possível excluir área que possui vagas cadastradas")
        return RedirectResponse("/admin/areas", status_code=status.HTTP_303_SEE_OTHER)

    if area_repo.excluir(id_area):
        logger.info(f"Área {id_area} excluída")
        informar_sucesso(request, "Área excluída com sucesso!")
    else:
        informar_erro(request, "Erro ao excluir área")

    return RedirectResponse("/admin/areas", status_code=status.HTTP_303_SEE_OTHER)