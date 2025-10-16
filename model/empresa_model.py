from dataclasses import dataclass


@dataclass
class Empresa:
    id_empresa: int
    nome: str
    cnpj: int
    descricao: str