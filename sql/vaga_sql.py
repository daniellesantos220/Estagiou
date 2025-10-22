"""
SQL statements para gerenciamento de vagas de estágio.
"""

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS vaga (
    id_vaga INTEGER PRIMARY KEY AUTOINCREMENT,
    id_area INTEGER NOT NULL,
    id_empresa INTEGER NOT NULL,
    id_recrutador INTEGER NOT NULL,
    status_vaga TEXT DEFAULT 'aberta',
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    numero_vagas INTEGER DEFAULT 1,
    salario REAL DEFAULT 0,
    requisitos TEXT,
    beneficios TEXT,
    carga_horaria INTEGER,
    modalidade TEXT,
    cidade TEXT,
    uf TEXT,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_area) REFERENCES area(id_area),
    FOREIGN KEY (id_empresa) REFERENCES empresa(id_empresa),
    FOREIGN KEY (id_recrutador) REFERENCES usuario(id)
)
"""

INSERIR = """
INSERT INTO vaga (
    id_area, id_empresa, id_recrutador, status_vaga, titulo, descricao,
    numero_vagas, salario, requisitos, beneficios,
    carga_horaria, modalidade, cidade, uf
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

ALTERAR = """
UPDATE vaga
SET id_area = ?, titulo = ?, descricao = ?, numero_vagas = ?,
    salario = ?, requisitos = ?, beneficios = ?, carga_horaria = ?,
    modalidade = ?, cidade = ?, uf = ?
WHERE id_vaga = ?
"""

ALTERAR_STATUS = """
UPDATE vaga
SET status_vaga = ?
WHERE id_vaga = ?
"""

EXCLUIR = "DELETE FROM vaga WHERE id_vaga = ?"

OBTER_POR_ID = """
SELECT v.*,
       a.nome as area_nome, a.descricao as area_descricao,
       e.nome as empresa_nome, e.cnpj as empresa_cnpj, e.descricao as empresa_descricao,
       u.nome as recrutador_nome, u.email as recrutador_email
FROM vaga v
LEFT JOIN area a ON v.id_area = a.id_area
LEFT JOIN empresa e ON v.id_empresa = e.id_empresa
LEFT JOIN usuario u ON v.id_recrutador = u.id
WHERE v.id_vaga = ?
"""

OBTER_TODAS = """
SELECT v.*,
       a.nome as area_nome,
       e.nome as empresa_nome
FROM vaga v
LEFT JOIN area a ON v.id_area = a.id_area
LEFT JOIN empresa e ON v.id_empresa = e.id_empresa
ORDER BY v.data_cadastro DESC
"""

OBTER_POR_EMPRESA = """
SELECT v.*, a.nome as area_nome
FROM vaga v
LEFT JOIN area a ON v.id_area = a.id_area
WHERE v.id_empresa = ?
ORDER BY v.data_cadastro DESC
"""

OBTER_POR_RECRUTADOR = """
SELECT v.*, a.nome as area_nome, e.nome as empresa_nome
FROM vaga v
LEFT JOIN area a ON v.id_area = a.id_area
LEFT JOIN empresa e ON v.id_empresa = e.id_empresa
WHERE v.id_recrutador = ?
ORDER BY v.data_cadastro DESC
"""

# Busca avançada com filtros
BUSCAR = """
SELECT v.*,
       a.nome as area_nome,
       e.nome as empresa_nome
FROM vaga v
LEFT JOIN area a ON v.id_area = a.id_area
LEFT JOIN empresa e ON v.id_empresa = e.id_empresa
WHERE (? IS NULL OR v.id_area = ?)
  AND (? IS NULL OR v.cidade LIKE '%' || ? || '%')
  AND (? IS NULL OR v.uf = ?)
  AND (? IS NULL OR v.modalidade = ?)
  AND (? IS NULL OR v.salario >= ?)
  AND v.status_vaga = 'aberta'
ORDER BY v.data_cadastro DESC
LIMIT ? OFFSET ?
"""

OBTER_QUANTIDADE = "SELECT COUNT(*) as quantidade FROM vaga"

OBTER_QUANTIDADE_POR_STATUS = """
SELECT COUNT(*) as quantidade FROM vaga WHERE status_vaga = ?
"""

OBTER_VAGAS_ABERTAS = """
SELECT v.*,
       a.nome as area_nome,
       e.nome as empresa_nome
FROM vaga v
LEFT JOIN area a ON v.id_area = a.id_area
LEFT JOIN empresa e ON v.id_empresa = e.id_empresa
WHERE v.status_vaga = 'aberta'
ORDER BY v.data_cadastro DESC
LIMIT ? OFFSET ?
"""