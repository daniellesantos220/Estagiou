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
    data_cadastro: str

    
    titulo: Optional[str] = None
    requisitos: Optional[str] = None
    beneficios: Optional[str] = None
    carga_horaria: Optional[int] = None
    modalidade: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None

    
    area: Optional[object] = None  
    empresa: Optional[object] = None  
    recrutador: Optional[object] = None  