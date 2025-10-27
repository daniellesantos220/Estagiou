from typing import Optional
from model.area_model import Area
from sql.area_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    """Cria a tabela de áreas se não existir."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(area: Area) -> Optional[int]:
    """
    Insere uma nova área no banco de dados.

    Args:
        area: Objeto Area com os dados a inserir

    Returns:
        ID da área inserida ou None em caso de erro
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            area.nome,
            area.descricao
        ))
        return cursor.lastrowid

def alterar(area: Area) -> bool:
    """
    Atualiza uma área existente.

    Args:
        area: Objeto Area com os dados atualizados

    Returns:
        True se a atualização foi bem-sucedida, False caso contrário
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            area.nome,
            area.descricao,
            area.id_area
        ))
        return cursor.rowcount > 0

def excluir(id_area: int) -> bool:
    """
    Exclui uma área do banco de dados.

    Args:
        id_area: ID da área a excluir

    Returns:
        True se a exclusão foi bem-sucedida, False caso contrário
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_area,))
        return cursor.rowcount > 0

def obter_por_id(id_area: int) -> Optional[Area]:
    """
    Busca uma área pelo ID.

    Args:
        id_area: ID da área

    Returns:
        Objeto Area ou None se não encontrado
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_area,))
        row = cursor.fetchone()
        if row:
            return Area(
                id_area=row["id_area"],
                nome=row["nome"],
                descricao=row["descricao"] if "descricao" in row.keys() else ""
            )
        return None

def obter_todas() -> list[Area]:
    """
    Retorna todas as áreas cadastradas.

    Returns:
        Lista de objetos Area
    """
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
    """
    Busca uma área pelo nome.

    Args:
        nome: Nome da área

    Returns:
        Objeto Area ou None se não encontrado
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_NOME, (nome,))
        row = cursor.fetchone()
        if row:
            return Area(
                id_area=row["id_area"],
                nome=row["nome"],
                descricao=row["descricao"] if "descricao" in row.keys() else ""
            )
        return None

def obter_quantidade() -> int:
    """
    Retorna a quantidade total de áreas cadastradas.

    Returns:
        Número de áreas
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def verificar_uso(id_area: int) -> int:
    """
    Verifica quantas vagas estão usando esta área.

    Args:
        id_area: ID da área

    Returns:
        Número de vagas associadas a esta área
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(VERIFICAR_USO, (id_area,))
            row = cursor.fetchone()
            return row["quantidade"] if row else 0
    except Exception:
        # Se a tabela vaga não existir, retorna 0
        return 0
