from dataclasses import dataclass
from typing import Optional

@dataclass
class Avaliacao:
    """
    Model de avaliação de empresa por estudante.

    Attributes:
        id_avaliacao: Identificador único
        id_empresa: FK para Empresa
        id_estudante: FK para Usuario
        nota: Nota de 1 a 5
        comentario: Comentário opcional
        data_avaliacao: Data da avaliação

        # Relacionamentos
        empresa: Objeto Empresa (opcional)
        estudante: Objeto Usuario (opcional)
    """
    id_avaliacao: int
    id_empresa: int
    id_estudante: int
    nota: int
    comentario: str
    data_avaliacao: str

    empresa: Optional[object] = None
    estudante: Optional[object] = None