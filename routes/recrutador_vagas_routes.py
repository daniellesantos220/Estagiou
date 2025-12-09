"""Rotas de vagas para recrutadores."""
from typing import Optional
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from dtos.vaga_dto import CriarVagaDTO, AlterarVagaDTO
from model.vaga_model import Vaga
from repo import vaga_repo, area_repo
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.logger_config import logger
from util.perfis import Perfil
from util.exceptions import ErroValidacaoFormulario

router = APIRouter(prefix="/recrutador/vagas")
templates = criar_templates()


@router.get("/")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def index(request: Request, usuario_logado: Optional[dict] = None):
    """Redireciona para lista de vagas"""
    return RedirectResponse(
        "/recrutador/vagas/listar", status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )


@router.get("/listar")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista vagas do recrutador logado"""
    assert usuario_logado is not None

    vagas = vaga_repo.obter_por_recrutador(usuario_logado["id"])

    # Enriquecer vagas com dados de área e quantidade de candidaturas
    vagas_enriquecidas = []
    for vaga in vagas:
        area = area_repo.obter_por_id(vaga.id_area) if vaga.id_area else None
        qtd_candidaturas = vaga_repo.contar_candidaturas(vaga.id_vaga)

        vagas_enriquecidas.append({
            "vaga": vaga,
            "area_nome": area.nome if area else "N/A",
            "qtd_candidaturas": qtd_candidaturas
        })

    return templates.TemplateResponse(
        "recrutador/vagas/listar.html",
        {"request": request, "vagas": vagas_enriquecidas}
    )


@router.get("/cadastrar")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de vaga"""
    areas = area_repo.obter_todas()

    return templates.TemplateResponse(
        "recrutador/vagas/cadastro.html",
        {"request": request, "areas": areas}
    )


@router.post("/cadastrar")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def post_cadastrar(
    request: Request,
    titulo: str = Form(...),
    descricao: str = Form(...),
    id_area: int = Form(...),
    numero_vagas: int = Form(1),
    salario: float = Form(0.0),
    requisitos: str = Form(""),
    beneficios: str = Form(""),
    carga_horaria: str = Form(""),
    modalidade: str = Form(""),
    cidade: str = Form(""),
    uf: str = Form(""),
    usuario_logado: Optional[dict] = None,
):
    """Cadastra uma nova vaga"""
    assert usuario_logado is not None

    dados_formulario = {
        "titulo": titulo,
        "descricao": descricao,
        "id_area": id_area,
        "numero_vagas": numero_vagas,
        "salario": salario,
        "requisitos": requisitos,
        "beneficios": beneficios,
        "carga_horaria": carga_horaria,
        "modalidade": modalidade,
        "cidade": cidade,
        "uf": uf,
    }

    try:
        # Validar com DTO
        dto = CriarVagaDTO(
            id_area=id_area,
            id_recrutador=usuario_logado["id"],
            titulo=titulo,
            descricao=descricao,
            numero_vagas=numero_vagas,
            salario=salario,
            requisitos=requisitos or None,
            beneficios=beneficios or None,
            carga_horaria=carga_horaria or None,
            modalidade=modalidade or None,
            cidade=cidade or None,
            uf=uf or None,
        )

        # Verificar se área existe
        area = area_repo.obter_por_id(dto.id_area)
        if not area:
            informar_erro(request, "Área selecionada não existe")
            areas = area_repo.obter_todas()
            return templates.TemplateResponse(
                "recrutador/vagas/cadastro.html",
                {"request": request, "areas": areas, "dados": dados_formulario},
            )

        # Criar vaga
        vaga = Vaga(
            id_vaga=0,
            id_area=dto.id_area,
            id_recrutador=dto.id_recrutador,
            status_vaga="aberta",
            titulo=dto.titulo,
            descricao=dto.descricao,
            numero_vagas=dto.numero_vagas,
            salario=dto.salario,
            requisitos=dto.requisitos,
            beneficios=dto.beneficios,
            carga_horaria=dto.carga_horaria,
            modalidade=dto.modalidade,
            cidade=dto.cidade,
            uf=dto.uf,
        )
        id_nova_vaga = vaga_repo.inserir(vaga)

        logger.info(f"Vaga '{dto.titulo}' (ID: {id_nova_vaga}) cadastrada por recrutador {usuario_logado['id']}")
        informar_sucesso(request, "Vaga cadastrada com sucesso!")

        return RedirectResponse(
            "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
        )

    except ValidationError as e:
        areas = area_repo.obter_todas()
        raise ErroValidacaoFormulario(
            validation_error=e,
            template_path="recrutador/vagas/cadastro.html",
            dados_formulario={**dados_formulario, "areas": areas},
            campo_padrao="titulo",
        )


@router.get("/editar/{id}")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def get_editar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exibe formulário de edição de vaga"""
    assert usuario_logado is not None

    vaga = vaga_repo.obter_por_id(id)

    if not vaga:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse(
            "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
        )

    # Verificar se a vaga pertence ao recrutador
    if vaga.id_recrutador != usuario_logado["id"]:
        informar_erro(request, "Você não tem permissão para editar esta vaga")
        return RedirectResponse(
            "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
        )

    areas = area_repo.obter_todas()

    dados_vaga = {
        "id_vaga": vaga.id_vaga,
        "titulo": vaga.titulo,
        "descricao": vaga.descricao,
        "id_area": vaga.id_area,
        "numero_vagas": vaga.numero_vagas,
        "salario": vaga.salario,
        "requisitos": vaga.requisitos or "",
        "beneficios": vaga.beneficios or "",
        "carga_horaria": vaga.carga_horaria or "",
        "modalidade": vaga.modalidade or "",
        "cidade": vaga.cidade or "",
        "uf": vaga.uf or "",
    }

    return templates.TemplateResponse(
        "recrutador/vagas/editar.html",
        {"request": request, "vaga": vaga, "areas": areas, "dados": dados_vaga}
    )


@router.post("/editar/{id}")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def post_editar(
    request: Request,
    id: int,
    titulo: str = Form(...),
    descricao: str = Form(...),
    id_area: int = Form(...),
    numero_vagas: int = Form(1),
    salario: float = Form(0.0),
    requisitos: str = Form(""),
    beneficios: str = Form(""),
    carga_horaria: str = Form(""),
    modalidade: str = Form(""),
    cidade: str = Form(""),
    uf: str = Form(""),
    usuario_logado: Optional[dict] = None,
):
    """Altera dados de uma vaga"""
    assert usuario_logado is not None

    vaga_atual = vaga_repo.obter_por_id(id)

    if not vaga_atual:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse(
            "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
        )

    # Verificar se a vaga pertence ao recrutador
    if vaga_atual.id_recrutador != usuario_logado["id"]:
        informar_erro(request, "Você não tem permissão para editar esta vaga")
        return RedirectResponse(
            "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
        )

    dados_formulario = {
        "id_vaga": id,
        "titulo": titulo,
        "descricao": descricao,
        "id_area": id_area,
        "numero_vagas": numero_vagas,
        "salario": salario,
        "requisitos": requisitos,
        "beneficios": beneficios,
        "carga_horaria": carga_horaria,
        "modalidade": modalidade,
        "cidade": cidade,
        "uf": uf,
    }

    try:
        # Validar com DTO
        dto = AlterarVagaDTO(
            id_vaga=id,
            id_area=id_area,
            titulo=titulo,
            descricao=descricao,
            numero_vagas=numero_vagas,
            salario=salario,
            requisitos=requisitos or None,
            beneficios=beneficios or None,
            carga_horaria=carga_horaria or None,
            modalidade=modalidade or None,
            cidade=cidade or None,
            uf=uf or None,
        )

        # Verificar se área existe
        area = area_repo.obter_por_id(dto.id_area)
        if not area:
            informar_erro(request, "Área selecionada não existe")
            areas = area_repo.obter_todas()
            return templates.TemplateResponse(
                "recrutador/vagas/editar.html",
                {"request": request, "vaga": vaga_atual, "areas": areas, "dados": dados_formulario},
            )

        # Atualizar vaga
        vaga_atualizada = Vaga(
            id_vaga=id,
            id_area=dto.id_area,
            id_recrutador=vaga_atual.id_recrutador,
            status_vaga=vaga_atual.status_vaga,
            titulo=dto.titulo,
            descricao=dto.descricao,
            numero_vagas=dto.numero_vagas,
            salario=dto.salario,
            requisitos=dto.requisitos,
            beneficios=dto.beneficios,
            carga_horaria=dto.carga_horaria,
            modalidade=dto.modalidade,
            cidade=dto.cidade,
            uf=dto.uf,
        )
        vaga_repo.alterar(vaga_atualizada)

        logger.info(f"Vaga {id} ('{dto.titulo}') alterada por recrutador {usuario_logado['id']}")
        informar_sucesso(request, "Vaga alterada com sucesso!")

        return RedirectResponse(
            "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
        )

    except ValidationError as e:
        areas = area_repo.obter_todas()
        raise ErroValidacaoFormulario(
            validation_error=e,
            template_path="recrutador/vagas/editar.html",
            dados_formulario={**dados_formulario, "vaga": vaga_atual, "areas": areas},
            campo_padrao="titulo",
        )


@router.post("/alterar-status/{id}")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def post_alterar_status(
    request: Request,
    id: int,
    novo_status: str = Form(...),
    usuario_logado: Optional[dict] = None,
):
    """Altera o status de uma vaga (abrir/fechar)"""
    assert usuario_logado is not None

    vaga = vaga_repo.obter_por_id(id)

    if not vaga:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse(
            "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
        )

    # Verificar se a vaga pertence ao recrutador
    if vaga.id_recrutador != usuario_logado["id"]:
        informar_erro(request, "Você não tem permissão para alterar esta vaga")
        return RedirectResponse(
            "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
        )

    # Validar status
    if novo_status not in ["aberta", "fechada"]:
        informar_erro(request, "Status inválido")
        return RedirectResponse(
            "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
        )

    sucesso = vaga_repo.atualizar_status(id, novo_status)

    if sucesso:
        status_texto = "aberta" if novo_status == "aberta" else "fechada"
        logger.info(f"Vaga {id} ('{vaga.titulo}') {status_texto} por recrutador {usuario_logado['id']}")
        informar_sucesso(request, f"Vaga {status_texto} com sucesso!")
    else:
        informar_erro(request, "Erro ao alterar status da vaga")

    return RedirectResponse(
        "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/excluir/{id}")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def post_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui uma vaga (somente se não tiver candidaturas)"""
    assert usuario_logado is not None

    vaga = vaga_repo.obter_por_id(id)

    if not vaga:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse(
            "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
        )

    # Verificar se a vaga pertence ao recrutador
    if vaga.id_recrutador != usuario_logado["id"]:
        informar_erro(request, "Você não tem permissão para excluir esta vaga")
        return RedirectResponse(
            "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
        )

    # Verificar se há candidaturas vinculadas
    quantidade_candidaturas = vaga_repo.contar_candidaturas(id)
    if quantidade_candidaturas > 0:
        informar_erro(
            request,
            f"Não é possível excluir esta vaga pois existem {quantidade_candidaturas} candidatura(s) vinculada(s). "
            f"Considere fechar a vaga ao invés de excluí-la."
        )
        return RedirectResponse(
            "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
        )

    vaga_repo.excluir(id)
    logger.info(f"Vaga {id} ('{vaga.titulo}') excluída por recrutador {usuario_logado['id']}")
    informar_sucesso(request, "Vaga excluída com sucesso!")

    return RedirectResponse(
        "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/{id}/candidatos")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def listar_candidatos(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Lista candidatos de uma vaga"""
    assert usuario_logado is not None

    vaga = vaga_repo.obter_por_id(id)

    if not vaga:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse(
            "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
        )

    # Verificar se a vaga pertence ao recrutador
    if vaga.id_recrutador != usuario_logado["id"]:
        informar_erro(request, "Você não tem permissão para ver candidatos desta vaga")
        return RedirectResponse(
            "/recrutador/vagas/listar", status_code=status.HTTP_303_SEE_OTHER
        )

    # Importar repo de candidatura localmente para evitar import circular
    from repo import candidatura_repo

    candidaturas = candidatura_repo.obter_por_vaga_com_candidato(id)

    return templates.TemplateResponse(
        "recrutador/vagas/candidatos.html",
        {"request": request, "vaga": vaga, "candidaturas": candidaturas}
    )
