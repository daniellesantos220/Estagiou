from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Categoria:
    id: int
    nome: str
    descricao: Optional[str] = None
    data_cadastro: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
