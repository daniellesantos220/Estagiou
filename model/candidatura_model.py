from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from model.usuario_model import Usuario
from model.vaga_model import Vaga


@dataclass
class Candidatura:
    id_candidatura: int
    id_vaga: int
    id_candidato: int
    data_candidatura: datetime
    Status: str

#Relacionamentos
    vaga: Optional[Vaga]
    candidato: Optional[Usuario]