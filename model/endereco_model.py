from dataclasses import dataclass
from typing import Optional

from model.usuario_model import Usuario


@dataclass
class Endereco:
    id_endereco: int
    id_usuario: int
    titulo: str
    logradouro: str
    numero: str
    bairro: str
    cidade: str
    uf: str
    cep: str
    complemento: Optional[str] = None

    usuario: Optional[Usuario] = None