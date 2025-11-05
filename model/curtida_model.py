from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass

class Curtida:
    id_usuario: int
    id_vaga: int
    data_curtida: Optional[datetime] = None
    