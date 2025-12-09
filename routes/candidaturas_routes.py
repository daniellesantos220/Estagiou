"""Rotas de candidaturas para estudantes."""
from typing import Optional
from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from model.candidatura_model import Candidatura
from repo import candidatura_repo, vaga_repo
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.logger_config import logger
from util.perfis import Perfil

router = APIRouter(prefix="/candidaturas")
templates = criar_templates()


@router.get("/")
@requer_autenticacao([Perfil.ESTUDANTE.value])
async def index(request: Request, usuario_logado: Optional[dict] = None):
    """Redireciona para lista de candidaturas"""
    return RedirectResponse(
        "/candidaturas/minhas", status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )


@router.get("/minhas")
@requer_autenticacao([Perfil.ESTUDANTE.value])
async def minhas_candidaturas(request: Request, usuario_logado: Optional[dict] = None):
    """Lista candidaturas do estudante logado"""
    assert usuario_logado is not None

    candidaturas = candidatura_repo.obter_por_candidato_com_vaga(usuario_logado["id"])

    return templates.TemplateResponse(
        "candidaturas/minhas.html",
        {"request": request, "candidaturas": candidaturas}
    )


@router.post("/candidatar/{id_vaga}")
@requer_autenticacao([Perfil.ESTUDANTE.value])
async def candidatar(request: Request, id_vaga: int, usuario_logado: Optional[dict] = None):
    """Realiza candidatura a uma vaga"""
    assert usuario_logado is not None

    # Verificar se a vaga existe
    vaga = vaga_repo.obter_por_id(id_vaga)
    if not vaga:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse("/vagas", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se a vaga está aberta
    if vaga.status_vaga != "aberta":
        informar_erro(request, "Esta vaga não está mais aceitando candidaturas")
        return RedirectResponse(f"/vagas/{id_vaga}", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se já existe candidatura
    ja_candidatou = candidatura_repo.verificar_candidatura_existente(id_vaga, usuario_logado["id"])
    if ja_candidatou:
        informar_erro(request, "Você já se candidatou a esta vaga")
        return RedirectResponse(f"/vagas/{id_vaga}", status_code=status.HTTP_303_SEE_OTHER)

    # Criar candidatura
    candidatura = Candidatura(
        id_candidatura=0,
        id_vaga=id_vaga,
        id_candidato=usuario_logado["id"],
        status="pendente"
    )

    try:
        id_candidatura = candidatura_repo.inserir(candidatura)
        logger.info(f"Candidatura {id_candidatura} criada: estudante {usuario_logado['id']} -> vaga {id_vaga}")
        informar_sucesso(request, f"Candidatura realizada com sucesso! Boa sorte!")
    except Exception as e:
        logger.error(f"Erro ao criar candidatura: {e}")
        informar_erro(request, "Erro ao processar sua candidatura. Tente novamente.")

    return RedirectResponse("/candidaturas/minhas", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/cancelar/{id_candidatura}")
@requer_autenticacao([Perfil.ESTUDANTE.value])
async def cancelar_candidatura(request: Request, id_candidatura: int, usuario_logado: Optional[dict] = None):
    """Cancela uma candidatura"""
    assert usuario_logado is not None

    # Verificar se a candidatura existe
    candidatura = candidatura_repo.obter_por_id(id_candidatura)
    if not candidatura:
        informar_erro(request, "Candidatura não encontrada")
        return RedirectResponse("/candidaturas/minhas", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se a candidatura pertence ao estudante
    if candidatura.id_candidato != usuario_logado["id"]:
        informar_erro(request, "Você não tem permissão para cancelar esta candidatura")
        return RedirectResponse("/candidaturas/minhas", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se pode ser cancelada (não pode cancelar se já foi aprovada ou rejeitada)
    if candidatura.status in ["aprovado", "rejeitado"]:
        informar_erro(request, f"Não é possível cancelar uma candidatura que já foi {candidatura.status}")
        return RedirectResponse("/candidaturas/minhas", status_code=status.HTTP_303_SEE_OTHER)

    # Atualizar status para cancelado
    sucesso = candidatura_repo.alterar_status(id_candidatura, "cancelado")

    if sucesso:
        logger.info(f"Candidatura {id_candidatura} cancelada pelo estudante {usuario_logado['id']}")
        informar_sucesso(request, "Candidatura cancelada com sucesso!")
    else:
        informar_erro(request, "Erro ao cancelar candidatura")

    return RedirectResponse("/candidaturas/minhas", status_code=status.HTTP_303_SEE_OTHER)
