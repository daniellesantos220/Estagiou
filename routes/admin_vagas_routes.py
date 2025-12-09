"""Rotas de administração de vagas (aprovação/moderação)."""
from typing import Optional
from fastapi import APIRouter, Form, Request, Query, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from dtos.vaga_dto import ReprovarVagaDTO
from repo import vaga_repo, area_repo
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.logger_config import logger
from util.perfis import Perfil
from util.exceptions import ErroValidacaoFormulario

router = APIRouter(prefix="/admin/vagas")
templates = criar_templates()


@router.get("/")
@requer_autenticacao([Perfil.ADMIN.value])
async def index(request: Request, usuario_logado: Optional[dict] = None):
    """Redireciona para lista de vagas"""
    return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def listar(
    request: Request,
    status_filtro: Optional[str] = Query(None),
    usuario_logado: Optional[dict] = None
):
    """Lista vagas para moderação com filtro de status"""

    # Buscar vagas por status
    if status_filtro:
        vagas = vaga_repo.obter_por_status(status_filtro)
    else:
        vagas = vaga_repo.obter_todas()

    # Enriquecer vagas com dados de área
    vagas_enriquecidas = []
    for vaga in vagas:
        area = area_repo.obter_por_id(vaga.id_area) if vaga.id_area else None

        vagas_enriquecidas.append({
            "vaga": vaga,
            "area_nome": area.nome if area else "N/A",
            "recrutador_nome": vaga.recrutador_nome if vaga.recrutador_nome else "N/A"
        })

    status_opcoes = ["aberta", "fechada", "suspensa"]

    return templates.TemplateResponse(
        "admin/vagas/listar.html",
        {
            "request": request,
            "vagas": vagas_enriquecidas,
            "status_filtro": status_filtro,
            "status_opcoes": status_opcoes
        }
    )


@router.post("/aprovar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_aprovar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Aprova uma vaga (abre)"""
    assert usuario_logado is not None

    vaga = vaga_repo.obter_por_id(id)
    if not vaga:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Atualizar status para aberta
    sucesso = vaga_repo.atualizar_status(id, "aberta")

    if sucesso:
        logger.info(f"Vaga {id} ('{vaga.titulo}') aprovada por admin {usuario_logado['id']}")
        informar_sucesso(request, "Vaga aprovada com sucesso! Agora ela está visível publicamente.")
    else:
        logger.error(f"Erro ao aprovar vaga {id}")
        informar_erro(request, "Erro ao aprovar vaga")

    return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/suspender/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_suspender(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Suspende uma vaga"""
    assert usuario_logado is not None

    vaga = vaga_repo.obter_por_id(id)
    if not vaga:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Atualizar status para suspensa
    sucesso = vaga_repo.atualizar_status(id, "suspensa")

    if sucesso:
        logger.info(f"Vaga {id} ('{vaga.titulo}') suspensa por admin {usuario_logado['id']}")
        informar_sucesso(request, "Vaga suspensa com sucesso!")
    else:
        logger.error(f"Erro ao suspender vaga {id}")
        informar_erro(request, "Erro ao suspender vaga")

    return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/excluir/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui uma vaga (qualquer status)"""
    assert usuario_logado is not None

    vaga = vaga_repo.obter_por_id(id)
    if not vaga:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se há candidaturas vinculadas
    quantidade_candidaturas = vaga_repo.contar_candidaturas(id)
    if quantidade_candidaturas > 0:
        informar_erro(
            request,
            f"Não é possível excluir esta vaga pois existem {quantidade_candidaturas} candidatura(s) vinculada(s). "
            f"Considere suspender a vaga ao invés de excluí-la."
        )
        logger.warning(
            f"Admin {usuario_logado['id']} tentou excluir vaga {id} com {quantidade_candidaturas} candidatura(s)"
        )
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    vaga_repo.excluir(id)
    logger.info(f"Vaga {id} ('{vaga.titulo}') excluída por admin {usuario_logado['id']}")
    informar_sucesso(request, "Vaga excluída com sucesso!")

    return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)
