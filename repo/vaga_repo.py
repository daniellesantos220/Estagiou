from typing import Optional
from model.vaga_model import Vaga
from sql.vaga_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    """Cria a tabela de vagas se não existir."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(vaga: Vaga) -> Optional[int]:
    """
    Insere uma nova vaga no banco de dados.

    Args:
        vaga: Objeto Vaga com os dados a inserir

    Returns:
        ID da vaga inserida ou None em caso de erro
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            vaga.id_area,
            vaga.id_empresa,
            vaga.id_recrutador,
            vaga.status_vaga,
            vaga.titulo,
            vaga.descricao,
            vaga.numero_vagas,
            vaga.salario,
            vaga.requisitos,
            vaga.beneficios,
            vaga.carga_horaria,
            vaga.modalidade,
            vaga.cidade,
            vaga.uf
        ))
        return cursor.lastrowid

def alterar(vaga: Vaga) -> bool:
    """
    Atualiza uma vaga existente.

    Args:
        vaga: Objeto Vaga com os dados atualizados

    Returns:
        True se a atualização foi bem-sucedida, False caso contrário
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            vaga.id_area,
            vaga.titulo,
            vaga.descricao,
            vaga.numero_vagas,
            vaga.salario,
            vaga.requisitos,
            vaga.beneficios,
            vaga.carga_horaria,
            vaga.modalidade,
            vaga.cidade,
            vaga.uf,
            vaga.id_vaga
        ))
        return cursor.rowcount > 0

def alterar_status(id_vaga: int, status: str) -> bool:
    """
    Atualiza o status de uma vaga.

    Args:
        id_vaga: ID da vaga
        status: Novo status (aberta, fechada, pausada, arquivada)

    Returns:
        True se a atualização foi bem-sucedida, False caso contrário
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR_STATUS, (status, id_vaga))
        return cursor.rowcount > 0

def excluir(id_vaga: int) -> bool:
    """
    Exclui uma vaga do banco de dados.

    Args:
        id_vaga: ID da vaga a excluir

    Returns:
        True se a exclusão foi bem-sucedida, False caso contrário
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_vaga,))
        return cursor.rowcount > 0

def obter_por_id(id_vaga: int) -> Optional[Vaga]:
    """
    Busca uma vaga pelo ID com dados relacionados.

    Args:
        id_vaga: ID da vaga

    Returns:
        Objeto Vaga ou None se não encontrado
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_vaga,))
        row = cursor.fetchone()
        if row:
            return Vaga(
                id_vaga=row["id_vaga"],
                id_area=row["id_area"],
                id_empresa=row["id_empresa"],
                id_recrutador=row["id_recrutador"],
                status_vaga=row["status_vaga"] if "status_vaga" in row.keys() else "aberta",
                descricao=row["descricao"],
                numero_vagas=row["numero_vagas"] if "numero_vagas" in row.keys() else 1,
                salario=row["salario"] if "salario" in row.keys() else 0.0,
                data_cadastro=row["data_cadastro"] if "data_cadastro" in row.keys() else None,
                titulo=row["titulo"],
                requisitos=row["requisitos"] if "requisitos" in row.keys() else None,
                beneficios=row["beneficios"] if "beneficios" in row.keys() else None,
                carga_horaria=row["carga_horaria"] if "carga_horaria" in row.keys() else None,
                modalidade=row["modalidade"] if "modalidade" in row.keys() else None,
                cidade=row["cidade"] if "cidade" in row.keys() else None,
                uf=row["uf"] if "uf" in row.keys() else None
            )
        return None

def obter_todas() -> list[Vaga]:
    """
    Retorna todas as vagas cadastradas.

    Returns:
        Lista de objetos Vaga
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        rows = cursor.fetchall()
        return [
            Vaga(
                id_vaga=row["id_vaga"],
                id_area=row["id_area"],
                id_empresa=row["id_empresa"],
                id_recrutador=row["id_recrutador"],
                status_vaga=row["status_vaga"] if "status_vaga" in row.keys() else "aberta",
                descricao=row["descricao"],
                numero_vagas=row["numero_vagas"] if "numero_vagas" in row.keys() else 1,
                salario=row["salario"] if "salario" in row.keys() else 0.0,
                data_cadastro=row["data_cadastro"] if "data_cadastro" in row.keys() else None,
                titulo=row["titulo"],
                requisitos=row["requisitos"] if "requisitos" in row.keys() else None,
                beneficios=row["beneficios"] if "beneficios" in row.keys() else None,
                carga_horaria=row["carga_horaria"] if "carga_horaria" in row.keys() else None,
                modalidade=row["modalidade"] if "modalidade" in row.keys() else None,
                cidade=row["cidade"] if "cidade" in row.keys() else None,
                uf=row["uf"] if "uf" in row.keys() else None
            )
            for row in rows
        ]

def obter_por_empresa(id_empresa: int) -> list[Vaga]:
    """
    Retorna todas as vagas de uma empresa.

    Args:
        id_empresa: ID da empresa

    Returns:
        Lista de objetos Vaga
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_EMPRESA, (id_empresa,))
        rows = cursor.fetchall()
        return [
            Vaga(
                id_vaga=row["id_vaga"],
                id_area=row["id_area"],
                id_empresa=row["id_empresa"],
                id_recrutador=row["id_recrutador"],
                status_vaga=row["status_vaga"] if "status_vaga" in row.keys() else "aberta",
                descricao=row["descricao"],
                numero_vagas=row["numero_vagas"] if "numero_vagas" in row.keys() else 1,
                salario=row["salario"] if "salario" in row.keys() else 0.0,
                data_cadastro=row["data_cadastro"] if "data_cadastro" in row.keys() else None,
                titulo=row["titulo"],
                requisitos=row["requisitos"] if "requisitos" in row.keys() else None,
                beneficios=row["beneficios"] if "beneficios" in row.keys() else None,
                carga_horaria=row["carga_horaria"] if "carga_horaria" in row.keys() else None,
                modalidade=row["modalidade"] if "modalidade" in row.keys() else None,
                cidade=row["cidade"] if "cidade" in row.keys() else None,
                uf=row["uf"] if "uf" in row.keys() else None
            )
            for row in rows
        ]

def obter_por_recrutador(id_recrutador: int) -> list[Vaga]:
    """
    Retorna todas as vagas criadas por um recrutador.

    Args:
        id_recrutador: ID do recrutador

    Returns:
        Lista de objetos Vaga
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_RECRUTADOR, (id_recrutador,))
        rows = cursor.fetchall()
        return [
            Vaga(
                id_vaga=row["id_vaga"],
                id_area=row["id_area"],
                id_empresa=row["id_empresa"],
                id_recrutador=row["id_recrutador"],
                status_vaga=row["status_vaga"] if "status_vaga" in row.keys() else "aberta",
                descricao=row["descricao"],
                numero_vagas=row["numero_vagas"] if "numero_vagas" in row.keys() else 1,
                salario=row["salario"] if "salario" in row.keys() else 0.0,
                data_cadastro=row["data_cadastro"] if "data_cadastro" in row.keys() else None,
                titulo=row["titulo"],
                requisitos=row["requisitos"] if "requisitos" in row.keys() else None,
                beneficios=row["beneficios"] if "beneficios" in row.keys() else None,
                carga_horaria=row["carga_horaria"] if "carga_horaria" in row.keys() else None,
                modalidade=row["modalidade"] if "modalidade" in row.keys() else None,
                cidade=row["cidade"] if "cidade" in row.keys() else None,
                uf=row["uf"] if "uf" in row.keys() else None
            )
            for row in rows
        ]

def buscar(
    id_area: Optional[int] = None,
    cidade: Optional[str] = None,
    uf: Optional[str] = None,
    modalidade: Optional[str] = None,
    salario_min: Optional[float] = None,
    limit: int = 50,
    offset: int = 0
) -> list[Vaga]:
    """
    Busca vagas com filtros opcionais.

    Args:
        id_area: ID da área para filtrar (opcional)
        cidade: Cidade para filtrar (opcional)
        uf: Estado para filtrar (opcional)
        modalidade: Modalidade para filtrar (opcional)
        salario_min: Salário mínimo para filtrar (opcional)
        limit: Número máximo de resultados
        offset: Deslocamento para paginação

    Returns:
        Lista de objetos Vaga
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(BUSCAR, (
            id_area, id_area,
            cidade, cidade,
            uf, uf,
            modalidade, modalidade,
            salario_min, salario_min,
            limit, offset
        ))
        rows = cursor.fetchall()
        return [
            Vaga(
                id_vaga=row["id_vaga"],
                id_area=row["id_area"],
                id_empresa=row["id_empresa"],
                id_recrutador=row["id_recrutador"],
                status_vaga=row["status_vaga"] if "status_vaga" in row.keys() else "aberta",
                descricao=row["descricao"],
                numero_vagas=row["numero_vagas"] if "numero_vagas" in row.keys() else 1,
                salario=row["salario"] if "salario" in row.keys() else 0.0,
                data_cadastro=row["data_cadastro"] if "data_cadastro" in row.keys() else None,
                titulo=row["titulo"],
                requisitos=row["requisitos"] if "requisitos" in row.keys() else None,
                beneficios=row["beneficios"] if "beneficios" in row.keys() else None,
                carga_horaria=row["carga_horaria"] if "carga_horaria" in row.keys() else None,
                modalidade=row["modalidade"] if "modalidade" in row.keys() else None,
                cidade=row["cidade"] if "cidade" in row.keys() else None,
                uf=row["uf"] if "uf" in row.keys() else None
            )
            for row in rows
        ]

def obter_quantidade() -> int:
    """
    Retorna a quantidade total de vagas cadastradas.

    Returns:
        Número de vagas
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def obter_quantidade_por_status(status: str) -> int:
    """
    Retorna a quantidade de vagas com determinado status.

    Args:
        status: Status das vagas

    Returns:
        Número de vagas com o status especificado
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_STATUS, (status,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def obter_vagas_abertas(limit: int = 50, offset: int = 0) -> list[Vaga]:
    """
    Retorna vagas com status 'aberta'.

    Args:
        limit: Número máximo de resultados
        offset: Deslocamento para paginação

    Returns:
        Lista de objetos Vaga
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_VAGAS_ABERTAS, (limit, offset))
        rows = cursor.fetchall()
        return [
            Vaga(
                id_vaga=row["id_vaga"],
                id_area=row["id_area"],
                id_empresa=row["id_empresa"],
                id_recrutador=row["id_recrutador"],
                status_vaga=row["status_vaga"] if "status_vaga" in row.keys() else "aberta",
                descricao=row["descricao"],
                numero_vagas=row["numero_vagas"] if "numero_vagas" in row.keys() else 1,
                salario=row["salario"] if "salario" in row.keys() else 0.0,
                data_cadastro=row["data_cadastro"] if "data_cadastro" in row.keys() else None,
                titulo=row["titulo"],
                requisitos=row["requisitos"] if "requisitos" in row.keys() else None,
                beneficios=row["beneficios"] if "beneficios" in row.keys() else None,
                carga_horaria=row["carga_horaria"] if "carga_horaria" in row.keys() else None,
                modalidade=row["modalidade"] if "modalidade" in row.keys() else None,
                cidade=row["cidade"] if "cidade" in row.keys() else None,
                uf=row["uf"] if "uf" in row.keys() else None
            )
            for row in rows
        ]
