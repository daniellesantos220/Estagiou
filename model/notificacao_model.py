from dataclasses import dataclass

@dataclass
class Notificacao:
    id_notificacao: int
    id_usuario: int
    tipo: str
    titulo: str
    mensagem: str
    lida: bool
    data_criacao: str
    link: str = ""