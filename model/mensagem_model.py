from dataclasses import dataclass
from typing import Optional

@dataclass
class Mensagem:
    """
    Model de mensagem entre usuários.

    Attributes:
        id_mensagem: Identificador único
        id_remetente: FK para Usuario (quem enviou)
        id_destinatario: FK para Usuario (quem recebe)
        assunto: Assunto da mensagem
        conteudo: Corpo da mensagem
        lida: Se a mensagem foi lida
        data_envio: Data/hora de envio

        # Relacionamentos
        remetente: Objeto Usuario (opcional)
        destinatario: Objeto Usuario (opcional)
    """
    id_mensagem: int
    id_remetente: int
    id_destinatario: int
    assunto: str
    conteudo: str
    lida: bool
    data_envio: str

    # Relacionamentos
    remetente: Optional[object] = None
    destinatario: Optional[object] = None