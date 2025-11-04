from typing import Optional
from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from util.auth_decorator import requer_autenticacao
from util.perfis import Perfil
from util.rate_limiter import RateLimiter
from util.template_util import criar_templates


router = APIRouter(prefix="/admin/[curtidas]")
templates = criar_templates("templates/admin/[curtidas]")

admin_curtidas_limiter = RateLimiter(
    max_tentativas=10,
    janela_minutos=1,
    nome="admin_curtidas",
)

@router.get("/")
@requer_autenticacao([Perfil.ADMIN.value])
async def index(request: Request, usuario_logado: Optional[dict] = None):
    """Redireciona para lista"""
    return RedirectResponse("/admin/[seu_recurso]/listar", status_code=status.HTTP_307_TEMPORARY_REDIRECT)