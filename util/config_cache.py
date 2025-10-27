from typing import Dict, Any
from repo import configuracao_repo

class ConfigCache:
    """Cache de configurações do sistema para melhor performance"""
    _cache: Dict[str, Any] = {}

    @classmethod
    def obter(cls, chave: str, padrao: str = "") -> str:
        """
        Obtém configuração com cache

        Args:
            chave: Chave da configuração
            padrao: Valor padrão se não encontrado

        Returns:
            Valor da configuração ou padrão
        """
        if chave not in cls._cache:
            config = configuracao_repo.obter_por_chave(chave)
            cls._cache[chave] = config.valor if config else padrao
        return cls._cache[chave]

    @classmethod
    def limpar(cls):
        """Limpa todo o cache de configurações"""
        cls._cache = {}

    @classmethod
    def limpar_chave(cls, chave: str):
        """Limpa cache de uma chave específica"""
        if chave in cls._cache:
            del cls._cache[chave]

# Instância global para uso em toda a aplicação
config = ConfigCache()
