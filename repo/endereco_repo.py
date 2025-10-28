from typing import Optional
from model.endereco_model import Endereco
from sql.endereco_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(endereco: Endereco) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            endereco.id_usuario,
            endereco.titulo,
            endereco.logradouro,
            endereco.numero,
            endereco.complemento,
            endereco.bairro,
            endereco.cidade,
            endereco.uf,
            endereco.cep
        ))
        return cursor.lastrowid

def alterar(endereco: Endereco) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            endereco.titulo,
            endereco.logradouro,
            endereco.numero,
            endereco.complemento,
            endereco.bairro,
            endereco.cidade,
            endereco.uf,
            endereco.cep,
            endereco.id_endereco
        ))
        return cursor.rowcount > 0

def excluir(id_endereco: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_endereco,))
        return cursor.rowcount > 0

def obter_por_id(id_endereco: int) -> Optional[Endereco]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_endereco,))
        row = cursor.fetchone()
        if row:
            return Endereco(
                id_endereco=row["id_endereco"],
                id_usuario=row["id_usuario"],
                titulo=row["titulo"],
                logradouro=row["logradouro"],
                numero=row["numero"],
                complemento=row["complemento"] if "complemento" in row.keys() else None,
                bairro=row["bairro"],
                cidade=row["cidade"],
                uf=row["uf"],
                cep=row["cep"]
            )
        return None

def obter_por_usuario(id_usuario: int) -> list[Endereco]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_USUARIO, (id_usuario,))
        rows = cursor.fetchall()
        return [
            Endereco(
                id_endereco=row["id_endereco"],
                id_usuario=row["id_usuario"],
                titulo=row["titulo"],
                logradouro=row["logradouro"],
                numero=row["numero"],
                complemento=row["complemento"] if "complemento" in row.keys() else None,
                bairro=row["bairro"],
                cidade=row["cidade"],
                uf=row["uf"],
                cep=row["cep"]
            )
            for row in rows
        ]

def obter_todos() -> list[Endereco]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [
            Endereco(
                id_endereco=row["id_endereco"],
                id_usuario=row["id_usuario"],
                titulo=row["titulo"],
                logradouro=row["logradouro"],
                numero=row["numero"],
                complemento=row["complemento"] if "complemento" in row.keys() else None,
                bairro=row["bairro"],
                cidade=row["cidade"],
                uf=row["uf"],
                cep=row["cep"]
            )
            for row in rows
        ]

def obter_quantidade() -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0
    

def obter_quantidade_por_usuario(id_usuario: int) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_USUARIO, (id_usuario,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0
