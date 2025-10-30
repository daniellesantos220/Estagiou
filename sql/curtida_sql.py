CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS curtida (
    id_usuario INTEGER NOT NULL,
    id_vaga INTEGER NOT NULL,
    data_curtida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_usuario, id_vaga),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id),
    FOREIGN KEY (id_vaga) REFERENCES vaga(id)
)
"""

INSERIR = "INSERT INTO curtida (id_usuario, id_vaga) VALUES (?, ?)"
EXCLUIR = "DELETE FROM curtida WHERE id_usuario = ? AND id_vaga = ?"
OBTER_POR_ID = "SELECT * FROM curtida WHERE id_usuario = ? AND id_vaga = ?"
OBTER_QUANTIDADE_POR_VAGA = "SELECT COUNT(*) AS quantidade FROM curtida WHERE id_vaga = ?"