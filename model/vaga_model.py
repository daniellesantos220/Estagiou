from dataclasses import dataclass
from enum import Enum
from typing import Optional


class StatusVaga(Enum):
    ABERTA = "aberta"
    FECHADA = "fechada"
    SUSPENSA = "suspensa"

@dataclass
class Vaga:
    id_vaga: int
    id_area: int
    id_empresa: int
    id_recrutador: int
    status_vaga: StatusVaga
    descricao: str
    numero_vagas: int
    salario: float
    data_cadastro: str

    # Campos adicionais
    titulo: Optional[str] = None
    requisitos: Optional[str] = None
    beneficios: Optional[str] = None
    carga_horaria: Optional[int] = None
    modalidade: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None

    # Relacionamentos
    area: Optional[object] = None
    empresa: Optional[object] = None
    recrutador: Optional[object] = None