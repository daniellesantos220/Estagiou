CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS notificacao (
    id_notificacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    titulo TEXT NOT NULL,
    mensagem TEXT NOT NULL,
    lida INTEGER DEFAULT 0,
    link TEXT,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
)
"""

INSERIR = """
INSERT INTO notificacao (id_usuario, tipo, titulo, mensagem, link)
VALUES (?, ?, ?, ?, ?)
"""

MARCAR_COMO_LIDA = """
UPDATE notificacao SET lida = 1 WHERE id_notificacao = ?
"""

MARCAR_TODAS_COMO_LIDAS = """
UPDATE notificacao SET lida = 1 WHERE id_usuario = ?
"""

OBTER_POR_USUARIO = """
SELECT * FROM notificacao
WHERE id_usuario = ?
ORDER BY data_criacao DESC
LIMIT ? OFFSET ?
"""

OBTER_NAO_LIDAS = """
SELECT * FROM notificacao
WHERE id_usuario = ? AND lida = 0
ORDER BY data_criacao DESC
"""

CONTAR_NAO_LIDAS = """
SELECT COUNT(*) as quantidade
FROM notificacao
WHERE id_usuario = ? AND lida = 0
"""

EXCLUIR = "DELETE FROM notificacao WHERE id_notificacao = ?"