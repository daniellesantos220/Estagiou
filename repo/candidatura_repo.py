from typing import Optional
from model.candidatura_model import Candidatura
from sql.candidatura_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    """Cria a tabela de candidaturas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(candidatura: Candidatura) -> Optional[int]:
    """Insere uma nova candidatura."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            candidatura.id_vaga,
            candidatura.id_candidato
        ))
        return cursor.lastrowid

def alterar_status(id_candidatura: int, status: str) -> bool:
    """Altera o status de uma candidatura."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR_STATUS, (status, id_candidatura))
        return cursor.rowcount > 0

def excluir(id_candidatura: int) -> bool:
    """Exclui uma candidatura (cancelar candidatura)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_candidatura,))
        return cursor.rowcount > 0

def obter_por_id(id_candidatura: int) -> Optional[Candidatura]:
    """Obtém uma candidatura por ID."""
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
    """Obtém todas as candidaturas de uma vaga."""
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
    """Obtém todas as candidaturas de um candidato."""
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
    """Verifica se o candidato já se candidatou a essa vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(VERIFICAR_CANDIDATURA_EXISTENTE, (id_vaga, id_candidato))
        row = cursor.fetchone()
        return row is not None

def obter_quantidade_por_vaga(id_vaga: int) -> int:
    """Obtém quantidade de candidaturas de uma vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_VAGA, (id_vaga,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def obter_quantidade_por_candidato(id_candidato: int) -> int:
    """Obtém quantidade de candidaturas de um candidato."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_CANDIDATO, (id_candidato,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def buscar_por_status_e_vaga(id_vaga: int, status: str) -> list[Candidatura]:
    """Busca candidaturas por status e vaga."""
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