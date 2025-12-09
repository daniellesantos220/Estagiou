from typing import Optional
from model.vaga_model import Vaga
from sql.vaga_sql import *
from util.db_util import obter_conexao


def _row_to_vaga(row) -> Vaga:
    """Converte uma row do banco para objeto Vaga."""
    return Vaga(
        id_vaga=row["id_vaga"],
        id_area=row["id_area"],
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
        uf=row["uf"] if "uf" in row.keys() else None,
        area_nome=row["area_nome"] if "area_nome" in row.keys() else None,
        recrutador_nome=row["recrutador_nome"] if "recrutador_nome" in row.keys() else None,
    )


def criar_tabela() -> bool:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True


def inserir(vaga: Vaga) -> Optional[int]:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            vaga.id_area,
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
    with obter_conexao() as conn:
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
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR_STATUS, (status, id_vaga))
        return cursor.rowcount > 0


def excluir(id_vaga: int) -> bool:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_vaga,))
        return cursor.rowcount > 0


def obter_por_id(id_vaga: int) -> Optional[Vaga]:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_vaga,))
        row = cursor.fetchone()
        if row:
            return _row_to_vaga(row)
        return None


def obter_todas() -> list[Vaga]:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        rows = cursor.fetchall()
        return [_row_to_vaga(row) for row in rows]


def obter_por_recrutador(id_recrutador: int) -> list[Vaga]:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_RECRUTADOR, (id_recrutador,))
        rows = cursor.fetchall()
        return [_row_to_vaga(row) for row in rows]


def buscar(
    id_area: Optional[int] = None,
    cidade: Optional[str] = None,
    uf: Optional[str] = None,
    modalidade: Optional[str] = None,
    salario_min: Optional[float] = None,
    limit: int = 50,
    offset: int = 0
) -> list[Vaga]:
    with obter_conexao() as conn:
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
        return [_row_to_vaga(row) for row in rows]


def obter_quantidade() -> int:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0


def obter_quantidade_por_status(status: str) -> int:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_STATUS, (status,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0


def obter_quantidade_por_area(id_area: int) -> int:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_AREA, (id_area,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0


def obter_vagas_abertas(limit: int = 50, offset: int = 0) -> list[Vaga]:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_VAGAS_ABERTAS, (limit, offset))
        rows = cursor.fetchall()
        return [_row_to_vaga(row) for row in rows]


def obter_ultimas_abertas(limit: int = 6) -> list[Vaga]:
    """Retorna as últimas vagas abertas (para home page)."""
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ULTIMAS_ABERTAS, (limit,))
        rows = cursor.fetchall()
        return [_row_to_vaga(row) for row in rows]


def buscar_por_termo(termo: Optional[str] = None, id_area: Optional[int] = None) -> list[Vaga]:
    """Busca vagas por palavra-chave no título/descrição e/ou por área."""
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(BUSCAR_POR_TERMO, (
            id_area, id_area,
            termo, termo, termo, termo
        ))
        rows = cursor.fetchall()
        return [_row_to_vaga(row) for row in rows]


def obter_por_status(status: str) -> list[Vaga]:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM vaga WHERE status_vaga = ? ORDER BY data_cadastro DESC",
            (status,)
        )
        rows = cursor.fetchall()
        return [_row_to_vaga(row) for row in rows]


def atualizar_status(id_vaga: int, novo_status: str) -> bool:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE vaga SET status_vaga = ? WHERE id_vaga = ?",
            (novo_status, id_vaga)
        )
        return cursor.rowcount > 0


def registrar_motivo_reprovacao(id_vaga: int, motivo: str) -> bool:
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE vaga SET motivo_reprovacao = ? WHERE id_vaga = ?",
            (motivo, id_vaga)
        )
        return cursor.rowcount > 0


def contar_candidaturas(id_vaga: int) -> int:
    try:
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) as quantidade FROM candidatura WHERE id_vaga = ?",
                (id_vaga,)
            )
            row = cursor.fetchone()
            return row["quantidade"] if row else 0
    except Exception:
        return 0
