from enum import Enum
from typing import Optional

class Perfil(str, Enum):
    """
    Enum centralizado para perfis de usuário do Estagiou.

    Este é a FONTE ÚNICA DA VERDADE para perfis no sistema.
    SEMPRE use este Enum ao referenciar perfis, NUNCA strings literais.

    Exemplos:
        - Correto: perfil = Perfil.ADMIN.value
        - Correto: perfil = Perfil.ESTUDANTE.value
        - Correto: perfil = Perfil.RECRUTADOR.value
        - ERRADO: perfil = "Administrador"
        - ERRADO: perfil = "Estudante"
    """

    # PERFIS DO ESTAGIOU #######################################
    ADMIN = "Administrador"
    ESTUDANTE = "Estudante"
    RECRUTADOR = "Recrutador"
    # FIM DOS PERFIS ############################################

    def __str__(self) -> str:
        """Retorna o valor do perfil como string"""
        return self.value

    @classmethod
    def valores(cls) -> list[str]:
        """
        Retorna lista de todos os valores de perfis.

        Returns:
            Lista com os valores: ["Administrador", "Estudante", "Recrutador"]
        """
        return [perfil.value for perfil in cls]

    @classmethod
    def existe(cls, valor: str) -> bool:
        """Verifica se um valor de perfil é válido."""
        return valor in cls.valores()

    @classmethod
    def from_string(cls, valor: str) -> Optional['Perfil']:
        """Converte uma string para o Enum Perfil correspondente."""
        try:
            return cls(valor)
        except ValueError:
            return None

    @classmethod
    def validar(cls, valor: str) -> str:
        """Valida e retorna o valor do perfil."""
        if not cls.existe(valor):
            raise ValueError(f'Perfil inválido: {valor}. Use: {", ".join(cls.valores())}')
        return valor
