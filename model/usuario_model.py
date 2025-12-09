from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    senha: str
    perfil: str
    data_nascimento: Optional[date] = None
    numero_documento: Optional[str] = None
    telefone: Optional[str] = None
    confirmado: bool = False
    token_redefinicao: Optional[str] = None
    data_token: Optional[datetime] = None
    data_cadastro: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
