from pydantic import ValidationError
from dtos.area_dto import AlterarAreaDTO, CriarAreaDTO
from model.area_model import Area
from util.exceptions import FormValidationError
from util.logger_config import logger
from typing import Optional
from fastapi import APIRouter, Form, Request, status
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
    
@router.get("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_editar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exibe formulário de alteração de área"""
    area = area_repo.obter_por_id(id)

    if not area:
        informar_erro(request, "Área não encontrada")
        return RedirectResponse("/admin/areas/listar", status_code=status.HTTP_303_SEE_OTHER)

    dados_area = {
        "id_area": area.id_area,
        "nome": area.nome,
        "descricao": area.descricao
    }

    return templates.TemplateResponse(
        "admin/areas/editar.html",
        {"request": request, "area": area, "dados": dados_area}
    )

@router.post("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_editar(
    request: Request,
    id: int,
    nome: str = Form(...),
    descricao: str = Form(""),
    usuario_logado: Optional[dict] = None
):
    """Altera dados de uma área"""
    assert usuario_logado is not None

    area_atual = area_repo.obter_por_id(id)
    if not area_atual:
        informar_erro(request, "Área não encontrada")
        return RedirectResponse("/admin/areas/listar", status_code=status.HTTP_303_SEE_OTHER)

    dados_formulario: dict = {"id_area": id, "nome": nome, "descricao": descricao}

    try:
        # Validar com DTO
        dto = AlterarAreaDTO(id_area=id, nome=nome, descricao=descricao)

        # Verificar se nome já existe em outra área
        area_nome = area_repo.obter_por_nome(dto.nome)
        if area_nome and area_nome.id_area != id:
            informar_erro(request, "Já existe outra área cadastrada com este nome")
            return templates.TemplateResponse(
                "admin/areas/editar.html",
                {"request": request, "area": area_atual, "dados": dados_formulario}
            )

        # Atualizar área
        area_atualizada = Area(id_area=id, nome=dto.nome, descricao=dto.descricao)
        area_repo.alterar(area_atualizada)

        logger.info(f"Área {id} ('{dto.nome}') alterada por admin {usuario_logado['id']}")
        informar_sucesso(request, "Área alterada com sucesso!")

        return RedirectResponse("/admin/areas/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["area"] = area_repo.obter_por_id(id)
        raise FormValidationError(
            validation_error=e,
            template_path="admin/areas/editar.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )