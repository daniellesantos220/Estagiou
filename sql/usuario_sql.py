# IMPORTANTE: O valor padrão 'Estudante' deve corresponder a Perfil.ESTUDANTE.value
# Fonte única da verdade: util.perfis.Perfil
# Valores válidos: 'Administrador' (Perfil.ADMIN.value), 'Estudante' (Perfil.ESTUDANTE.value), 'Recrutador' (Perfil.RECRUTADOR.value)
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

ALTERAR_SENHA = """
UPDATE usuario
SET senha = ?
WHERE id = ?
"""

EXCLUIR = "DELETE FROM usuario WHERE id = ?"

OBTER_POR_ID = "SELECT * FROM usuario WHERE id = ?"

OBTER_TODOS = "SELECT * FROM usuario ORDER BY nome"

OBTER_QUANTIDADE = "SELECT COUNT(*) as quantidade FROM usuario"

OBTER_POR_EMAIL = "SELECT * FROM usuario WHERE email = ?"

ATUALIZAR_TOKEN = """
UPDATE usuario
SET token_redefinicao = ?, data_token = ?
WHERE email = ?
"""

OBTER_POR_TOKEN = """
SELECT * FROM usuario
WHERE token_redefinicao = ?
"""

LIMPAR_TOKEN = """
UPDATE usuario
SET token_redefinicao = NULL, data_token = NULL
WHERE id = ?
"""

OBTER_TODOS_POR_PERFIL = """
SELECT * FROM usuario
WHERE perfil = ?
ORDER BY nome
"""