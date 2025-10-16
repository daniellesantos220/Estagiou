from dataclasses import dataclass
from datetime import datetime


@dataclass
class Candidatura:
    id_candidatura: int
    id_vaga: int
    id_candidato: int
    data_candidatura: datetime
    Status: str