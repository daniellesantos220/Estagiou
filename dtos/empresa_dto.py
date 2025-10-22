from pydantic import BaseModel, field_validator
from dtos.validators import validar_cnpj, validar_nome_generico, validar_id_positivo

class CriarEmpresaDTO(BaseModel):
    """DTO para criação de empresa."""
    nome: str
    cnpj: str
    descricao: str

    _validar_nome = field_validator("nome")(validar_nome_generico(min_length=3, max_length=200))
    _validar_cnpj = field_validator("cnpj")(validar_cnpj())

class AlterarEmpresaDTO(BaseModel):
    """DTO para alteração de empresa."""
    id_empresa: int
    nome: str
    cnpj: str
    descricao: str

    _validar_id = field_validator("id_empresa")(validar_id_positivo())
    _validar_nome = field_validator("nome")(validar_nome_generico(min_length=3, max_length=200))
    _validar_cnpj = field_validator("cnpj")(validar_cnpj())