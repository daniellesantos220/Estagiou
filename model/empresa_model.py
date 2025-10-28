from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Empresa:
    id_empresa: int
    nome: str
    cnpj: str 
    descricao: str
    data_cadastro: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None