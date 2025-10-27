from dataclasses import dataclass
from typing import Optional

from model.empresa_model import Empresa
from model.usuario_model import Usuario

@dataclass
class Avaliacao:
    id_avaliacao: int
    id_empresa: int
    id_estudante: int
    nota: int
    comentario: str
    data_avaliacao: str

    empresa: Optional[Empresa] = None
    estudante: Optional[Usuario] = None