from dataclasses import dataclass
from datetime import datetime


@dataclass
class Vaga:
    id_vaga: int
    id_area: int
    id_empresa: int
    id_recrutador: int
    status_vaga: str
    descricao: str
    numero_vagas: int
    salario: float
    data_cadastro: datetime