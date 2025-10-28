from typing import Optional
import sqlite3
from model.configuracao_model import Configuracao
from sql.configuracao_sql import *
from util.db_util import get_connection
from util.logger_config import logger

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def obter_por_chave(chave: str) -> Optional[Configuracao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_CHAVE, (chave,))
        row = cursor.fetchone()
        if row:
            return Configuracao(
                id=row["id"],
                chave=row["chave"],
                valor=row["valor"],
                descricao=row["descricao"]
            )
        return None

def obter_todos() -> list[Configuracao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [
            Configuracao(
                id=row["id"],
                chave=row["chave"],
                valor=row["valor"],
                descricao=row["descricao"]
            )
            for row in rows
        ]

def atualizar(chave: str, valor: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (valor, chave))
        return cursor.rowcount > 0


def inserir_ou_atualizar(chave: str, valor: str, descricao: str = "") -> bool:
    try:
        # Verificar se configuração já existe
        config_existente = obter_por_chave(chave)

        if config_existente:
            # Configuração existe - atualizar
            logger.debug(f"Atualizando configuração existente: {chave} = {valor}")
            return atualizar(chave, valor)
        else:
            # Configuração não existe - inserir
            logger.debug(f"Inserindo nova configuração: {chave} = {valor}")
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(INSERIR, (chave, valor, descricao))
                return cursor.rowcount > 0

    except Exception as e:
        logger.error(f"Erro ao inserir ou atualizar configuração '{chave}': {e}")
        raise

def inserir_padrao() -> None:
    configs_padrao = [
        ("nome_sistema", "Sistema Web", "Nome do sistema"),
        ("email_contato", "contato@sistema.com", "E-mail de contato"),
        ("tema_padrao", "claro", "Tema padrão (claro/escuro)"),
        ("theme", "original", "Tema visual da aplicação (Bootswatch)"),
    ]

    with get_connection() as conn:
        cursor = conn.cursor()
        for chave, valor, descricao in configs_padrao:
            try:
                cursor.execute(INSERIR, (chave, valor, descricao))
            except sqlite3.IntegrityError:
                # Configuração já existe (violação de UNIQUE constraint)
                logger.debug(f"Configuração '{chave}' já existe, pulando inserção")
            except Exception as e:
                # Outro tipo de erro - logar e re-raise para não mascarar problema
                logger.error(f"Erro ao inserir configuração padrão '{chave}': {e}")
                raise
