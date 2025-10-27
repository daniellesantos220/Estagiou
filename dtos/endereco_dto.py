from pydantic import BaseModel, field_validator
from dtos.validators import validar_id_positivo, validar_cep, validar_uf

class CriarEnderecoDTO(BaseModel):
    """DTO para criação de endereço."""
    id_usuario: int
    titulo: str
    logradouro: str
    numero: str
    complemento: str = ""
    bairro: str
    cidade: str
    uf: str
    cep: str

    _validar_id_usuario = field_validator("id_usuario")(validar_id_positivo())
    _validar_uf = field_validator("uf")(validar_uf())
    _validar_cep = field_validator("cep")(validar_cep())

class AlterarEnderecoDTO(BaseModel):
    """DTO para alteração de endereço."""
    id_endereco: int
    titulo: str
    logradouro: str
    numero: str
    complemento: str
    bairro: str
    cidade: str
    uf: str
    cep: str

    _validar_id = field_validator("id_endereco")(validar_id_positivo())
    _validar_uf = field_validator("uf")(validar_uf())
    _validar_cep = field_validator("cep")(validar_cep())