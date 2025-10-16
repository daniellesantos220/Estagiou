from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from model.area_model import Area
from model.empresa_model import Empresa
from model.usuario_model import Usuario


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

    area: Optional[Area]
    empresa: Optional[Empresa]
    recrutador: Optional[Usuario]