from dataclasses import dataclass

from typing import Optional


@dataclass
class Candidatura:
    """
    Model de candidatura a uma vaga no sistema Estagiou.

    Attributes:
        id_candidatura: Identificador único da candidatura
        id_vaga: FK para Vaga
        id_candidato: FK para Usuario (estudante que se candidatou)
        data_candidatura: Data da candidatura
        status: Status da candidatura (pendente, em_analise, aprovado, rejeitado, cancelado)

        # Relacionamentos (populados via JOIN)
        vaga: Objeto Vaga (opcional)
        candidato: Objeto Usuario (opcional)
    """
    id_candidatura: int
    id_vaga: int
    id_candidato: int
    data_candidatura: str
    status: str

    # Relacionamentos
    vaga: Optional[object] = None 
    candidato: Optional[object] = None