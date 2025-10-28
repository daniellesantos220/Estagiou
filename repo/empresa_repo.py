from typing import Optional
from model.empresa_model import Empresa
from sql.empresa_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(empresa: Empresa) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            empresa.nome,
            empresa.cnpj,
            empresa.descricao
        ))
        return cursor.lastrowid

def alterar(empresa: Empresa) -> bool:
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
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_empresa,))
        return cursor.rowcount > 0

def obter_por_id(id_empresa: int) -> Optional[Empresa]:
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
                data_cadastro=row["data_cadastro"] if "data_cadastro" in row.keys() else None,
                data_atualizacao=row["data_atualizacao"] if "data_atualizacao" in row.keys() else None
            )
        return None

def obter_todas() -> list[Empresa]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        rows = cursor.fetchall()
        return [
            Empresa(
                id_empresa=row["id_empresa"],
                nome=row["nome"],
                cnpj=row["cnpj"],
                descricao=row["descricao"],
                data_cadastro=row["data_cadastro"] if "data_cadastro" in row.keys() else None,
                data_atualizacao=row["data_atualizacao"] if "data_atualizacao" in row.keys() else None
            )
            for row in rows
        ]

def obter_por_cnpj(cnpj: str) -> Optional[Empresa]:
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
                data_cadastro=row["data_cadastro"] if "data_cadastro" in row.keys() else None,
                data_atualizacao=row["data_atualizacao"] if "data_atualizacao" in row.keys() else None
            )
        return None

def obter_quantidade() -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def buscar(nome: Optional[str] = None, limit: int = 50, offset: int = 0) -> list[Empresa]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(BUSCAR, (nome, nome, limit, offset))
        rows = cursor.fetchall()
        return [
            Empresa(
                id_empresa=row["id_empresa"],
                nome=row["nome"],
                cnpj=row["cnpj"],
                descricao=row["descricao"],
                data_cadastro=row["data_cadastro"] if "data_cadastro" in row.keys() else None,
                data_atualizacao=row["data_atualizacao"] if "data_atualizacao" in row.keys() else None
            )
            for row in rows
        ]
