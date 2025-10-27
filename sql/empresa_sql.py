"""
SQL statements para gerenciamento de empresas.
"""

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS empresa (
    id_empresa INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cnpj TEXT UNIQUE NOT NULL,
    descricao TEXT,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

INSERIR = """
INSERT INTO empresa (nome, cnpj, descricao)
VALUES (?, ?, ?)
"""

ALTERAR = """
UPDATE empresa
SET nome = ?, cnpj = ?, descricao = ?
WHERE id_empresa = ?
"""

EXCLUIR = "DELETE FROM empresa WHERE id_empresa = ?"

OBTER_POR_ID = "SELECT * FROM empresa WHERE id_empresa = ?"

OBTER_TODAS = "SELECT * FROM empresa ORDER BY nome"

OBTER_POR_CNPJ = "SELECT * FROM empresa WHERE cnpj = ?"

OBTER_QUANTIDADE = "SELECT COUNT(*) as quantidade FROM empresa"

# Buscar empresas com filtros
BUSCAR = """
SELECT * FROM empresa
WHERE (? IS NULL OR nome LIKE '%' || ? || '%')
ORDER BY nome
LIMIT ? OFFSET ?
"""