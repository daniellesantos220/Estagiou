from dataclasses import dataclass
from typing import Optional

@dataclass
class Vaga:
    """
    Model de vaga de estágio no sistema Estagiou.

    Attributes:
        id_vaga: Identificador único da vaga
        id_area: FK para Area
        id_empresa: FK para Empresa
        id_recrutador: FK para Usuario (recrutador que criou a vaga)
        status_vaga: Status da vaga (aberta, fechada, pausada, arquivada)
        descricao: Descrição detalhada da vaga
        numero_vagas: Quantidade de vagas disponíveis
        salario: Valor da bolsa/salário
        data_cadastro: Data de criação da vaga

        # Campos adicionais sugeridos (não estão no diagrama ER mas são úteis)
        titulo: Título da vaga
        requisitos: Requisitos da vaga
        beneficios: Benefícios oferecidos
        carga_horaria: Carga horária semanal
        modalidade: Presencial, Remoto ou Híbrido
        cidade: Cidade da vaga
        uf: Estado da vaga

        # Relacionamentos (populados via JOIN)
        area: Objeto Area (opcional)
        empresa: Objeto Empresa (opcional)
        recrutador: Objeto Usuario (opcional)
    """
    id_vaga: int
    id_area: int
    id_empresa: int
    id_recrutador: int
    status_vaga: str
    titulo: str
    descricao: str
    numero_vagas: int
    salario: float
    data_cadastro: str

    # Campos opcionais
    requisitos: Optional[str] = None
    beneficios: Optional[str] = None
    carga_horaria: Optional[int] = None
    modalidade: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None

    # Relacionamentos
    area: Optional[object] = None
    empresa: Optional[object] = None
    recrutador: Optional[object] = None