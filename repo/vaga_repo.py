from typing import Optional
from model.vaga_model import Vaga
from model.area_model import Area
from model.empresa_model import Empresa
from model.usuario_model import Usuario
from sql.vaga_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    """Cria a tabela de vagas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(vaga: Vaga) -> Optional[int]:
    """Insere uma nova vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            vaga.id_area,
            vaga.id_empresa,
            vaga.id_recrutador,
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
    """Altera uma vaga existente."""
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
    """Altera o status de uma vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR_STATUS, (status, id_vaga))
        return cursor.rowcount > 0

def excluir(id_vaga: int) -> bool:
    """Exclui uma vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_vaga,))
        return cursor.rowcount > 0

def _montar_vaga_completa(row) -> Vaga:
    """Monta objeto Vaga com relacionamentos."""
    vaga = Vaga(
        id_vaga=row["id_vaga"],
        id_area=row["id_area"],
        id_empresa=row["id_empresa"],
        id_recrutador=row["id_recrutador"],
        status_vaga=row["status_vaga"],
        descricao=row["descricao"],
        numero_vagas=row["numero_vagas"],
        salario=row["salario"],
        data_cadastro=row["data_cadastro"],
        titulo=row.get("titulo"),
        requisitos=row.get("requisitos"),
        beneficios=row.get("beneficios"),
        carga_horaria=row.get("carga_horaria"),
        modalidade=row.get("modalidade"),
        cidade=row.get("cidade"),
        uf=row.get("uf")
    )

    # Adicionar área se disponível
    if "area_nome" in row.keys():
        vaga.area = Area(
            id_area=row["id_area"],
            nome=row["area_nome"],
            descricao=row.get("area_descricao", "")
        )

    # Adicionar empresa se disponível
    if "empresa_nome" in row.keys():
        vaga.empresa = Empresa(
            id_empresa=row["id_empresa"],
            nome=row["empresa_nome"],
            cnpj=row.get("empresa_cnpj", ""),
            descricao=row.get("empresa_descricao", "")
        )

    return vaga

def obter_por_id(id_vaga: int) -> Optional[Vaga]:
    """Obtém uma vaga por ID com relacionamentos."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_vaga,))
        row = cursor.fetchone()
        if row:
            return _montar_vaga_completa(row)
        return None

def obter_todas() -> list[Vaga]:
    """Obtém todas as vagas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        rows = cursor.fetchall()
        return [_montar_vaga_completa(row) for row in rows]

def obter_por_empresa(id_empresa: int) -> list[Vaga]:
    """Obtém vagas de uma empresa específica."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_EMPRESA, (id_empresa,))
        rows = cursor.fetchall()
        return [_montar_vaga_completa(row) for row in rows]

def obter_por_recrutador(id_recrutador: int) -> list[Vaga]:
    """Obtém vagas de um recrutador específico."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_RECRUTADOR, (id_recrutador,))
        rows = cursor.fetchall()
        return [_montar_vaga_completa(row) for row in rows]

def buscar(
    id_area: Optional[int] = None,
    cidade: Optional[str] = None,
    uf: Optional[str] = None,
    modalidade: Optional[str] = None,
    salario_minimo: Optional[float] = None,
    limite: int = 50,
    offset: int = 0
) -> list[Vaga]:
    """Busca vagas com filtros."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(BUSCAR, (
            id_area, id_area,
            cidade, cidade,
            uf, uf,
            modalidade, modalidade,
            salario_minimo, salario_minimo,
            limite, offset
        ))
        rows = cursor.fetchall()
        return [_montar_vaga_completa(row) for row in rows]

def obter_vagas_abertas(limite: int = 50, offset: int = 0) -> list[Vaga]:
    """Obtém apenas vagas abertas (para visualização pública)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_VAGAS_ABERTAS, (limite, offset))
        rows = cursor.fetchall()
        return [_montar_vaga_completa(row) for row in rows]

def obter_quantidade() -> int:
    """Obtém a quantidade total de vagas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def obter_quantidade_por_status(status: str) -> int:
    """Obtém a quantidade de vagas por status."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_STATUS, (status,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0