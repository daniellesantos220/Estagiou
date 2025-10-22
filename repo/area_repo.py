from typing import Optional
from model.area_model import Area
from sql.area_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    """Cria a tabela de áreas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(area: Area) -> Optional[int]:
    """Insere uma nova área."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (area.nome, area.descricao))
        return cursor.lastrowid

def alterar(area: Area) -> bool:
    """Altera uma área existente."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (area.nome, area.descricao, area.id_area))
        return cursor.rowcount > 0

def excluir(id_area: int) -> bool:
    """Exclui uma área."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_area,))
        return cursor.rowcount > 0

def obter_por_id(id_area: int) -> Optional[Area]:
    """Obtém uma área por ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_area,))
        row = cursor.fetchone()
        if row:
            return Area(
                id_area=row["id_area"],
                nome=row["nome"],
                descricao=row["descricao"]
            )
        return None

def obter_todas() -> list[Area]:
    """Obtém todas as áreas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        rows = cursor.fetchall()
        return [
            Area(
                id_area=row["id_area"],
                nome=row["nome"],
                descricao=row["descricao"]
            )
            for row in rows
        ]

def obter_por_nome(nome: str) -> Optional[Area]:
    """Obtém uma área por nome."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_NOME, (nome,))
        row = cursor.fetchone()
        if row:
            return Area(
                id_area=row["id_area"],
                nome=row["nome"],
                descricao=row["descricao"]
            )
        return None

def obter_quantidade() -> int:
    """Obtém a quantidade total de áreas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def verificar_uso(id_area: int) -> int:
    """Verifica quantas vagas estão usando esta área."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(VERIFICAR_USO, (id_area,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0