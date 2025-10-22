from typing import Optional
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from model.vaga_model import Vaga
from repo import vaga_repo, empresa_repo, area_repo
from dtos.vaga_dto import CriarVagaDTO, AlterarVagaDTO
from util.auth_decorator import requer_autenticacao
from util.perfis import Perfil
from util.flash_messages import informar_sucesso, informar_erro
from util.template_util import criar_templates
from util.logger_config import logger
from util.exceptions import FormValidationError

router = APIRouter(prefix="/recrutador")
templates = criar_templates("templates/recrutador")

@router.get("/dashboard")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def dashboard(request: Request, usuario_logado: Optional[dict] = None):
    """Dashboard do recrutador."""
    assert usuario_logado is not None
    id_recrutador = usuario_logado["id"]

    # Buscar vagas do recrutador
    vagas = vaga_repo.obter_por_recrutador(id_recrutador)

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "vagas": vagas
    })

@router.get("/vagas/nova")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def nova_vaga(request: Request, usuario_logado: Optional[dict] = None):
    """Formulário para criar nova vaga."""
    areas = area_repo.obter_todas()
    empresas = empresa_repo.obter_todas()

    return templates.TemplateResponse("vaga_form.html", {
        "request": request,
        "vaga": None,
        "areas": areas,
        "empresas": empresas
    })

@router.post("/vagas/nova")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def criar_vaga(
    request: Request,
    id_area: int = Form(),
    id_empresa: int = Form(),
    titulo: str = Form(),
    descricao: str = Form(),
    numero_vagas: int = Form(1),
    salario: float = Form(0.0),
    requisitos: str = Form(""),
    beneficios: str = Form(""),
    carga_horaria: int = Form(None),
    modalidade: str = Form(None),
    cidade: str = Form(""),
    uf: str = Form(""),
    usuario_logado: Optional[dict] = None
):
    """Cria nova vaga."""
    assert usuario_logado is not None
    id_recrutador = usuario_logado["id"]

    dados_formulario = {
        "id_area": id_area,
        "id_empresa": id_empresa,
        "titulo": titulo,
        "descricao": descricao,
        "numero_vagas": numero_vagas,
        "salario": salario,
        "requisitos": requisitos,
        "beneficios": beneficios,
        "carga_horaria": carga_horaria,
        "modalidade": modalidade,
        "cidade": cidade,
        "uf": uf
    }

    try:
        # Validar com DTO
        dto = CriarVagaDTO(
            id_area=id_area,
            id_empresa=id_empresa,
            id_recrutador=id_recrutador,
            titulo=titulo,
            descricao=descricao,
            numero_vagas=numero_vagas,
            salario=salario,
            requisitos=requisitos or None,
            beneficios=beneficios or None,
            carga_horaria=carga_horaria,
            modalidade=modalidade or None,
            cidade=cidade or None,
            uf=uf or None
        )

        # Criar vaga
        vaga = Vaga(
            id_vaga=0,
            id_area=dto.id_area,
            id_empresa=dto.id_empresa,
            id_recrutador=dto.id_recrutador,
            status_vaga="aberta",
            descricao=dto.descricao,
            numero_vagas=dto.numero_vagas,
            salario=dto.salario,
            data_cadastro="",
            titulo=dto.titulo,
            requisitos=dto.requisitos,
            beneficios=dto.beneficios,
            carga_horaria=dto.carga_horaria,
            modalidade=dto.modalidade,
            cidade=dto.cidade,
            uf=dto.uf
        )

        vaga_id = vaga_repo.inserir(vaga)

        if vaga_id:
            logger.info(f"Vaga '{dto.titulo}' criada pelo recrutador {id_recrutador}")
            informar_sucesso(request, "Vaga criada com sucesso!")
            return RedirectResponse("/recrutador/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        else:
            informar_erro(request, "Erro ao criar vaga")
            areas = area_repo.obter_todas()
            empresas = empresa_repo.obter_todas()
            return templates.TemplateResponse("vaga_form.html", {
                "request": request,
                "vaga": None,
                "dados": dados_formulario,
                "areas": areas,
                "empresas": empresas
            })

    except ValidationError as e:
        raise FormValidationError(
            validation_error=e,
            template_path="recrutador/vaga_form.html",
            dados_formulario=dados_formulario,
            campo_padrao="titulo"
        )

# Adicionar rotas para editar, excluir, arquivar vagas
# Adicionar rotas para visualizar candidatos de uma vaga
# ... (seguir padrão similar)