from pydantic import BaseModel, field_validator
from dtos.validators import validar_texto_obrigatorio

class ReprovarVagaDTO(BaseModel):
    """DTO para reprovação de vaga pelo administrador."""
    motivo: str

    _validar_motivo = field_validator("motivo")(validar_texto_obrigatorio(min_length=10, max_length=500))

def validar_texto_obrigatorio(min_length: int = 1, max_length: int = 1000):
    """Validador para campos de texto obrigatórios."""
    def validador(v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Este campo é obrigatório")
        if len(v) < min_length:
            raise ValueError(f"Deve ter no mínimo {min_length} caracteres")
        if len(v) > max_length:
            raise ValueError(f"Deve ter no máximo {max_length} caracteres")
        return v.strip()
    return validador