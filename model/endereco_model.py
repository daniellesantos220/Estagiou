from dataclasses import dataclass
from typing import Optional


@dataclass
class Endereco:
    """
    Model de endereço no sistema Estagiou.

    Attributes:
        id_endereco: Identificador único do endereço
        id_usuario: FK para Usuario
        titulo: Título do endereço (ex: Casa, Trabalho)
        logradouro: Nome da rua/avenida
        numero: Número do imóvel
        complemento: Complemento do endereço (opcional)
        bairro: Nome do bairro
        cidade: Nome da cidade
        uf: Sigla do estado (2 letras)
        cep: CEP formatado

        # Relacionamentos
        usuario: Objeto Usuario (opcional)
    """
    id_endereco: int
    id_usuario: int
    titulo: str
    logradouro: str
    numero: str
    bairro: str
    cidade: str
    uf: str
    cep: str
    complemento: Optional[str] = None

    # Relacionamentos
    usuario: Optional[object] = None