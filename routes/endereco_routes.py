"""Rotas de gerenciamento de endereço do usuário."""
from typing import Optional
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError, BaseModel, field_validator

from model.endereco_model import Endereco
from repo import endereco_repo
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.logger_config import logger
from util.perfis import Perfil
from util.exceptions import ErroValidacaoFormulario


# DTO para validação de endereço
class EnderecoDTO(BaseModel):
    """DTO para criar/alterar endereço."""
    logradouro: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    uf: str
    cep: str

    @field_validator("logradouro")
    @classmethod
    def validar_logradouro(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Logradouro é obrigatório")
        valor = v.strip()
        if len(valor) < 3:
            raise ValueError("Logradouro deve ter no mínimo 3 caracteres")
        if len(valor) > 200:
            raise ValueError("Logradouro deve ter no máximo 200 caracteres")
        return valor

    @field_validator("numero")
    @classmethod
    def validar_numero(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Número é obrigatório")
        return v.strip()

    @field_validator("bairro")
    @classmethod
    def validar_bairro(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Bairro é obrigatório")
        valor = v.strip()
        if len(valor) < 2:
            raise ValueError("Bairro deve ter no mínimo 2 caracteres")
        return valor

    @field_validator("cidade")
    @classmethod
    def validar_cidade(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Cidade é obrigatória")
        valor = v.strip()
        if len(valor) < 2:
            raise ValueError("Cidade deve ter no mínimo 2 caracteres")
        return valor

    @field_validator("uf")
    @classmethod
    def validar_uf(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Estado (UF) é obrigatório")
        valor = v.strip().upper()
        ufs_validas = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
                       "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
                       "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
        if valor not in ufs_validas:
            raise ValueError("Estado (UF) inválido")
        return valor

    @field_validator("cep")
    @classmethod
    def validar_cep(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("CEP é obrigatório")
        # Remove caracteres não numéricos
        cep_limpo = "".join(filter(str.isdigit, v))
        if len(cep_limpo) != 8:
            raise ValueError("CEP deve conter 8 dígitos")
        return cep_limpo


router = APIRouter(prefix="/usuario/endereco")
templates = criar_templates()


@router.get("/")
@requer_autenticacao([Perfil.ADMIN.value, Perfil.ESTUDANTE.value, Perfil.RECRUTADOR.value])
async def get_endereco(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de endereço do usuário (único endereço por usuário)"""
    assert usuario_logado is not None

    # Buscar endereço do usuário (apenas 1 por regra de negócio)
    enderecos = endereco_repo.obter_por_usuario(usuario_logado["id"])
    endereco = enderecos[0] if enderecos else None

    dados = {}
    if endereco:
        dados = {
            "id_endereco": endereco.id_endereco,
            "logradouro": endereco.logradouro,
            "numero": endereco.numero,
            "complemento": endereco.complemento or "",
            "bairro": endereco.bairro,
            "cidade": endereco.cidade,
            "uf": endereco.uf,
            "cep": endereco.cep,
        }

    return templates.TemplateResponse(
        "usuario/endereco.html",
        {"request": request, "endereco": endereco, "dados": dados}
    )


@router.post("/")
@requer_autenticacao([Perfil.ADMIN.value, Perfil.ESTUDANTE.value, Perfil.RECRUTADOR.value])
async def post_endereco(
    request: Request,
    logradouro: str = Form(...),
    numero: str = Form(...),
    complemento: str = Form(""),
    bairro: str = Form(...),
    cidade: str = Form(...),
    uf: str = Form(...),
    cep: str = Form(...),
    usuario_logado: Optional[dict] = None,
):
    """Cria ou atualiza endereço do usuário"""
    assert usuario_logado is not None

    dados_formulario = {
        "logradouro": logradouro,
        "numero": numero,
        "complemento": complemento,
        "bairro": bairro,
        "cidade": cidade,
        "uf": uf,
        "cep": cep,
    }

    try:
        # Validar dados
        dto = EnderecoDTO(
            logradouro=logradouro,
            numero=numero,
            complemento=complemento or None,
            bairro=bairro,
            cidade=cidade,
            uf=uf,
            cep=cep,
        )

        # Buscar endereço existente do usuário
        enderecos = endereco_repo.obter_por_usuario(usuario_logado["id"])
        endereco_existente = enderecos[0] if enderecos else None

        if endereco_existente:
            # Atualizar endereço existente
            endereco_atualizado = Endereco(
                id_endereco=endereco_existente.id_endereco,
                id_usuario=usuario_logado["id"],
                titulo="Principal",
                logradouro=dto.logradouro,
                numero=dto.numero,
                complemento=dto.complemento,
                bairro=dto.bairro,
                cidade=dto.cidade,
                uf=dto.uf,
                cep=dto.cep,
            )
            endereco_repo.alterar(endereco_atualizado)
            logger.info(f"Endereço {endereco_existente.id_endereco} atualizado pelo usuário {usuario_logado['id']}")
            informar_sucesso(request, "Endereço atualizado com sucesso!")
        else:
            # Criar novo endereço
            novo_endereco = Endereco(
                id_endereco=0,
                id_usuario=usuario_logado["id"],
                titulo="Principal",
                logradouro=dto.logradouro,
                numero=dto.numero,
                complemento=dto.complemento,
                bairro=dto.bairro,
                cidade=dto.cidade,
                uf=dto.uf,
                cep=dto.cep,
            )
            id_novo = endereco_repo.inserir(novo_endereco)
            logger.info(f"Endereço {id_novo} criado para o usuário {usuario_logado['id']}")
            informar_sucesso(request, "Endereço cadastrado com sucesso!")

        return RedirectResponse(
            "/usuario/endereco", status_code=status.HTTP_303_SEE_OTHER
        )

    except ValidationError as e:
        # Buscar endereço para reexibir no template
        enderecos = endereco_repo.obter_por_usuario(usuario_logado["id"])
        endereco_existente = enderecos[0] if enderecos else None

        raise ErroValidacaoFormulario(
            validation_error=e,
            template_path="usuario/endereco.html",
            dados_formulario={**dados_formulario, "endereco": endereco_existente},
            campo_padrao="logradouro",
        )
