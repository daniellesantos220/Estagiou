from dataclasses import dataclass
from typing import Optional
from util.perfis import Perfil

@dataclass
class Usuario:
    """
    Model de usuário do sistema Estagiou.

    Attributes:
        id: Identificador único do usuário
        nome: Nome completo do usuário
        email: E-mail único do usuário
        senha: Hash da senha do usuário
        perfil: Perfil do usuário (Perfil.ADMIN.value, Perfil.ESTUDANTE.value, Perfil.RECRUTADOR.value)

        # Novos campos do Estagiou
        data_nascimento: Data de nascimento (formato: YYYY-MM-DD)
        telefone: Telefone de contato (opcional)
        numero_documento: CPF ou outro documento (opcional)
        confirmado: Se o usuário confirmou o e-mail (boolean)
        curriculo_path: Caminho para o arquivo de currículo em PDF (opcional)

        # Campos de recuperação de senha
        token_redefinicao: Token para redefinição de senha (opcional)
        data_token: Data de expiração do token (opcional)
        data_cadastro: Data de cadastro do usuário (opcional)

    Nota: A foto do usuário é armazenada no filesystem em /static/img/usuarios/{id:06d}.jpg
          O currículo é armazenado em /static/curriculos/{id:06d}.pdf
    """
    id: int
    nome: str
    email: str
    senha: str
    perfil: str

    # Novos campos
    data_nascimento: Optional[str] = None
    telefone: Optional[str] = None
    numero_documento: Optional[str] = None
    confirmado: bool = False
    curriculo_path: Optional[str] = None

    # Campos existentes
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None
    data_cadastro: Optional[str] = None
