from pydantic import BaseModel, field_validator
from typing import Optional
from dtos.validators import validar_id_positivo, validar_nome_generico

class CriarVagaDTO(BaseModel):
    """DTO para criação de vaga."""
    id_area: int
    id_empresa: int
    id_recrutador: int
    titulo: str
    descricao: str
    numero_vagas: int = 1
    salario: float = 0.0
    requisitos: Optional[str] = None
    beneficios: Optional[str] = None
    carga_horaria: Optional[int] = None
    modalidade: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None

    _validar_id_area = field_validator("id_area")(validar_id_positivo())
    _validar_id_empresa = field_validator("id_empresa")(validar_id_positivo())
    _validar_id_recrutador = field_validator("id_recrutador")(validar_id_positivo())
    _validar_titulo = field_validator("titulo")(validar_nome_generico(min_length=5, max_length=200))

    @field_validator("numero_vagas")
    @classmethod
    def validar_numero_vagas(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Número de vagas deve ser pelo menos 1")
        if v > 100:
            raise ValueError("Número de vagas não pode exceder 100")
        return v

    @field_validator("salario")
    @classmethod
    def validar_salario(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Salário não pode ser negativo")
        return v

    @field_validator("modalidade")
    @classmethod
    def validar_modalidade(cls, v: Optional[str]) -> Optional[str]:
        if v and v not in ["Presencial", "Remoto", "Híbrido"]:
            raise ValueError("Modalidade deve ser: Presencial, Remoto ou Híbrido")
        return v

class AlterarVagaDTO(BaseModel):
    """DTO para alteração de vaga."""
    id_vaga: int
    id_area: int
    titulo: str
    descricao: str
    numero_vagas: int
    salario: float
    requisitos: Optional[str]
    beneficios: Optional[str]
    carga_horaria: Optional[int]
    modalidade: Optional[str]
    cidade: Optional[str]
    uf: Optional[str]

    _validar_id_vaga = field_validator("id_vaga")(validar_id_positivo())
    _validar_id_area = field_validator("id_area")(validar_id_positivo())
    _validar_titulo = field_validator("titulo")(validar_nome_generico(min_length=5, max_length=200))

class BuscarVagasDTO(BaseModel):
    """DTO para busca de vagas com filtros."""
    id_area: Optional[int] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    modalidade: Optional[str] = None
    salario_minimo: Optional[float] = None
    limite: int = 50
    offset: int = 0