from dataclasses import dataclass
from typing import Optional

@dataclass
class Empresa:
    """
    Model de empresa no sistema Estagiou.

    Attributes:
        id_empresa: Identificador único da empresa
        nome: Nome da empresa
        cnpj: CNPJ da empresa (string para preservar formatação)
        descricao: Descrição da empresa
        data_cadastro: Data de cadastro da empresa (opcional)
    """
    id_empresa: int
    nome: str
    cnpj: str
    descricao: str
    data_cadastro: Optional[str] = None