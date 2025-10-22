from fastapi import APIRouter, Request, Query
from typing import Optional

from repo import vaga_repo
from util.template_util import criar_templates

router = APIRouter(prefix="/vagas")
templates = criar_templates("templates/vagas")

@router.get("/")
async def listar_vagas(
    request: Request,
    area: Optional[int] = Query(None),
    cidade: Optional[str] = Query(None),
    uf: Optional[str] = Query(None),
    modalidade: Optional[str] = Query(None),
    salario_min: Optional[float] = Query(None),
    pagina: int = Query(1, ge=1)
):
    """Lista vagas abertas com filtros (acesso público)."""
    limite = 20
    offset = (pagina - 1) * limite

    # Buscar vagas com filtros
    vagas = vaga_repo.buscar(
        id_area=area,
        cidade=cidade,
        uf=uf,
        modalidade=modalidade,
        salario_min=salario_min,
        limit=limite,
        offset=offset
    )

    return templates.TemplateResponse("listar.html", {
        "request": request,
        "vagas": vagas,
        "filtros": {
            "area": area,
            "cidade": cidade,
            "uf": uf,
            "modalidade": modalidade,
            "salario_min": salario_min
        },
        "pagina": pagina
    })

@router.get("/{id_vaga}")
async def detalhes_vaga(request: Request, id_vaga: int):
    """Exibe detalhes de uma vaga específica."""
    vaga = vaga_repo.obter_por_id(id_vaga)
    if not vaga:
        # Retornar 404 ou redirecionar
        return templates.TemplateResponse("404.html", {
            "request": request,
            "mensagem": "Vaga não encontrada"
        }, status_code=404)

    return templates.TemplateResponse("detalhes.html", {
        "request": request,
        "vaga": vaga
    })