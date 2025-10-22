from typing import Optional
from model.empresa_model import Empresa
from sql.empresa_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    """Cria a tabela de empresas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(empresa: Empresa) -> Optional[int]:
    """Insere uma nova empresa."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (empresa.nome, empresa.cnpj, empresa.descricao))
        return cursor.lastrowid

def alterar(empresa: Empresa) -> bool:
    """Altera uma empresa existente."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            empresa.nome,
            empresa.cnpj,
            empresa.descricao,
            empresa.id_empresa
        ))
        return cursor.rowcount > 0

def excluir(id_empresa: int) -> bool:
    """Exclui uma empresa."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_empresa,))
        return cursor.rowcount > 0

def obter_por_id(id_empresa: int) -> Optional[Empresa]:
    """Obtém uma empresa por ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_empresa,))
        row = cursor.fetchone()
        if row:
            return Empresa(
                id_empresa=row["id_empresa"],
                nome=row["nome"],
                cnpj=row["cnpj"],
                descricao=row["descricao"]
            )
        return None

def obter_todas() -> list[Empresa]:
    """Obtém todas as empresas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        rows = cursor.fetchall()
        return [
            Empresa(
                id_empresa=row["id_empresa"],
                nome=row["nome"],
                cnpj=row["cnpj"],
                descricao=row["descricao"]
            )
            for row in rows
        ]

def obter_por_cnpj(cnpj: str) -> Optional[Empresa]:
    """Obtém uma empresa por CNPJ."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_CNPJ, (cnpj,))
        row = cursor.fetchone()
        if row:
            return Empresa(
                id_empresa=row["id_empresa"],
                nome=row["nome"],
                cnpj=row["cnpj"],
                descricao=row["descricao"]
            )
        return None

def obter_quantidade() -> int:
    """Obtém a quantidade total de empresas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def buscar(termo: Optional[str] = None, limite: int = 50, offset: int = 0) -> list[Empresa]:
    """Busca empresas com filtros."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(BUSCAR, (termo, termo, limite, offset))
        rows = cursor.fetchall()
        return [
            Empresa(
                id_empresa=row["id_empresa"],
                nome=row["nome"],
                cnpj=row["cnpj"],
                descricao=row["descricao"]
            )
            for row in rows
        ]