from typing import Optional
from model.candidatura_model import Candidatura
from sql.candidatura_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    """Cria a tabela de candidaturas se não existir."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(candidatura: Candidatura) -> Optional[int]:
    """
    Insere uma nova candidatura no banco de dados.

    Args:
        candidatura: Objeto Candidatura com os dados a inserir

    Returns:
        ID da candidatura inserida ou None em caso de erro
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            candidatura.id_vaga,
            candidatura.id_candidato
        ))
        return cursor.lastrowid

def alterar_status(id_candidatura: int, status: str) -> bool:
    """
    Atualiza o status de uma candidatura.

    Args:
        id_candidatura: ID da candidatura
        status: Novo status (pendente, em_analise, aprovado, rejeitado, cancelado)

    Returns:
        True se a atualização foi bem-sucedida, False caso contrário
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR_STATUS, (status, id_candidatura))
        return cursor.rowcount > 0

def excluir(id_candidatura: int) -> bool:
    """
    Exclui uma candidatura do banco de dados.

    Args:
        id_candidatura: ID da candidatura a excluir

    Returns:
        True se a exclusão foi bem-sucedida, False caso contrário
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_candidatura,))
        return cursor.rowcount > 0

def obter_por_id(id_candidatura: int) -> Optional[Candidatura]:
    """
    Busca uma candidatura pelo ID com dados relacionados.

    Args:
        id_candidatura: ID da candidatura

    Returns:
        Objeto Candidatura ou None se não encontrado
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_candidatura,))
        row = cursor.fetchone()
        if row:
            return Candidatura(
                id_candidatura=row["id_candidatura"],
                id_vaga=row["id_vaga"],
                id_candidato=row["id_candidato"],
                data_candidatura=row["data_candidatura"],
                status=row["status"]
            )
        return None

def obter_por_vaga(id_vaga: int) -> list[Candidatura]:
    """
    Retorna todas as candidaturas de uma vaga.

    Args:
        id_vaga: ID da vaga

    Returns:
        Lista de objetos Candidatura
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_VAGA, (id_vaga,))
        rows = cursor.fetchall()
        return [
            Candidatura(
                id_candidatura=row["id_candidatura"],
                id_vaga=row["id_vaga"],
                id_candidato=row["id_candidato"],
                data_candidatura=row["data_candidatura"],
                status=row["status"]
            )
            for row in rows
        ]

def obter_por_candidato(id_candidato: int) -> list[Candidatura]:
    """
    Retorna todas as candidaturas de um candidato.

    Args:
        id_candidato: ID do candidato

    Returns:
        Lista de objetos Candidatura
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_CANDIDATO, (id_candidato,))
        rows = cursor.fetchall()
        return [
            Candidatura(
                id_candidatura=row["id_candidatura"],
                id_vaga=row["id_vaga"],
                id_candidato=row["id_candidato"],
                data_candidatura=row["data_candidatura"],
                status=row["status"]
            )
            for row in rows
        ]

def verificar_candidatura_existente(id_vaga: int, id_candidato: int) -> bool:
    """
    Verifica se já existe uma candidatura do candidato para a vaga.

    Args:
        id_vaga: ID da vaga
        id_candidato: ID do candidato

    Returns:
        True se já existe candidatura, False caso contrário
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(VERIFICAR_CANDIDATURA_EXISTENTE, (id_vaga, id_candidato))
        return cursor.fetchone() is not None

def obter_quantidade_por_vaga(id_vaga: int) -> int:
    """
    Retorna a quantidade de candidaturas para uma vaga.

    Args:
        id_vaga: ID da vaga

    Returns:
        Número de candidaturas
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_VAGA, (id_vaga,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def obter_quantidade_por_candidato(id_candidato: int) -> int:
    """
    Retorna a quantidade de candidaturas de um candidato.

    Args:
        id_candidato: ID do candidato

    Returns:
        Número de candidaturas
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_CANDIDATO, (id_candidato,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def obter_quantidade_por_status(status: str) -> int:
    """
    Retorna a quantidade de candidaturas com determinado status.

    Args:
        status: Status das candidaturas

    Returns:
        Número de candidaturas com o status especificado
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_STATUS, (status,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def buscar_por_status_e_vaga(id_vaga: int, status: str) -> list[Candidatura]:
    """
    Busca candidaturas de uma vaga com determinado status.

    Args:
        id_vaga: ID da vaga
        status: Status das candidaturas

    Returns:
        Lista de objetos Candidatura
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(BUSCAR_POR_STATUS_E_VAGA, (id_vaga, status))
        rows = cursor.fetchall()
        return [
            Candidatura(
                id_candidatura=row["id_candidatura"],
                id_vaga=row["id_vaga"],
                id_candidato=row["id_candidato"],
                data_candidatura=row["data_candidatura"],
                status=row["status"]
            )
            for row in rows
        ]

def obter_quantidade() -> int:
    """
    Retorna a quantidade total de candidaturas.

    Returns:
        Número de candidaturas
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def obter_por_status(status: str) -> list[Candidatura]:
    """
    Busca candidaturas por status.

    Args:
        status: Status das candidaturas

    Returns:
        Lista de objetos Candidatura
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_STATUS, (status,))
        rows = cursor.fetchall()
        return [
            Candidatura(
                id_candidatura=row["id_candidatura"],
                id_vaga=row["id_vaga"],
                id_candidato=row["id_candidato"],
                data_candidatura=row["data_candidatura"],
                status=row["status"]
            )
            for row in rows
        ]

def verificar_candidatura(id_vaga: int, id_candidato: int) -> bool:
    """
    Verifica se já existe candidatura de um candidato para uma vaga.
    Alias para verificar_candidatura_existente.

    Args:
        id_vaga: ID da vaga
        id_candidato: ID do candidato

    Returns:
        True se existe candidatura, False caso contrário
    """
    return verificar_candidatura_existente(id_vaga, id_candidato)
