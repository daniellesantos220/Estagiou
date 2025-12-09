"""Rotas públicas de vagas (acessíveis sem autenticação)."""
from typing import Optional
from fastapi import APIRouter, Request, Query

from repo import vaga_repo, area_repo, candidatura_repo
from util.template_util import criar_templates

router = APIRouter(prefix="/vagas")
templates = criar_templates()


@router.get("/")
async def listar_vagas(
    request: Request,
    termo: Optional[str] = Query(None),
    id_area: Optional[int] = Query(None),
):
    """Lista vagas abertas com filtros de busca"""

    # Buscar vagas com filtros
    if termo or id_area:
        vagas = vaga_repo.buscar_por_termo(termo=termo, id_area=id_area)
    else:
        vagas = vaga_repo.obter_vagas_abertas(limit=50)

    # Enriquecer vagas com dados de área
    vagas_enriquecidas = []
    for vaga in vagas:
        area = area_repo.obter_por_id(vaga.id_area) if vaga.id_area else None
        vagas_enriquecidas.append({
            "vaga": vaga,
            "area_nome": area.nome if area else "N/A",
        })

    # Buscar todas as áreas para o filtro
    areas = area_repo.obter_todas()

    return templates.TemplateResponse(
        "vagas/listar.html",
        {
            "request": request,
            "vagas": vagas_enriquecidas,
            "areas": areas,
            "termo": termo or "",
            "id_area": id_area,
        }
    )


@router.get("/{id}")
async def detalhes_vaga(request: Request, id: int):
    """Exibe detalhes de uma vaga"""

    vaga = vaga_repo.obter_por_id(id)

    if not vaga:
        return templates.TemplateResponse(
            "vagas/nao_encontrada.html",
            {"request": request},
            status_code=404
        )

    # Buscar área
    area = area_repo.obter_por_id(vaga.id_area) if vaga.id_area else None

    # Verificar se usuário logado já se candidatou
    ja_candidatou = False
    usuario_logado = request.session.get("usuario_logado")
    if usuario_logado and usuario_logado.get("perfil") == "Estudante":
        ja_candidatou = candidatura_repo.verificar_candidatura_existente(id, usuario_logado["id"])

    return templates.TemplateResponse(
        "vagas/detalhes.html",
        {
            "request": request,
            "vaga": vaga,
            "area": area,
            "ja_candidatou": ja_candidatou,
        }
    )
