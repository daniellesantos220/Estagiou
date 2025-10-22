from dataclasses import dataclass

@dataclass
class Notificacao:
    """
    Model de notificação para usuários.

    Attributes:
        id_notificacao: Identificador único
        id_usuario: FK para Usuario
        tipo: Tipo da notificação (nova_vaga, candidatura_atualizada, mensagem_recebida, etc.)
        titulo: Título da notificação
        mensagem: Mensagem da notificação
        lida: Se foi lida
        data_criacao: Data/hora de criação
        link: Link relacionado (opcional)
    """
    id_notificacao: int
    id_usuario: int
    tipo: str
    titulo: str
    mensagem: str
    lida: bool
    data_criacao: str
    link: str = ""