CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS avaliacao (
    id_avaliacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_empresa INTEGER NOT NULL,
    id_estudante INTEGER NOT NULL,
    nota INTEGER NOT NULL CHECK(nota >= 1 AND nota <= 5),
    comentario TEXT,
    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_empresa) REFERENCES empresa(id_empresa),
    FOREIGN KEY (id_estudante) REFERENCES usuario(id),
    UNIQUE(id_empresa, id_estudante)
)
"""

INSERIR = """
INSERT INTO avaliacao (id_empresa, id_estudante, nota, comentario)
VALUES (?, ?, ?, ?)
"""

ALTERAR = """
UPDATE avaliacao
SET nota = ?, comentario = ?
WHERE id_avaliacao = ?
"""

OBTER_POR_EMPRESA = """
SELECT a.*, u.nome as estudante_nome
FROM avaliacao a
LEFT JOIN usuario u ON a.id_estudante = u.id
WHERE a.id_empresa = ?
ORDER BY a.data_avaliacao DESC
"""

OBTER_MEDIA_EMPRESA = """
SELECT AVG(nota) as media, COUNT(*) as total
FROM avaliacao
WHERE id_empresa = ?
"""

VERIFICAR_AVALIACAO_EXISTENTE = """
SELECT id_avaliacao
FROM avaliacao
WHERE id_empresa = ? AND id_estudante = ?
"""