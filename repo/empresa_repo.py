from typing import Optional
from model.empresa_model import Empresa
from sql.empresa_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    """Cria a tabela de empresas se não existir."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(empresa: Empresa) -> Optional[int]:
    """
    Insere uma nova empresa no banco de dados.

    Args:
        empresa: Objeto Empresa com os dados a inserir

    Returns:
        ID da empresa inserida ou None em caso de erro
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            empresa.nome,
            empresa.cnpj,
            empresa.descricao
        ))
        return cursor.lastrowid

def alterar(empresa: Empresa) -> bool:
    """
    Atualiza uma empresa existente.

    Args:
        empresa: Objeto Empresa com os dados atualizados

    Returns:
        True se a atualização foi bem-sucedida, False caso contrário
    """
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
    """
    Exclui uma empresa do banco de dados.

    Args:
        id_empresa: ID da empresa a excluir

    Returns:
        True se a exclusão foi bem-sucedida, False caso contrário
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_empresa,))
        return cursor.rowcount > 0

def obter_por_id(id_empresa: int) -> Optional[Empresa]:
    """
    Busca uma empresa pelo ID.

    Args:
        id_empresa: ID da empresa

    Returns:
        Objeto Empresa ou None se não encontrado
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_empresa,))
        row = cursor.fetchone()
        if row:
            return Empresa(
                id_empresa=row["id_empresa"],
                nome=row["nome"],
                cnpj=row["cnpj"],
                descricao=row["descricao"] if "descricao" in row.keys() else "",
                data_cadastro=row["data_cadastro"] if "data_cadastro" in row.keys() else None
            )
        return None

def obter_todas() -> list[Empresa]:
    """
    Retorna todas as empresas cadastradas.

    Returns:
        Lista de objetos Empresa
    """
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
    """
    Busca uma empresa pelo CNPJ.

    Args:
        cnpj: CNPJ da empresa

    Returns:
        Objeto Empresa ou None se não encontrado
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_CNPJ, (cnpj,))
        row = cursor.fetchone()
        if row:
            return Empresa(
                id_empresa=row["id_empresa"],
                nome=row["nome"],
                cnpj=row["cnpj"],
                descricao=row["descricao"] if "descricao" in row.keys() else "",
                data_cadastro=row["data_cadastro"] if "data_cadastro" in row.keys() else None
            )
        return None

def obter_quantidade() -> int:
    """
    Retorna a quantidade total de empresas cadastradas.

    Returns:
        Número de empresas
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def buscar(nome: Optional[str] = None, limit: int = 50, offset: int = 0) -> list[Empresa]:
    """
    Busca empresas com filtros opcionais.

    Args:
        nome: Nome da empresa para filtrar (opcional)
        limit: Número máximo de resultados
        offset: Deslocamento para paginação

    Returns:
        Lista de objetos Empresa
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(BUSCAR, (nome, nome, limit, offset))
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
