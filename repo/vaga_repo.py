from typing import Optional
from model.vaga_model import Vaga
from sql.vaga_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(vaga: Vaga) -> Optional[int]:
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
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR_STATUS, (status, id_vaga))
        return cursor.rowcount > 0

def excluir(id_vaga: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_vaga,))
        return cursor.rowcount > 0

def obter_por_id(id_vaga: int) -> Optional[Vaga]:
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
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def obter_quantidade_por_status(status: str) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_STATUS, (status,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0
    
def obter_quantidade_por_area(id_area: int) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_AREA, (id_area,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def obter_vagas_abertas(limit: int = 50, offset: int = 0) -> list[Vaga]:
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

def obter_por_status(status: str) -> list[Vaga]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM vaga WHERE status = ? ORDER BY data_cadastro DESC",
            (status,)
        )
        rows = cursor.fetchall()
        return [Vaga(**dict(row)) for row in rows]

def atualizar_status(id_vaga: int, novo_status: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE vaga SET status = ? WHERE id_vaga = ?",
            (novo_status, id_vaga)
        )
        return cursor.rowcount > 0

def registrar_motivo_reprovacao(id_vaga: int, motivo: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE vaga SET motivo_reprovacao = ? WHERE id_vaga = ?",
            (motivo, id_vaga)
        )
        return cursor.rowcount > 0

def contar_candidaturas(id_vaga: int) -> int:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) as quantidade FROM candidatura WHERE id_vaga = ?",
                (id_vaga,)
            )
            row = cursor.fetchone()
            return row["quantidade"] if row else 0
    except Exception:
        return 0