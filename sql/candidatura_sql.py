"""
SQL statements para gerenciamento de candidaturas.
"""

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS candidatura (
    id_candidatura INTEGER PRIMARY KEY AUTOINCREMENT,
    id_vaga INTEGER NOT NULL,
    id_candidato INTEGER NOT NULL,
    data_candidatura DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pendente',
    FOREIGN KEY (id_vaga) REFERENCES vaga(id_vaga),
    FOREIGN KEY (id_candidato) REFERENCES usuario(id),
    UNIQUE(id_vaga, id_candidato)  -- Um candidato não pode se candidatar duas vezes à mesma vaga
)
"""

INSERIR = """
INSERT INTO candidatura (id_vaga, id_candidato)
VALUES (?, ?)
"""

ALTERAR_STATUS = """
UPDATE candidatura
SET status = ?
WHERE id_candidatura = ?
"""

EXCLUIR = "DELETE FROM candidatura WHERE id_candidatura = ?"

OBTER_POR_ID = """
SELECT c.*,
       v.titulo as vaga_titulo, v.descricao as vaga_descricao, v.salario as vaga_salario,
       u.nome as candidato_nome, u.email as candidato_email, u.telefone as candidato_telefone
FROM candidatura c
LEFT JOIN vaga v ON c.id_vaga = v.id_vaga
LEFT JOIN usuario u ON c.id_candidato = u.id
WHERE c.id_candidatura = ?
"""

OBTER_POR_VAGA = """
SELECT c.*,
       u.nome as candidato_nome, u.email as candidato_email,
       u.telefone as candidato_telefone, u.curriculo_path
FROM candidatura c
LEFT JOIN usuario u ON c.id_candidato = u.id
WHERE c.id_vaga = ?
ORDER BY c.data_candidatura DESC
"""

OBTER_POR_CANDIDATO = """
SELECT c.*,
       v.titulo as vaga_titulo, v.salario as vaga_salario, v.cidade as vaga_cidade,
       e.nome as empresa_nome
FROM candidatura c
LEFT JOIN vaga v ON c.id_vaga = v.id_vaga
LEFT JOIN empresa e ON v.id_empresa = e.id_empresa
WHERE c.id_candidato = ?
ORDER BY c.data_candidatura DESC
"""

VERIFICAR_CANDIDATURA_EXISTENTE = """
SELECT id_candidatura
FROM candidatura
WHERE id_vaga = ? AND id_candidato = ?
"""

OBTER_QUANTIDADE_POR_VAGA = """
SELECT COUNT(*) as quantidade
FROM candidatura
WHERE id_vaga = ?
"""

OBTER_QUANTIDADE_POR_CANDIDATO = """
SELECT COUNT(*) as quantidade
FROM candidatura
WHERE id_candidato = ?
"""

OBTER_QUANTIDADE_POR_STATUS = """
SELECT COUNT(*) as quantidade
FROM candidatura
WHERE status = ?
"""

OBTER_QUANTIDADE = """
SELECT COUNT(*) as quantidade
FROM candidatura
"""

OBTER_POR_STATUS = """
SELECT c.*,
       v.titulo as vaga_titulo, v.salario as vaga_salario,
       u.nome as candidato_nome, u.email as candidato_email
FROM candidatura c
LEFT JOIN vaga v ON c.id_vaga = v.id_vaga
LEFT JOIN usuario u ON c.id_candidato = u.id
WHERE c.status = ?
ORDER BY c.data_candidatura DESC
"""

# Obter candidaturas com filtros
BUSCAR_POR_STATUS_E_VAGA = """
SELECT c.*,
       u.nome as candidato_nome, u.email as candidato_email
FROM candidatura c
LEFT JOIN usuario u ON c.id_candidato = u.id
WHERE c.id_vaga = ? AND c.status = ?
ORDER BY c.data_candidatura DESC
"""