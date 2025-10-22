from dataclasses import dataclass


@dataclass
class Area:
    """
    Model de área de atuação no sistema Estagiou.

    Attributes:
        id_area: Identificador único da área
        nome: Nome da área (ex: Desenvolvimento, Design, Marketing, Recursos Humanos)
        descricao: Descrição detalhada da área de atuação
    """
    id_area: int
    nome: str
    descricao: str
    