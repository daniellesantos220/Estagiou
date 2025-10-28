from dataclasses import dataclass
from enum import Enum
from typing import Optional


class StatusVaga(Enum):
    ABERTA = "aberta"
    FECHADA = "fechada"
    SUSPENSA = "suspensa"

@dataclass
class Vaga:
    # Campos obrigatórios (sem valores padrão)
    id_vaga: int
    id_area: int
    id_empresa: int
    id_recrutador: int
    status_vaga: str  # Aceita string diretamente (ex: "aberta", "fechada", "suspensa")
    descricao: str
    titulo: str
    numero_vagas: int
    salario: float

    # Campos opcionais (com valores padrão)
    data_cadastro: Optional[str] = None  # Preenchido automaticamente pelo banco
    requisitos: Optional[str] = None
    beneficios: Optional[str] = None
    carga_horaria: Optional[str] = None  # Mudado para str (ex: "40h/semana", "6h/dia")
    modalidade: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None

    # Relacionamentos
    area: Optional[object] = None
    empresa: Optional[object] = None
    recrutador: Optional[object] = None