from pydantic import BaseModel, field_validator
from dtos.validators import validar_id_positivo

class CriarCandidaturaDTO(BaseModel):
    """DTO para criação de candidatura."""
    id_vaga: int
    id_candidato: int

    _validar_id_vaga = field_validator("id_vaga")(validar_id_positivo())
    _validar_id_candidato = field_validator("id_candidato")(validar_id_positivo())

class AlterarStatusCandidaturaDTO(BaseModel):
    """DTO para alteração de status de candidatura."""
    id_candidatura: int
    status: str

    _validar_id = field_validator("id_candidatura")(validar_id_positivo())

    @field_validator("status")
    @classmethod
    def validar_status(cls, v: str) -> str:
        status_validos = ["pendente", "em_analise", "aprovado", "rejeitado", "cancelado"]
        if v not in status_validos:
            raise ValueError(f"Status deve ser um de: {', '.join(status_validos)}")
        return v