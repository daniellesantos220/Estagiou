CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS mensagem (
    id_mensagem INTEGER PRIMARY KEY AUTOINCREMENT,
    id_remetente INTEGER NOT NULL,
    id_destinatario INTEGER NOT NULL,
    assunto TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    lida INTEGER DEFAULT 0,
    data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_remetente) REFERENCES usuario(id),
    FOREIGN KEY (id_destinatario) REFERENCES usuario(id)
)
"""

INSERIR = """
INSERT INTO mensagem (id_remetente, id_destinatario, assunto, conteudo)
VALUES (?, ?, ?, ?)
"""

MARCAR_COMO_LIDA = """
UPDATE mensagem SET lida = 1 WHERE id_mensagem = ?
"""

EXCLUIR = "DELETE FROM mensagem WHERE id_mensagem = ?"

OBTER_POR_ID = """
SELECT m.*,
       r.nome as remetente_nome, r.email as remetente_email,
       d.nome as destinatario_nome, d.email as destinatario_email
FROM mensagem m
LEFT JOIN usuario r ON m.id_remetente = r.id
LEFT JOIN usuario d ON m.id_destinatario = d.id
WHERE m.id_mensagem = ?
"""

OBTER_RECEBIDAS = """
SELECT m.*, u.nome as remetente_nome
FROM mensagem m
LEFT JOIN usuario u ON m.id_remetente = u.id
WHERE m.id_destinatario = ?
ORDER BY m.data_envio DESC
"""

OBTER_ENVIADAS = """
SELECT m.*, u.nome as destinatario_nome
FROM mensagem m
LEFT JOIN usuario u ON m.id_destinatario = u.id
WHERE m.id_remetente = ?
ORDER BY m.data_envio DESC
"""

CONTAR_NAO_LIDAS = """
SELECT COUNT(*) as quantidade
FROM mensagem
WHERE id_destinatario = ? AND lida = 0
"""