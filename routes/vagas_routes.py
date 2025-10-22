from typing import Optional
from fastapi import APIRouter, Form, Request, Query, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from repo import vaga_repo, area_repo, empresa_repo
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.logger_config import logger
from util.perfis import Perfil

router = APIRouter(prefix="/admin/vagas")
templates = criar_templates("templates/admin/vagas")

@router.get("/")
@requer_autenticacao([Perfil.ADMIN.value])
async def index(request: Request, usuario_logado: Optional[dict] = None):
    """Redireciona para lista de vagas"""
    return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_307_TEMPORARY_REDIRECT)

@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def listar(
    request: Request,
    status_filtro: Optional[str] = Query("Pendente"),
    usuario_logado: Optional[dict] = None
):
    """Lista vagas para moderação com filtro de status"""

    # Buscar vagas por status
    if status_filtro:
        vagas = vaga_repo.obter_por_status(status_filtro)
    else:
        vagas = vaga_repo.obter_todas()

    # Enriquecer vagas com dados de área e empresa
    vagas_enriquecidas = []
    for vaga in vagas:
        area = area_repo.obter_por_id(vaga.id_area) if vaga.id_area else None
        empresa = empresa_repo.obter_por_id(vaga.id_empresa) if vaga.id_empresa else None

        vagas_enriquecidas.append({
            "vaga": vaga,
            "area_nome": area.nome if area else "N/A",
            "empresa_nome": empresa.nome if empresa else "N/A"
        })

    status_opcoes = ["Pendente", "Aprovada", "Reprovada", "Arquivada"]

    return templates.TemplateResponse(
        "admin/vagas/listar.html",
        {
            "request": request,
            "vagas": vagas_enriquecidas,
            "status_filtro": status_filtro,
            "status_opcoes": status_opcoes
        }
    )