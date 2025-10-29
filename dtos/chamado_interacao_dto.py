from pydantic import BaseModel, field_validator
from dtos.validators import validar_string_obrigatoria, validar_id_positivo


class CriarInteracaoDTO(BaseModel):
    """DTO para criar uma nova interação em um chamado."""
    mensagem: str

    _validar_mensagem = field_validator("mensagem")(
        validar_string_obrigatoria(
            nome_campo="Mensagem",
            tamanho_minimo=10,
            tamanho_maximo=2000
        )
    )


class AlterarInteracaoDTO(BaseModel):
    """DTO para alterar uma interação existente."""
    id: int
    mensagem: str

    _validar_id = field_validator("id")(validar_id_positivo("ID"))
    _validar_mensagem = field_validator("mensagem")(
        validar_string_obrigatoria(
            nome_campo="Mensagem",
            tamanho_minimo=10,
            tamanho_maximo=2000
        )
    )
