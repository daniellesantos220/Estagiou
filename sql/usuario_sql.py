CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    perfil TEXT DEFAULT 'Estudante',

    -- Novos campos do Estagiou
    data_nascimento TEXT,
    telefone TEXT,
    numero_documento TEXT,
    confirmado INTEGER DEFAULT 0,
    curriculo_path TEXT,

    -- Campos de recuperação de senha
    token_redefinicao TEXT,
    data_token DATETIME,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

# Atualizar statements INSERIR e ALTERAR para incluir novos campos
INSERIR = """
INSERT INTO usuario (nome, email, senha, perfil, data_nascimento, telefone, numero_documento)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

ALTERAR = """
UPDATE usuario
SET nome = ?, email = ?, perfil = ?, data_nascimento = ?, telefone = ?, numero_documento = ?
WHERE id = ?
"""

# Novo statement para atualizar caminho do currículo
ATUALIZAR_CURRICULO = """
UPDATE usuario
SET curriculo_path = ?
WHERE id = ?
"""

# Novo statement para confirmar e-mail
CONFIRMAR_EMAIL = """
UPDATE usuario
SET confirmado = 1
WHERE id = ?
"""