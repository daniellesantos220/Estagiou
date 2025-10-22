from typing import Optional
from model.mensagem_model import Mensagem
from sql.mensagem_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(mensagem: Mensagem) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            mensagem.id_remetente,
            mensagem.id_destinatario,
            mensagem.assunto,
            mensagem.conteudo
        ))
        return cursor.lastrowid

def marcar_como_lida(id_mensagem: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(MARCAR_COMO_LIDA, (id_mensagem,))
        return cursor.rowcount > 0

def obter_recebidas(id_destinatario: int) -> list[Mensagem]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_RECEBIDAS, (id_destinatario,))
        rows = cursor.fetchall()
        return [
            Mensagem(
                id_mensagem=row["id_mensagem"],
                id_remetente=row["id_remetente"],
                id_destinatario=row["id_destinatario"],
                assunto=row["assunto"],
                conteudo=row["conteudo"],
                lida=bool(row["lida"]),
                data_envio=row["data_envio"]
            )
            for row in rows
        ]

def contar_nao_lidas(id_destinatario: int) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONTAR_NAO_LIDAS, (id_destinatario,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0