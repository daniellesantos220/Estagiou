#Aprovação de Vaga
from fastapi.params import Form
from pydantic_core import ValidationError
from util.logger_config import logger
from typing import Optional
from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from repo import vaga_repo
from util.auth_decorator import requer_autenticacao
from util.flash_messages import informar_erro, informar_sucesso
from util.perfis import Perfil
from util.template_util import criar_templates
from dtos.vaga_dto import ReprovarVagaDTO


router = APIRouter(prefix="/admin/vagas")
templates = criar_templates("templates/admin/vagas")

@router.post("/aprovar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_aprovar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Aprova uma vaga pendente"""
    assert usuario_logado is not None

    vaga = vaga_repo.obter_por_id(id)
    if not vaga:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    if vaga.status != "Pendente":
        informar_erro(request, "Apenas vagas pendentes podem ser aprovadas")
        logger.warning(f"Admin {usuario_logado['id']} tentou aprovar vaga {id} com status '{vaga.status}'")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Atualizar status para Aprovada
    sucesso = vaga_repo.atualizar_status(id, "Aprovada")

    if sucesso:
        logger.info(f"Vaga {id} ('{vaga.titulo}') aprovada por admin {usuario_logado['id']}")
        informar_sucesso(request, "Vaga aprovada com sucesso! Agora ela está visível publicamente.")
    else:
        logger.error(f"Erro ao aprovar vaga {id}")
        informar_erro(request, "Erro ao aprovar vaga")

    return RedirectResponse("/admin/vagas/listar?status_filtro=Pendente", status_code=status.HTTP_303_SEE_OTHER)


#Arquivamento de Vaga

@router.post("/arquivar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_arquivar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Arquiva uma vaga (aprovada ou reprovada)"""
    assert usuario_logado is not None

    vaga = vaga_repo.obter_por_id(id)
    if not vaga:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    if vaga.status not in ["Aprovada", "Reprovada"]:
        informar_erro(request, "Apenas vagas aprovadas ou reprovadas podem ser arquivadas")
        logger.warning(f"Admin {usuario_logado['id']} tentou arquivar vaga {id} com status '{vaga.status}'")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Atualizar status para Arquivada
    sucesso = vaga_repo.atualizar_status(id, "Arquivada")

    if sucesso:
        logger.info(f"Vaga {id} ('{vaga.titulo}') arquivada por admin {usuario_logado['id']}")
        informar_sucesso(request, "Vaga arquivada com sucesso!")
    else:
        logger.error(f"Erro ao arquivar vaga {id}")
        informar_erro(request, "Erro ao arquivar vaga")

    return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)


#Exclusão de Vaga

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
            f"Considere arquivar a vaga ao invés de excluí-la."
        )
        logger.warning(
            f"Admin {usuario_logado['id']} tentou excluir vaga {id} com {quantidade_candidaturas} candidatura(s)"
        )
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    vaga_repo.excluir(id)
    logger.info(f"Vaga {id} ('{vaga.titulo}') excluída por admin {usuario_logado['id']}")
    informar_sucesso(request, "Vaga excluída com sucesso!")

    return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/reprovar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_reprovar(
    request: Request,
    id: int,
    motivo: str = Form(...),
    usuario_logado: Optional[dict] = None
):
    """Reprova uma vaga pendente com motivo"""
    assert usuario_logado is not None

    vaga = vaga_repo.obter_por_id(id)
    if not vaga:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    if vaga.status != "Pendente":
        informar_erro(request, "Apenas vagas pendentes podem ser reprovadas")
        logger.warning(f"Admin {usuario_logado['id']} tentou reprovar vaga {id} com status '{vaga.status}'")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    try:
        # Validar motivo com DTO
        dto = ReprovarVagaDTO(motivo=motivo)

        # Atualizar status para Reprovada
        sucesso = vaga_repo.atualizar_status(id, "Reprovada")

        if sucesso:
            # Registrar motivo da reprovação
            vaga_repo.registrar_motivo_reprovacao(id, dto.motivo)

            logger.info(
                f"Vaga {id} ('{vaga.titulo}') reprovada por admin {usuario_logado['id']} - "
                f"Motivo: {dto.motivo[:50]}..."
            )
            informar_sucesso(request, "Vaga reprovada. O recrutador será notificado.")
        else:
            logger.error(f"Erro ao reprovar vaga {id}")
            informar_erro(request, "Erro ao reprovar vaga")

        return RedirectResponse("/admin/vagas/listar?status_filtro=Pendente", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        informar_erro(request, f"Motivo inválido: {e.errors()[0]['msg']}")
        return RedirectResponse("/admin/vagas/listar?status_filtro=Pendente", status_code=status.HTTP_303_SEE_OTHER)