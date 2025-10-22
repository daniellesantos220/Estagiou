from typing import Optional, Tuple
from model.avaliacao_model import Avaliacao
from sql.avaliacao_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(avaliacao: Avaliacao) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            avaliacao.id_empresa,
            avaliacao.id_estudante,
            avaliacao.nota,
            avaliacao.comentario
        ))
        return cursor.lastrowid

def obter_por_empresa(id_empresa: int) -> list[Avaliacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_EMPRESA, (id_empresa,))
        rows = cursor.fetchall()
        return [
            Avaliacao(
                id_avaliacao=row["id_avaliacao"],
                id_empresa=row["id_empresa"],
                id_estudante=row["id_estudante"],
                nota=row["nota"],
                comentario=row["comentario"],
                data_avaliacao=row["data_avaliacao"]
            )
            for row in rows
        ]

def obter_media_empresa(id_empresa: int) -> Tuple[float, int]:
    """Retorna (média, total de avaliações)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_MEDIA_EMPRESA, (id_empresa,))
        row = cursor.fetchone()
        if row and row["total"] > 0:
            return (round(row["media"], 1), row["total"])
        return (0.0, 0)

def verificar_avaliacao_existente(id_empresa: int, id_estudante: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(VERIFICAR_AVALIACAO_EXISTENTE, (id_empresa, id_estudante))
        return cursor.fetchone() is not None