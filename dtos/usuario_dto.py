from typing import Optional
from pydantic import BaseModel, Field, field_validator
from util.perfis import Perfil
from dtos.validators import (
    validar_email,
    validar_senha_forte,
    validar_nome_pessoa,
    validar_id_positivo,
    validar_tipo,
    validar_data_nascimento,
    validar_cpf_simples,
    validar_telefone_br,
)


class CriarUsuarioDTO(BaseModel):
    """DTO para criação de usuário pelo administrador."""

    nome: str = Field(..., description="Nome completo do usuário")
    data_nascimento: str = Field(..., description="Data de nascimento")
    email: str = Field(..., description="E-mail do usuário")
    numero_documento: str = Field(..., description="CPF do usuário")
    telefone: str = Field(..., description="Telefone do usuário")
    senha: str = Field(..., description="Senha do usuário")
    perfil: str = Field(..., description="Perfil/Role do usuário")
    confirmado: bool = Field(default=False, description="Usuário confirmado")

    _validar_nome = field_validator("nome")(validar_nome_pessoa())
    _validar_data_nascimento = field_validator("data_nascimento")(validar_data_nascimento())
    _validar_email = field_validator("email")(validar_email())
    _validar_cpf = field_validator("numero_documento")(validar_cpf_simples())
    _validar_telefone = field_validator("telefone")(validar_telefone_br())
    _validar_senha = field_validator("senha")(validar_senha_forte())
    _validar_perfil = field_validator("perfil")(validar_tipo("Perfil", Perfil))


class AlterarUsuarioDTO(BaseModel):
    """DTO para alteração de usuário pelo administrador."""

    id: int = Field(..., description="ID do usuário a ser alterado")
    nome: str = Field(..., description="Nome completo do usuário")
    data_nascimento: str = Field(..., description="Data de nascimento")
    email: str = Field(..., description="E-mail do usuário")
    numero_documento: str = Field(..., description="CPF do usuário")
    telefone: str = Field(..., description="Telefone do usuário")
    perfil: str = Field(..., description="Perfil/Role do usuário")
    confirmado: bool = Field(default=False, description="Usuário confirmado")

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_nome = field_validator("nome")(validar_nome_pessoa())
    _validar_data_nascimento = field_validator("data_nascimento")(validar_data_nascimento())
    _validar_email = field_validator("email")(validar_email())
    _validar_cpf = field_validator("numero_documento")(validar_cpf_simples())
    _validar_telefone = field_validator("telefone")(validar_telefone_br())
    _validar_perfil = field_validator("perfil")(validar_tipo("Perfil", Perfil))
