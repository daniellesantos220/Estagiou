from typing import Optional
from model.categoria_model import Categoria
from sql.categoria_sql import *
from util.db_util import get_connection


def _row_to_categoria(row) -> Categoria:
    """
    Converte uma linha do banco de dados em objeto Categoria.

    Args:
        row: Linha do cursor SQLite (sqlite3.Row)

    Returns:
        Objeto Categoria populado
    """
    return Categoria(
        id=row["id"],
        nome=row["nome"],
        descricao=row["descricao"] if "descricao" in row.keys() else None,
        data_cadastro=row["data_cadastro"] if "data_cadastro" in row.keys() else None,
        data_atualizacao=row["data_atualizacao"] if "data_atualizacao" in row.keys() else None,
    )


def criar_tabela() -> bool:
    """Cria a tabela de categorias no banco de dados."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True


def inserir(categoria: Categoria) -> Optional[int]:
    """
    Insere uma nova categoria no banco de dados.

    Args:
        categoria: Objeto Categoria com os dados a serem inseridos

    Returns:
        ID da categoria inserida ou None em caso de erro
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            INSERIR,
            (
                categoria.nome,
                categoria.descricao,
            ),
        )
        return cursor.lastrowid


def alterar(categoria: Categoria) -> bool:
    """
    Altera uma categoria existente no banco de dados.

    Args:
        categoria: Objeto Categoria com os dados atualizados

    Returns:
        True se a categoria foi alterada, False caso contrário
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            ALTERAR,
            (
                categoria.nome,
                categoria.descricao,
                categoria.id,
            ),
        )
        return cursor.rowcount > 0


def excluir(id: int) -> bool:
    """
    Exclui uma categoria do banco de dados.

    Args:
        id: ID da categoria a ser excluída

    Returns:
        True se a categoria foi excluída, False caso contrário
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0


def obter_por_id(id: int) -> Optional[Categoria]:
    """
    Obtém uma categoria pelo ID.

    Args:
        id: ID da categoria

    Returns:
        Objeto Categoria ou None se não encontrada
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return _row_to_categoria(row)
        return None


def obter_todos() -> list[Categoria]:
    """
    Obtém todas as categorias do banco de dados.

    Returns:
        Lista de objetos Categoria
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [_row_to_categoria(row) for row in rows]


def obter_quantidade() -> int:
    """
    Obtém a quantidade total de categorias.

    Returns:
        Número total de categorias
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0


def obter_por_nome(nome: str) -> Optional[Categoria]:
    """
    Obtém uma categoria pelo nome.

    Args:
        nome: Nome da categoria

    Returns:
        Objeto Categoria ou None se não encontrada
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_NOME, (nome,))
        row = cursor.fetchone()
        if row:
            return _row_to_categoria(row)
        return None
