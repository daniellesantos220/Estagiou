from typing import Optional
from model.notificacao_model import Notificacao
from sql.notificacao_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(notificacao: Notificacao) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            notificacao.id_usuario,
            notificacao.tipo,
            notificacao.titulo,
            notificacao.mensagem,
            notificacao.link
        ))
        return cursor.lastrowid

def criar_notificacao(id_usuario: int, tipo: str, titulo: str, mensagem: str, link: str = "") -> Optional[int]:
    """Helper para criar notificação facilmente."""
    notificacao = Notificacao(
        id_notificacao=0,
        id_usuario=id_usuario,
        tipo=tipo,
        titulo=titulo,
        mensagem=mensagem,
        lida=False,
        data_criacao="",
        link=link
    )
    return inserir(notificacao)

def obter_nao_lidas(id_usuario: int) -> list[Notificacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_NAO_LIDAS, (id_usuario,))
        rows = cursor.fetchall()
        return [
            Notificacao(
                id_notificacao=row["id_notificacao"],
                id_usuario=row["id_usuario"],
                tipo=row["tipo"],
                titulo=row["titulo"],
                mensagem=row["mensagem"],
                lida=bool(row["lida"]),
                data_criacao=row["data_criacao"],
                link=row.get("link", "")
            )
            for row in rows
        ]

def contar_nao_lidas(id_usuario: int) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONTAR_NAO_LIDAS, (id_usuario,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def marcar_como_lida(id_notificacao: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(MARCAR_COMO_LIDA, (id_notificacao,))
        return cursor.rowcount > 0