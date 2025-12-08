from typing import Optional
from model.area_model import Area
from sql.area_sql import *
from util.db_util import obter_conexao


def criar_tabela() -> bool:
    """Cria a tabela de áreas se não existir."""
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True


def inserir(area: Area) -> Optional[int]:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (area.nome, area.descricao))
        return cursor.lastrowid


def alterar(area: Area) -> bool:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (area.nome, area.descricao, area.id_area))
        return cursor.rowcount > 0


def excluir(id_area: int) -> bool:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_area,))
        return cursor.rowcount > 0


def obter_por_id(id_area: int) -> Optional[Area]:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_area,))
        row = cursor.fetchone()
        if row:
            return Area(
                id_area=row["id_area"],
                nome=row["nome"],
                descricao=row["descricao"] if "descricao" in row.keys() else "",
            )
        return None


def obter_todas() -> list[Area]:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        rows = cursor.fetchall()
        return [
            Area(id_area=row["id_area"], nome=row["nome"], descricao=row["descricao"])
            for row in rows
        ]


def obter_por_nome(nome: str) -> Optional[Area]:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_NOME, (nome,))
        row = cursor.fetchone()
        if row:
            return Area(
                id_area=row["id_area"],
                nome=row["nome"],
                descricao=row["descricao"] if "descricao" in row.keys() else "",
            )
        return None


def obter_quantidade() -> int:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0


def obter_quantidade_vagas_por_area(id_area: int) -> int:
    """Retorna a quantidade de vagas associadas a uma área."""
    import sqlite3
    try:
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_QUANTIDADE_VAGAS_POR_AREA, (id_area,))
            row = cursor.fetchone()
            return row["quantidade"] if row else 0
    except sqlite3.OperationalError:
        # Tabela vaga não existe ainda
        return 0
