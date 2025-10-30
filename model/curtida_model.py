from dataclasses import dataclass
from datetime import datetime

@dataclass

class Curtida:
    id: int
    usuario_id: int
    id_vaga: int
    data_curtida: datetime
    