"""
SQL statements para gerenciamento de áreas de atuação.
"""

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS area (
    id_area INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT
)
"""

INSERIR = """
INSERT INTO area (nome, descricao)
VALUES (?, ?)
"""

ALTERAR = """
UPDATE area
SET nome = ?, descricao = ?
WHERE id_area = ?
"""

EXCLUIR = "DELETE FROM area WHERE id_area = ?"

OBTER_POR_ID = "SELECT * FROM area WHERE id_area = ?"

OBTER_TODAS = "SELECT * FROM area ORDER BY nome"

OBTER_POR_NOME = "SELECT * FROM area WHERE nome = ?"

OBTER_QUANTIDADE = "SELECT COUNT(*) as quantidade FROM area"

# Verifica se área está sendo usada em alguma vaga
VERIFICAR_USO = """
SELECT COUNT(*) as quantidade
FROM vaga
WHERE id_area = ?
"""