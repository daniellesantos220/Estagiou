from fastapi import APIRouter, Request, status

from repo import vaga_repo, area_repo
from util.template_util import criar_templates
from util.rate_limiter import DynamicRateLimiter, obter_identificador_cliente
from util.flash_messages import informar_erro
from util.logger_config import logger

router = APIRouter()
templates_public = criar_templates()


def obter_ultimas_vagas_para_home():
    """Busca as últimas 6 vagas abertas e enriquece com dados de área."""
    try:
        vagas = vaga_repo.obter_ultimas_abertas(6)
        vagas_enriquecidas = []
        for vaga in vagas:
            area = area_repo.obter_por_id(vaga.id_area) if vaga.id_area else None
            vagas_enriquecidas.append({
                "vaga": vaga,
                "area_nome": area.nome if area else "N/A",
            })
        return vagas_enriquecidas
    except Exception as e:
        logger.error(f"Erro ao buscar vagas para home: {e}")
        return []

# Rate limiter para páginas públicas (proteção contra DDoS)
public_limiter = DynamicRateLimiter(
    chave_max="rate_limit_public_max",
    chave_minutos="rate_limit_public_minutos",
    padrao_max=100,
    padrao_minutos=1,
    nome="public_pages",
)


@router.get("/")
async def home(request: Request):
    """
    Rota inicial - Landing Page pública (sempre)
    Exibe as últimas 6 vagas abertas em cards
    """
    # Rate limiting por IP
    ip = obter_identificador_cliente(request)
    if not public_limiter.verificar(ip):
        informar_erro(request, "Muitas requisições. Aguarde alguns minutos.")
        logger.warning(f"Rate limit excedido para página pública - IP: {ip}")
        return templates_public.TemplateResponse(
            "errors/429.html",
            {"request": request},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    # Buscar últimas vagas para a home page
    vagas = obter_ultimas_vagas_para_home()

    return templates_public.TemplateResponse("index.html", {"request": request, "vagas": vagas})


@router.get("/index")
async def index(request: Request):
    """
    Página pública inicial (Landing Page)
    Sempre exibe a página pública, independentemente de autenticação
    Exibe as últimas 6 vagas abertas em cards
    """
    # Rate limiting por IP
    ip = obter_identificador_cliente(request)
    if not public_limiter.verificar(ip):
        informar_erro(request, "Muitas requisições. Aguarde alguns minutos.")
        logger.warning(f"Rate limit excedido para página pública - IP: {ip}")
        return templates_public.TemplateResponse(
            "errors/429.html",
            {"request": request},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    # Buscar últimas vagas para a home page
    vagas = obter_ultimas_vagas_para_home()

    return templates_public.TemplateResponse("index.html", {"request": request, "vagas": vagas})


@router.get("/sobre")
async def sobre(request: Request):
    """
    Página "Sobre" com informações do projeto acadêmico
    """
    # Rate limiting por IP
    ip = obter_identificador_cliente(request)
    if not public_limiter.verificar(ip):
        informar_erro(request, "Muitas requisições. Aguarde alguns minutos.")
        logger.warning(f"Rate limit excedido para página pública - IP: {ip}")
        return templates_public.TemplateResponse(
            "errors/429.html",
            {"request": request},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    return templates_public.TemplateResponse("sobre.html", {"request": request})
