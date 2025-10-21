from dataclasses import dataclass


@dataclass
class Empresa:
    """
    Model de empresa no sistema Estagiou.

    Attributes:
        id_empresa: Identificador único da empresa
        nome: Nome da empresa
        cnpj: CNPJ da empresa (string para preservar formatação)
        descricao: Descrição da empresa
    """
    id_empresa: int
    nome: str
    cnpj: str  # Alterado de int para str
    descricao: str