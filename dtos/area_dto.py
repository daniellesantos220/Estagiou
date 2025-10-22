from pydantic import BaseModel, field_validator
from dtos.validators import validar_nome_generico, validar_id_positivo

class CriarAreaDTO(BaseModel):
    """DTO para criação de área."""
    nome: str
    descricao: str

    _validar_nome = field_validator("nome")(validar_nome_generico(min_length=3, max_length=100))

class AlterarAreaDTO(BaseModel):
    """DTO para alteração de área."""
    id_area: int
    nome: str
    descricao: str

    _validar_id = field_validator("id_area")(validar_id_positivo())
    _validar_nome = field_validator("nome")(validar_nome_generico(min_length=3, max_length=100))