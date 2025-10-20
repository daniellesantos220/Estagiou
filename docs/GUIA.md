# 📘 GUIA COMPLETO DE IMPLEMENTAÇÃO - ESTAGIOU

> Guia didático passo a passo para transformar o DefaultWebApp no Estagiou

**Versão:** 1.0
**Data:** 2025-10-20
**Tempo Estimado Total:** 6-8 semanas

---

## 📑 ÍNDICE

- [FASE 1: Fundação](#fase-1-fundação)
  - [1.1 Ajustar Perfis de Usuário](#11-ajustar-perfis-de-usuário)
  - [1.2 Completar Models](#12-completar-models)
  - [1.3 Criar Arquivos SQL](#13-criar-arquivos-sql)
  - [1.4 Criar Repositories](#14-criar-repositories)
  - [1.5 Criar DTOs](#15-criar-dtos)

- [FASE 2: Funcionalidades Core](#fase-2-funcionalidades-core)
  - [2.1 Rotas Públicas](#21-rotas-públicas)
  - [2.2 Rotas de Estudante](#22-rotas-de-estudante)
  - [2.3 Templates Públicos](#23-templates-públicos)

---

# FASE 1: FUNDAÇÃO

Duração estimada: 1-2 semanas

Esta fase estabelece a base de dados e estruturas fundamentais do Estagiou.

---

## 1.1 Ajustar Perfis de Usuário

### 📝 Objetivo
Adaptar o sistema de perfis para os três tipos de usuários do Estagiou: Administrador, Estudante e Recrutador.

### 📂 Arquivo a Modificar
`util/perfis.py`

### ✏️ O que fazer

1. **Abra o arquivo** `util/perfis.py`

2. **Substitua os perfis existentes:**

```python
# ANTES (remover):
ADMIN = "Administrador"
CLIENTE = "Cliente"
VENDEDOR = "Vendedor"

# DEPOIS (usar):
ADMIN = "Administrador"
ESTUDANTE = "Estudante"
RECRUTADOR = "Recrutador"
```

3. **Resultado final do Enum:**

```python
from enum import Enum
from typing import Optional

class Perfil(str, Enum):
    """
    Enum centralizado para perfis de usuário do Estagiou.

    Perfis disponíveis:
    - ADMIN: Administrador da plataforma
    - ESTUDANTE: Estudante buscando estágios
    - RECRUTADOR: Recrutador de empresa
    """

    # PERFIS DO ESTAGIOU
    ADMIN = "Administrador"
    ESTUDANTE = "Estudante"
    RECRUTADOR = "Recrutador"

    # Manter todos os métodos existentes (valores, existe, from_string, validar)
    # Não precisa modificar nada abaixo desta linha
```

### ✅ Verificação
- [ ] Arquivo modificado
- [ ] Sistema inicializa sem erros
- [ ] Seeds de usuários ainda funcionam (serão atualizados depois)

---

## 1.2 Completar Models

### 📝 Objetivo
Adicionar campos específicos do Estagiou aos models existentes.

---

### 1.2.1 Model Usuario - Adicionar Campos de Estudante

### 📂 Arquivo a Modificar
`model/usuario_model.py`

### ✏️ O que fazer

1. **Adicione os imports necessários:**

```python
from dataclasses import dataclass
from typing import Optional
from datetime import date  # ADICIONAR ESTA LINHA
from util.perfis import Perfil
```

2. **Adicione os novos campos ao dataclass Usuario:**

```python
@dataclass
class Usuario:
    """
    Model de usuário do sistema Estagiou.

    Campos comuns a todos os perfis:
        id, nome, email, senha, perfil, token_redefinicao, data_token, data_cadastro

    Campos específicos de ESTUDANTE:
        cpf, telefone, data_nascimento, curso, instituicao, periodo,
        curriculo_arquivo, habilidades

    Campos específicos de RECRUTADOR:
        cpf, telefone, id_empresa (relacionamento)
    """
    # Campos existentes (NÃO MODIFICAR)
    id: int
    nome: str
    email: str
    senha: str
    perfil: str
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None
    data_cadastro: Optional[str] = None

    # NOVOS CAMPOS - ADICIONAR ABAIXO:

    # Campos comuns (Estudante e Recrutador)
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None

    # Campos específicos de Estudante
    curso: Optional[str] = None
    instituicao: Optional[str] = None
    periodo: Optional[str] = None
    curriculo_arquivo: Optional[str] = None  # Caminho do PDF: /static/curriculos/{id:06d}.pdf
    habilidades: Optional[str] = None  # JSON ou texto separado por vírgula

    # Campos específicos de Recrutador
    id_empresa: Optional[int] = None  # FK para tabela empresa
```

### ✅ Verificação
- [ ] Campos adicionados
- [ ] Imports corretos
- [ ] Sistema inicializa sem erros

---

### 1.2.2 Model Empresa - Completar Campos

### 📂 Arquivo a Modificar
`model/empresa_model.py`

### ✏️ O que fazer

1. **Adicione os imports:**

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
```

2. **Substitua o dataclass completo:**

```python
@dataclass
class Empresa:
    """
    Model de empresa no sistema Estagiou.

    Relacionamentos:
        - Uma empresa tem vários recrutadores (Usuario com perfil RECRUTADOR)
        - Uma empresa tem várias vagas
    """
    # Identificação
    id_empresa: int
    nome: str
    cnpj: str  # Alterado de int para str para manter formatação
    descricao: str

    # Contato
    setor: Optional[str] = None
    site: Optional[str] = None
    telefone: Optional[str] = None
    email_contato: Optional[str] = None

    # Mídia
    logo: Optional[str] = None  # Caminho: /static/img/empresas/{id:06d}.jpg

    # Plano e Limites
    plano: str = "Público"  # Público, Básico, Intermediário, Avançado
    vagas_mensais_limite: int = 2  # Limite por plano
    vagas_publicadas_mes: int = 0  # Contador do mês atual

    # Auditoria
    data_cadastro: Optional[datetime] = None
    ativo: bool = True
```

### ✅ Verificação
- [ ] Campos adicionados
- [ ] Tipo do CNPJ alterado para str
- [ ] Campos de plano adicionados

---

### 1.2.3 Model Vaga - Ajustar e Completar

### 📂 Arquivo a Modificar
`model/vaga_model.py`

### ✏️ O que fazer

1. **Substitua o conteúdo completo:**

```python
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

from model.area_model import Area
from model.empresa_model import Empresa
from model.usuario_model import Usuario


@dataclass
class Vaga:
    """
    Model de vaga de estágio no sistema Estagiou.

    Relacionamentos:
        - Pertence a uma Empresa
        - Pertence a uma Área
        - Foi criada por um Recrutador (Usuario)
        - Tem várias Candidaturas
    """
    # Identificação
    id_vaga: int
    id_area: int
    id_empresa: int
    id_recrutador: int

    # Informações principais
    titulo: str
    descricao: str
    requisitos: str

    # Detalhes da vaga
    numero_vagas: int
    salario: float
    beneficios: Optional[str] = None
    carga_horaria: str = "20h semanais"  # Ex: "20h semanais", "6h diárias"
    modalidade: str = "Presencial"  # Presencial, Remoto, Híbrido

    # Localização
    cidade: str = ""
    estado: str = ""

    # Status e controle
    status_vaga: str = "aberta"  # aberta, em_analise, encerrada, arquivada
    destaque: bool = False  # Apenas para planos pagos
    visualizacoes: int = 0

    # Prazos
    prazo_candidatura: Optional[date] = None
    data_cadastro: Optional[datetime] = None

    # Relacionamentos (preenchidos por JOIN)
    area: Optional[Area] = None
    empresa: Optional[Empresa] = None
    recrutador: Optional[Usuario] = None
```

### ✅ Verificação
- [ ] Todos os campos adicionados
- [ ] Relacionamentos mantidos
- [ ] Campos de localização e modalidade adicionados

---

### 1.2.4 Model Candidatura - Ajustar Status

### 📂 Arquivo a Modificar
`model/candidatura_model.py`

### ✏️ O que fazer

1. **Substitua o conteúdo:**

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from model.usuario_model import Usuario
from model.vaga_model import Vaga


@dataclass
class Candidatura:
    """
    Model de candidatura a uma vaga.

    Relacionamentos:
        - Pertence a uma Vaga
        - Pertence a um Candidato (Usuario com perfil ESTUDANTE)
    """
    id_candidatura: int
    id_vaga: int
    id_candidato: int
    data_candidatura: datetime

    # Status possíveis: "em_analise", "entrevista_agendada", "aprovado", "reprovado"
    status: str = "em_analise"  # Corrigido de "Status" para "status" (lowercase)

    # Observações do recrutador
    observacoes: Optional[str] = None

    # Relacionamentos (preenchidos por JOIN)
    vaga: Optional[Vaga] = None
    candidato: Optional[Usuario] = None
```

### ✅ Verificação
- [ ] Campo "Status" renomeado para "status" (lowercase)
- [ ] Campo observacoes adicionado
- [ ] Comentários sobre status possíveis adicionados

---

### 1.2.5 Models Auxiliares - Verificar

Os models `Area` e `Endereco` já estão adequados, mas vamos verificar:

### 📂 Arquivo: `model/area_model.py`
**Status:** ✅ OK - Não precisa modificar

### 📂 Arquivo: `model/endereco_model.py`
**Status:** ✅ OK - Não precisa modificar

---

## 1.3 Criar Arquivos SQL

### 📝 Objetivo
Criar os arquivos SQL com as queries para gerenciar as tabelas do banco de dados.

---

### 1.3.1 SQL de Empresa

### 📂 Arquivo a Criar
`sql/empresa_sql.py`

### ✏️ Passo a Passo

1. **Crie o arquivo** `sql/empresa_sql.py`

2. **Adicione o seguinte conteúdo:**

```python
"""
Queries SQL para a tabela empresa.
"""

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS empresa (
    id_empresa INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cnpj TEXT NOT NULL UNIQUE,
    descricao TEXT,
    setor TEXT,
    site TEXT,
    telefone TEXT,
    email_contato TEXT,
    logo TEXT,
    plano TEXT NOT NULL DEFAULT 'Público',
    vagas_mensais_limite INTEGER NOT NULL DEFAULT 2,
    vagas_publicadas_mes INTEGER NOT NULL DEFAULT 0,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    ativo INTEGER NOT NULL DEFAULT 1
)
"""

INSERIR = """
INSERT INTO empresa (
    nome, cnpj, descricao, setor, site, telefone, email_contato,
    plano, vagas_mensais_limite
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT * FROM empresa
WHERE ativo = 1
ORDER BY nome
"""

OBTER_POR_ID = """
SELECT * FROM empresa
WHERE id_empresa = ?
"""

OBTER_POR_CNPJ = """
SELECT * FROM empresa
WHERE cnpj = ?
"""

ATUALIZAR = """
UPDATE empresa
SET nome = ?, descricao = ?, setor = ?, site = ?,
    telefone = ?, email_contato = ?
WHERE id_empresa = ?
"""

ATUALIZAR_LOGO = """
UPDATE empresa
SET logo = ?
WHERE id_empresa = ?
"""

ATUALIZAR_PLANO = """
UPDATE empresa
SET plano = ?, vagas_mensais_limite = ?
WHERE id_empresa = ?
"""

INCREMENTAR_CONTADOR_VAGAS = """
UPDATE empresa
SET vagas_publicadas_mes = vagas_publicadas_mes + 1
WHERE id_empresa = ?
"""

RESETAR_CONTADOR_MENSAL = """
UPDATE empresa
SET vagas_publicadas_mes = 0
"""

DESATIVAR = """
UPDATE empresa
SET ativo = 0
WHERE id_empresa = ?
"""

EXCLUIR = """
DELETE FROM empresa
WHERE id_empresa = ?
"""
```

### ✅ Verificação
- [ ] Arquivo criado em `sql/empresa_sql.py`
- [ ] Todas as queries definidas
- [ ] Queries usam prepared statements (?)

---

### 1.3.2 SQL de Vaga

### 📂 Arquivo a Criar
`sql/vaga_sql.py`

### ✏️ Passo a Passo

1. **Crie o arquivo** `sql/vaga_sql.py`

2. **Adicione o conteúdo:**

```python
"""
Queries SQL para a tabela vaga.
"""

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS vaga (
    id_vaga INTEGER PRIMARY KEY AUTOINCREMENT,
    id_area INTEGER NOT NULL,
    id_empresa INTEGER NOT NULL,
    id_recrutador INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    requisitos TEXT NOT NULL,
    numero_vagas INTEGER NOT NULL DEFAULT 1,
    salario REAL NOT NULL DEFAULT 0.0,
    beneficios TEXT,
    carga_horaria TEXT NOT NULL DEFAULT '20h semanais',
    modalidade TEXT NOT NULL DEFAULT 'Presencial',
    cidade TEXT,
    estado TEXT,
    status_vaga TEXT NOT NULL DEFAULT 'aberta',
    destaque INTEGER NOT NULL DEFAULT 0,
    visualizacoes INTEGER NOT NULL DEFAULT 0,
    prazo_candidatura DATE,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_area) REFERENCES area(id_area),
    FOREIGN KEY (id_empresa) REFERENCES empresa(id_empresa),
    FOREIGN KEY (id_recrutador) REFERENCES usuario(id)
)
"""

INSERIR = """
INSERT INTO vaga (
    id_area, id_empresa, id_recrutador, titulo, descricao, requisitos,
    numero_vagas, salario, beneficios, carga_horaria, modalidade,
    cidade, estado, prazo_candidatura
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODAS = """
SELECT v.*,
       a.nome as area_nome,
       e.nome as empresa_nome, e.logo as empresa_logo,
       u.nome as recrutador_nome
FROM vaga v
LEFT JOIN area a ON v.id_area = a.id_area
LEFT JOIN empresa e ON v.id_empresa = e.id_empresa
LEFT JOIN usuario u ON v.id_recrutador = u.id
ORDER BY v.data_cadastro DESC
"""

OBTER_ABERTAS = """
SELECT v.*,
       a.nome as area_nome,
       e.nome as empresa_nome, e.logo as empresa_logo
FROM vaga v
LEFT JOIN area a ON v.id_area = a.id_area
LEFT JOIN empresa e ON v.id_empresa = e.id_empresa
WHERE v.status_vaga = 'aberta'
ORDER BY v.destaque DESC, v.data_cadastro DESC
"""

OBTER_POR_ID = """
SELECT v.*,
       a.nome as area_nome, a.descricao as area_descricao,
       e.nome as empresa_nome, e.logo as empresa_logo,
       e.descricao as empresa_descricao, e.setor as empresa_setor,
       u.nome as recrutador_nome
FROM vaga v
LEFT JOIN area a ON v.id_area = a.id_area
LEFT JOIN empresa e ON v.id_empresa = e.id_empresa
LEFT JOIN usuario u ON v.id_recrutador = u.id
WHERE v.id_vaga = ?
"""

OBTER_POR_EMPRESA = """
SELECT v.*, a.nome as area_nome
FROM vaga v
LEFT JOIN area a ON v.id_area = a.id_area
WHERE v.id_empresa = ?
ORDER BY v.data_cadastro DESC
"""

OBTER_POR_RECRUTADOR = """
SELECT v.*, a.nome as area_nome
FROM vaga v
LEFT JOIN area a ON v.id_area = a.id_area
WHERE v.id_recrutador = ?
ORDER BY v.data_cadastro DESC
"""

BUSCAR_COM_FILTROS = """
SELECT v.*,
       a.nome as area_nome,
       e.nome as empresa_nome, e.logo as empresa_logo
FROM vaga v
LEFT JOIN area a ON v.id_area = a.id_area
LEFT JOIN empresa e ON v.id_empresa = e.id_empresa
WHERE v.status_vaga = 'aberta'
{filtros}
ORDER BY v.destaque DESC, v.data_cadastro DESC
LIMIT ? OFFSET ?
"""

CONTAR_COM_FILTROS = """
SELECT COUNT(*) as total
FROM vaga v
WHERE v.status_vaga = 'aberta'
{filtros}
"""

ATUALIZAR = """
UPDATE vaga
SET titulo = ?, descricao = ?, requisitos = ?, numero_vagas = ?,
    salario = ?, beneficios = ?, carga_horaria = ?, modalidade = ?,
    cidade = ?, estado = ?, prazo_candidatura = ?
WHERE id_vaga = ?
"""

ATUALIZAR_STATUS = """
UPDATE vaga
SET status_vaga = ?
WHERE id_vaga = ?
"""

ATUALIZAR_DESTAQUE = """
UPDATE vaga
SET destaque = ?
WHERE id_vaga = ?
"""

INCREMENTAR_VISUALIZACOES = """
UPDATE vaga
SET visualizacoes = visualizacoes + 1
WHERE id_vaga = ?
"""

EXCLUIR = """
DELETE FROM vaga
WHERE id_vaga = ?
"""
```

### ✅ Verificação
- [ ] Arquivo criado
- [ ] CRIAR_TABELA com FKs
- [ ] Queries com JOINs para trazer informações relacionadas
- [ ] Query de busca com filtros dinâmicos

---

### 1.3.3 SQL de Candidatura

### 📂 Arquivo a Criar
`sql/candidatura_sql.py`

### ✏️ Passo a Passo

1. **Crie o arquivo** `sql/candidatura_sql.py`

2. **Adicione o conteúdo:**

```python
"""
Queries SQL para a tabela candidatura.
"""

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS candidatura (
    id_candidatura INTEGER PRIMARY KEY AUTOINCREMENT,
    id_vaga INTEGER NOT NULL,
    id_candidato INTEGER NOT NULL,
    data_candidatura DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'em_analise',
    observacoes TEXT,
    FOREIGN KEY (id_vaga) REFERENCES vaga(id_vaga),
    FOREIGN KEY (id_candidato) REFERENCES usuario(id),
    UNIQUE(id_vaga, id_candidato)
)
"""

INSERIR = """
INSERT INTO candidatura (id_vaga, id_candidato)
VALUES (?, ?)
"""

OBTER_POR_ID = """
SELECT c.*,
       v.titulo as vaga_titulo, v.salario as vaga_salario,
       v.cidade as vaga_cidade, v.estado as vaga_estado,
       e.nome as empresa_nome, e.logo as empresa_logo,
       u.nome as candidato_nome, u.email as candidato_email,
       u.telefone as candidato_telefone, u.curso as candidato_curso
FROM candidatura c
LEFT JOIN vaga v ON c.id_vaga = v.id_vaga
LEFT JOIN empresa e ON v.id_empresa = e.id_empresa
LEFT JOIN usuario u ON c.id_candidato = u.id
WHERE c.id_candidatura = ?
"""

OBTER_POR_ESTUDANTE = """
SELECT c.*,
       v.titulo as vaga_titulo, v.salario as vaga_salario,
       v.status_vaga as vaga_status,
       e.nome as empresa_nome, e.logo as empresa_logo
FROM candidatura c
LEFT JOIN vaga v ON c.id_vaga = v.id_vaga
LEFT JOIN empresa e ON v.id_empresa = e.id_empresa
WHERE c.id_candidato = ?
ORDER BY c.data_candidatura DESC
"""

OBTER_POR_VAGA = """
SELECT c.*,
       u.nome as candidato_nome, u.email as candidato_email,
       u.telefone as candidato_telefone, u.curso as candidato_curso,
       u.instituicao as candidato_instituicao, u.periodo as candidato_periodo,
       u.curriculo_arquivo as candidato_curriculo
FROM candidatura c
LEFT JOIN usuario u ON c.id_candidato = u.id
WHERE c.id_vaga = ?
ORDER BY c.data_candidatura DESC
"""

OBTER_POR_EMPRESA = """
SELECT c.*,
       v.titulo as vaga_titulo,
       u.nome as candidato_nome, u.email as candidato_email,
       u.curso as candidato_curso
FROM candidatura c
LEFT JOIN vaga v ON c.id_vaga = v.id_vaga
LEFT JOIN usuario u ON c.id_candidato = u.id
WHERE v.id_empresa = ?
ORDER BY c.data_candidatura DESC
"""

VERIFICAR_CANDIDATURA_EXISTENTE = """
SELECT id_candidatura
FROM candidatura
WHERE id_vaga = ? AND id_candidato = ?
"""

ATUALIZAR_STATUS = """
UPDATE candidatura
SET status = ?, observacoes = ?
WHERE id_candidatura = ?
"""

EXCLUIR = """
DELETE FROM candidatura
WHERE id_candidatura = ?
"""

CONTAR_POR_VAGA = """
SELECT COUNT(*) as total
FROM candidatura
WHERE id_vaga = ?
"""

CONTAR_POR_STATUS = """
SELECT status, COUNT(*) as total
FROM candidatura
WHERE id_vaga = ?
GROUP BY status
"""
```

### ✅ Verificação
- [ ] Arquivo criado
- [ ] UNIQUE constraint para evitar candidaturas duplicadas
- [ ] Queries com JOINs para dados relacionados
- [ ] Queries de contagem por status

---

### 1.3.4 SQL de Área

### 📂 Arquivo a Criar
`sql/area_sql.py`

### ✏️ Passo a Passo

1. **Crie o arquivo** `sql/area_sql.py`

2. **Adicione o conteúdo:**

```python
"""
Queries SQL para a tabela area.
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

OBTER_TODAS = """
SELECT * FROM area
ORDER BY nome
"""

OBTER_POR_ID = """
SELECT * FROM area
WHERE id_area = ?
"""

OBTER_POR_NOME = """
SELECT * FROM area
WHERE nome = ?
"""

ATUALIZAR = """
UPDATE area
SET nome = ?, descricao = ?
WHERE id_area = ?
"""

EXCLUIR = """
DELETE FROM area
WHERE id_area = ?
"""

CONTAR_VAGAS_POR_AREA = """
SELECT a.id_area, a.nome, COUNT(v.id_vaga) as total_vagas
FROM area a
LEFT JOIN vaga v ON a.id_area = v.id_area AND v.status_vaga = 'aberta'
GROUP BY a.id_area, a.nome
ORDER BY total_vagas DESC
"""
```

### ✅ Verificação
- [ ] Arquivo criado
- [ ] UNIQUE constraint no nome
- [ ] Query para contar vagas por área

---

### 1.3.5 SQL de Endereço

### 📂 Arquivo a Criar
`sql/endereco_sql.py`

### ✏️ Passo a Passo

1. **Crie o arquivo** `sql/endereco_sql.py`

2. **Adicione o conteúdo:**

```python
"""
Queries SQL para a tabela endereco.
"""

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS endereco (
    id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    logradouro TEXT NOT NULL,
    numero TEXT NOT NULL,
    complemento TEXT,
    bairro TEXT NOT NULL,
    cidade TEXT NOT NULL,
    uf TEXT NOT NULL,
    cep TEXT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
)
"""

INSERIR = """
INSERT INTO endereco (
    id_usuario, titulo, logradouro, numero, complemento,
    bairro, cidade, uf, cep
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT * FROM endereco
ORDER BY titulo
"""

OBTER_POR_ID = """
SELECT * FROM endereco
WHERE id_endereco = ?
"""

OBTER_POR_USUARIO = """
SELECT * FROM endereco
WHERE id_usuario = ?
ORDER BY titulo
"""

ATUALIZAR = """
UPDATE endereco
SET titulo = ?, logradouro = ?, numero = ?, complemento = ?,
    bairro = ?, cidade = ?, uf = ?, cep = ?
WHERE id_endereco = ?
"""

EXCLUIR = """
DELETE FROM endereco
WHERE id_endereco = ?
"""

EXCLUIR_POR_USUARIO = """
DELETE FROM endereco
WHERE id_usuario = ?
"""
```

### ✅ Verificação
- [ ] Arquivo criado
- [ ] FK para usuario
- [ ] Queries para obter endereços por usuário

---

### 1.3.6 Atualizar SQL de Usuario

### 📂 Arquivo a Modificar
`sql/usuario_sql.py`

### ✏️ O que fazer

1. **Abra o arquivo** `sql/usuario_sql.py`

2. **Localize a query CRIAR_TABELA e adicione os novos campos:**

```python
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    perfil TEXT NOT NULL,
    token_redefinicao TEXT,
    data_token DATETIME,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- NOVOS CAMPOS: adicionar aqui
    cpf TEXT,
    telefone TEXT,
    data_nascimento DATE,
    curso TEXT,
    instituicao TEXT,
    periodo TEXT,
    curriculo_arquivo TEXT,
    habilidades TEXT,
    id_empresa INTEGER,

    FOREIGN KEY (id_empresa) REFERENCES empresa(id_empresa)
)
"""
```

3. **Adicione uma nova query para atualizar perfil de estudante:**

```python
# Adicionar no final do arquivo

ATUALIZAR_PERFIL_ESTUDANTE = """
UPDATE usuario
SET nome = ?, cpf = ?, telefone = ?, data_nascimento = ?,
    curso = ?, instituicao = ?, periodo = ?, habilidades = ?
WHERE id = ?
"""

ATUALIZAR_CURRICULO = """
UPDATE usuario
SET curriculo_arquivo = ?
WHERE id = ?
"""

ATUALIZAR_EMPRESA_RECRUTADOR = """
UPDATE usuario
SET id_empresa = ?
WHERE id = ?
"""

OBTER_RECRUTADORES_POR_EMPRESA = """
SELECT * FROM usuario
WHERE id_empresa = ? AND perfil = 'Recrutador'
ORDER BY nome
"""
```

### ✅ Verificação
- [ ] Campos adicionados à CRIAR_TABELA
- [ ] Queries de atualização específicas criadas
- [ ] FK para empresa adicionada

---

## 1.4 Criar Repositories

### 📝 Objetivo
Criar os repositories que implementam a lógica de acesso ao banco de dados.

---

### 1.4.1 Repository de Empresa

### 📂 Arquivo a Criar
`repo/empresa_repo.py`

### ✏️ Passo a Passo

**IMPORTANTE:** Siga o padrão dos repositories existentes (`usuario_repo.py`, `tarefa_repo.py`)

1. **Crie o arquivo** `repo/empresa_repo.py`

2. **Estrutura básica:**

```python
"""
Repository para operações com empresas.
Padrão: Model ↔ Repository ↔ Database
"""

from typing import List, Optional
from datetime import datetime

from model.empresa_model import Empresa
from sql.empresa_sql import *
from util.db_util import get_connection


def _row_to_empresa(row) -> Empresa:
    """
    Converte uma linha do banco em objeto Empresa.

    Args:
        row: Row do SQLite

    Returns:
        Objeto Empresa preenchido
    """
    return Empresa(
        id_empresa=row["id_empresa"],
        nome=row["nome"],
        cnpj=row["cnpj"],
        descricao=row["descricao"],
        setor=row["setor"],
        site=row["site"],
        telefone=row["telefone"],
        email_contato=row["email_contato"],
        logo=row["logo"],
        plano=row["plano"],
        vagas_mensais_limite=row["vagas_mensais_limite"],
        vagas_publicadas_mes=row["vagas_publicadas_mes"],
        data_cadastro=row["data_cadastro"],
        ativo=bool(row["ativo"])
    )


def criar_tabela():
    """Cria a tabela empresa se não existir."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)


def inserir(empresa: Empresa) -> int:
    """
    Insere uma nova empresa.

    Args:
        empresa: Objeto Empresa a inserir

    Returns:
        ID da empresa inserida
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            empresa.nome,
            empresa.cnpj,
            empresa.descricao,
            empresa.setor,
            empresa.site,
            empresa.telefone,
            empresa.email_contato,
            empresa.plano,
            empresa.vagas_mensais_limite
        ))
        return cursor.lastrowid


def obter_todos() -> List[Empresa]:
    """Retorna todas as empresas ativas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        return [_row_to_empresa(row) for row in cursor.fetchall()]


def obter_por_id(empresa_id: int) -> Optional[Empresa]:
    """Retorna uma empresa pelo ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (empresa_id,))
        row = cursor.fetchone()
        return _row_to_empresa(row) if row else None


def obter_por_cnpj(cnpj: str) -> Optional[Empresa]:
    """Retorna uma empresa pelo CNPJ."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_CNPJ, (cnpj,))
        row = cursor.fetchone()
        return _row_to_empresa(row) if row else None


def atualizar(empresa: Empresa):
    """Atualiza os dados de uma empresa."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            empresa.nome,
            empresa.descricao,
            empresa.setor,
            empresa.site,
            empresa.telefone,
            empresa.email_contato,
            empresa.id_empresa
        ))


def atualizar_logo(empresa_id: int, logo_path: str):
    """Atualiza o caminho da logo da empresa."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_LOGO, (logo_path, empresa_id))


def atualizar_plano(empresa_id: int, plano: str, vagas_limite: int):
    """Atualiza o plano da empresa e seu limite de vagas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_PLANO, (plano, vagas_limite, empresa_id))


def incrementar_contador_vagas(empresa_id: int):
    """Incrementa o contador de vagas publicadas no mês."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INCREMENTAR_CONTADOR_VAGAS, (empresa_id,))


def resetar_contador_mensal():
    """Reseta o contador mensal de todas as empresas (executar via cronjob)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(RESETAR_CONTADOR_MENSAL)


def pode_publicar_vaga(empresa_id: int) -> bool:
    """
    Verifica se a empresa pode publicar mais vagas no mês.

    Returns:
        True se ainda tem vagas disponíveis, False caso contrário
    """
    empresa = obter_por_id(empresa_id)
    if not empresa:
        return False
    return empresa.vagas_publicadas_mes < empresa.vagas_mensais_limite


def desativar(empresa_id: int):
    """Desativa uma empresa (soft delete)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DESATIVAR, (empresa_id,))


def excluir(empresa_id: int):
    """Exclui permanentemente uma empresa."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (empresa_id,))
```

### 💡 Dicas

- **Sempre use `get_connection()`** do `util/db_util`
- **Função `_row_to_model`** converte row em objeto
- **Use `cursor.lastrowid`** para pegar ID inserido
- **Funções específicas** (como `pode_publicar_vaga`) agregam valor

### ✅ Verificação
- [ ] Arquivo criado
- [ ] Todas as funções implementadas
- [ ] Usa pattern do projeto
- [ ] Imports corretos

---

### 1.4.2 Repository de Vaga

### 📂 Arquivo a Criar
`repo/vaga_repo.py`

### ✏️ Estrutura Completa

```python
"""
Repository para operações com vagas.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date

from model.vaga_model import Vaga
from model.area_model import Area
from model.empresa_model import Empresa
from model.usuario_model import Usuario
from sql.vaga_sql import *
from util.db_util import get_connection


def _row_to_vaga(row) -> Vaga:
    """Converte row do banco em objeto Vaga com relacionamentos."""

    # Criar objetos relacionados se houver dados
    area = None
    if row.get("area_nome"):
        area = Area(
            id_area=row["id_area"],
            nome=row["area_nome"],
            descricao=row.get("area_descricao")
        )

    empresa = None
    if row.get("empresa_nome"):
        empresa = Empresa(
            id_empresa=row["id_empresa"],
            nome=row["empresa_nome"],
            cnpj="",  # Não incluído no JOIN
            descricao=row.get("empresa_descricao", ""),
            setor=row.get("empresa_setor"),
            logo=row.get("empresa_logo")
        )

    recrutador = None
    if row.get("recrutador_nome"):
        recrutador = Usuario(
            id=row["id_recrutador"],
            nome=row["recrutador_nome"],
            email="",  # Não incluído no JOIN
            senha="",
            perfil="Recrutador"
        )

    return Vaga(
        id_vaga=row["id_vaga"],
        id_area=row["id_area"],
        id_empresa=row["id_empresa"],
        id_recrutador=row["id_recrutador"],
        titulo=row["titulo"],
        descricao=row["descricao"],
        requisitos=row["requisitos"],
        numero_vagas=row["numero_vagas"],
        salario=row["salario"],
        beneficios=row["beneficios"],
        carga_horaria=row["carga_horaria"],
        modalidade=row["modalidade"],
        cidade=row["cidade"],
        estado=row["estado"],
        status_vaga=row["status_vaga"],
        destaque=bool(row["destaque"]),
        visualizacoes=row["visualizacoes"],
        prazo_candidatura=row["prazo_candidatura"],
        data_cadastro=row["data_cadastro"],
        area=area,
        empresa=empresa,
        recrutador=recrutador
    )


def criar_tabela():
    """Cria a tabela vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)


def inserir(vaga: Vaga) -> int:
    """Insere uma nova vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            vaga.id_area,
            vaga.id_empresa,
            vaga.id_recrutador,
            vaga.titulo,
            vaga.descricao,
            vaga.requisitos,
            vaga.numero_vagas,
            vaga.salario,
            vaga.beneficios,
            vaga.carga_horaria,
            vaga.modalidade,
            vaga.cidade,
            vaga.estado,
            vaga.prazo_candidatura
        ))
        return cursor.lastrowid


def obter_todas() -> List[Vaga]:
    """Retorna todas as vagas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        return [_row_to_vaga(row) for row in cursor.fetchall()]


def obter_abertas() -> List[Vaga]:
    """Retorna apenas vagas abertas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ABERTAS)
        return [_row_to_vaga(row) for row in cursor.fetchall()]


def obter_por_id(vaga_id: int) -> Optional[Vaga]:
    """Retorna uma vaga pelo ID com todos os relacionamentos."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (vaga_id,))
        row = cursor.fetchone()
        return _row_to_vaga(row) if row else None


def obter_por_empresa(empresa_id: int) -> List[Vaga]:
    """Retorna todas as vagas de uma empresa."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_EMPRESA, (empresa_id,))
        return [_row_to_vaga(row) for row in cursor.fetchall()]


def obter_por_recrutador(recrutador_id: int) -> List[Vaga]:
    """Retorna todas as vagas criadas por um recrutador."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_RECRUTADOR, (recrutador_id,))
        return [_row_to_vaga(row) for row in cursor.fetchall()]


def buscar_com_filtros(
    area_id: Optional[int] = None,
    cidade: Optional[str] = None,
    estado: Optional[str] = None,
    modalidade: Optional[str] = None,
    salario_min: Optional[float] = None,
    salario_max: Optional[float] = None,
    termo_busca: Optional[str] = None,
    limite: int = 20,
    offset: int = 0
) -> tuple[List[Vaga], int]:
    """
    Busca vagas com filtros dinâmicos.

    Returns:
        Tupla (lista de vagas, total de resultados)
    """
    filtros = []
    params = []

    if area_id:
        filtros.append("AND v.id_area = ?")
        params.append(area_id)

    if cidade:
        filtros.append("AND LOWER(v.cidade) LIKE LOWER(?)")
        params.append(f"%{cidade}%")

    if estado:
        filtros.append("AND v.estado = ?")
        params.append(estado)

    if modalidade:
        filtros.append("AND v.modalidade = ?")
        params.append(modalidade)

    if salario_min is not None:
        filtros.append("AND v.salario >= ?")
        params.append(salario_min)

    if salario_max is not None:
        filtros.append("AND v.salario <= ?")
        params.append(salario_max)

    if termo_busca:
        filtros.append("""
            AND (LOWER(v.titulo) LIKE LOWER(?)
                 OR LOWER(v.descricao) LIKE LOWER(?))
        """)
        termo = f"%{termo_busca}%"
        params.extend([termo, termo])

    filtros_sql = " ".join(filtros)

    with get_connection() as conn:
        cursor = conn.cursor()

        # Contar total
        count_query = CONTAR_COM_FILTROS.format(filtros=filtros_sql)
        cursor.execute(count_query, params)
        total = cursor.fetchone()["total"]

        # Buscar vagas
        params_busca = params + [limite, offset]
        busca_query = BUSCAR_COM_FILTROS.format(filtros=filtros_sql)
        cursor.execute(busca_query, params_busca)
        vagas = [_row_to_vaga(row) for row in cursor.fetchall()]

        return vagas, total


def atualizar(vaga: Vaga):
    """Atualiza uma vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            vaga.titulo,
            vaga.descricao,
            vaga.requisitos,
            vaga.numero_vagas,
            vaga.salario,
            vaga.beneficios,
            vaga.carga_horaria,
            vaga.modalidade,
            vaga.cidade,
            vaga.estado,
            vaga.prazo_candidatura,
            vaga.id_vaga
        ))


def atualizar_status(vaga_id: int, status: str):
    """Atualiza o status de uma vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_STATUS, (status, vaga_id))


def atualizar_destaque(vaga_id: int, destaque: bool):
    """Ativa/desativa destaque de uma vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_DESTAQUE, (1 if destaque else 0, vaga_id))


def incrementar_visualizacoes(vaga_id: int):
    """Incrementa o contador de visualizações."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INCREMENTAR_VISUALIZACOES, (vaga_id,))


def excluir(vaga_id: int):
    """Exclui uma vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (vaga_id,))
```

### 💡 Destaque Especial

A função `buscar_com_filtros()` é a mais complexa. Ela:
1. Monta filtros SQL dinamicamente
2. Conta o total de resultados
3. Busca com paginação
4. Retorna tupla (vagas, total)

### ✅ Verificação
- [ ] Arquivo criado
- [ ] Função de busca com filtros implementada
- [ ] Relacionamentos preenchidos no _row_to_vaga
- [ ] Todas as operações CRUD

---

**Continua na próxima parte do guia...**

---

## 📌 Checkpoint da Fase 1 (Parte 1)

Até aqui você deve ter:

✅ Perfis ajustados (Estudante, Recrutador)
✅ Models completos com novos campos
✅ 6 arquivos SQL criados
✅ 2 repositories criados (Empresa, Vaga)

**Próximos passos:**
- [ ] Criar mais 3 repositories (Candidatura, Area, Endereco)
- [ ] Criar DTOs com validações
- [ ] Atualizar main.py
- [ ] Testar as tabelas

---

---

### 1.4.3 Repository de Candidatura

### 📂 Arquivo a Criar
`repo/candidatura_repo.py`

### ✏️ Estrutura Completa

```python
"""
Repository para operações com candidaturas.
"""

from typing import List, Optional, Dict
from datetime import datetime

from model.candidatura_model import Candidatura
from model.vaga_model import Vaga
from model.usuario_model import Usuario
from sql.candidatura_sql import *
from util.db_util import get_connection


def _row_to_candidatura(row) -> Candidatura:
    """Converte row em objeto Candidatura."""

    # Criar objetos relacionados se houver dados
    vaga = None
    if row.get("vaga_titulo"):
        vaga = Vaga(
            id_vaga=row["id_vaga"],
            id_area=0,
            id_empresa=0,
            id_recrutador=0,
            titulo=row["vaga_titulo"],
            descricao="",
            requisitos="",
            numero_vagas=0,
            salario=row.get("vaga_salario", 0.0),
            cidade=row.get("vaga_cidade", ""),
            estado=row.get("vaga_estado", ""),
            status_vaga=row.get("vaga_status", "aberta")
        )

    candidato = None
    if row.get("candidato_nome"):
        candidato = Usuario(
            id=row["id_candidato"],
            nome=row["candidato_nome"],
            email=row.get("candidato_email", ""),
            senha="",
            perfil="Estudante",
            telefone=row.get("candidato_telefone"),
            curso=row.get("candidato_curso"),
            instituicao=row.get("candidato_instituicao"),
            periodo=row.get("candidato_periodo"),
            curriculo_arquivo=row.get("candidato_curriculo")
        )

    return Candidatura(
        id_candidatura=row["id_candidatura"],
        id_vaga=row["id_vaga"],
        id_candidato=row["id_candidato"],
        data_candidatura=row["data_candidatura"],
        status=row["status"],
        observacoes=row["observacoes"],
        vaga=vaga,
        candidato=candidato
    )


def criar_tabela():
    """Cria a tabela candidatura."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)


def inserir(candidatura: Candidatura) -> int:
    """Insere uma nova candidatura."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            candidatura.id_vaga,
            candidatura.id_candidato
        ))
        return cursor.lastrowid


def obter_por_id(candidatura_id: int) -> Optional[Candidatura]:
    """Retorna uma candidatura pelo ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (candidatura_id,))
        row = cursor.fetchone()
        return _row_to_candidatura(row) if row else None


def obter_por_estudante(estudante_id: int) -> List[Candidatura]:
    """Retorna todas as candidaturas de um estudante."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ESTUDANTE, (estudante_id,))
        return [_row_to_candidatura(row) for row in cursor.fetchall()]


def obter_por_vaga(vaga_id: int) -> List[Candidatura]:
    """Retorna todas as candidaturas de uma vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_VAGA, (vaga_id,))
        return [_row_to_candidatura(row) for row in cursor.fetchall()]


def obter_por_empresa(empresa_id: int) -> List[Candidatura]:
    """Retorna todas as candidaturas das vagas de uma empresa."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_EMPRESA, (empresa_id,))
        return [_row_to_candidatura(row) for row in cursor.fetchall()]


def verificar_candidatura_existente(vaga_id: int, candidato_id: int) -> bool:
    """Verifica se o candidato já se candidatou a esta vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(VERIFICAR_CANDIDATURA_EXISTENTE, (vaga_id, candidato_id))
        row = cursor.fetchone()
        return row is not None


def atualizar_status(candidatura_id: int, status: str, observacoes: Optional[str] = None):
    """Atualiza o status de uma candidatura."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_STATUS, (status, observacoes, candidatura_id))


def excluir(candidatura_id: int):
    """Exclui uma candidatura."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (candidatura_id,))


def contar_por_vaga(vaga_id: int) -> int:
    """Conta o total de candidaturas de uma vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONTAR_POR_VAGA, (vaga_id,))
        row = cursor.fetchone()
        return row["total"] if row else 0


def contar_por_status(vaga_id: int) -> Dict[str, int]:
    """
    Retorna contagem de candidaturas por status.

    Returns:
        Dict como {"em_analise": 5, "aprovado": 2, ...}
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONTAR_POR_STATUS, (vaga_id,))
        rows = cursor.fetchall()
        return {row["status"]: row["total"] for row in rows}
```

### ✅ Verificação
- [ ] Arquivo criado
- [ ] Verificação de candidatura duplicada
- [ ] Contadores por status
- [ ] Relacionamentos preenchidos

---

### 1.4.4 Repository de Área

### 📂 Arquivo a Criar
`repo/area_repo.py`

### ✏️ Estrutura (Simples)

```python
"""
Repository para operações com áreas.
"""

from typing import List, Optional, Dict
from model.area_model import Area
from sql.area_sql import *
from util.db_util import get_connection


def _row_to_area(row) -> Area:
    """Converte row em objeto Area."""
    return Area(
        id_area=row["id_area"],
        nome=row["nome"],
        descricao=row["descricao"]
    )


def criar_tabela():
    """Cria a tabela area."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)


def inserir(area: Area) -> int:
    """Insere uma nova área."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (area.nome, area.descricao))
        return cursor.lastrowid


def obter_todas() -> List[Area]:
    """Retorna todas as áreas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        return [_row_to_area(row) for row in cursor.fetchall()]


def obter_por_id(area_id: int) -> Optional[Area]:
    """Retorna uma área pelo ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (area_id,))
        row = cursor.fetchone()
        return _row_to_area(row) if row else None


def obter_por_nome(nome: str) -> Optional[Area]:
    """Retorna uma área pelo nome."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_NOME, (nome,))
        row = cursor.fetchone()
        return _row_to_area(row) if row else None


def atualizar(area: Area):
    """Atualiza uma área."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (area.nome, area.descricao, area.id_area))


def excluir(area_id: int):
    """Exclui uma área."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (area_id,))


def contar_vagas_por_area() -> List[Dict]:
    """
    Retorna estatísticas de vagas por área.

    Returns:
        Lista de dicts: [{"id_area": 1, "nome": "TI", "total_vagas": 10}, ...]
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONTAR_VAGAS_POR_AREA)
        return [dict(row) for row in cursor.fetchall()]
```

### ✅ Verificação
- [ ] CRUD completo
- [ ] Função de estatísticas

---

### 1.4.5 Repository de Endereço

### 📂 Arquivo a Criar
`repo/endereco_repo.py`

### ✏️ Estrutura (Simples)

```python
"""
Repository para operações com endereços.
"""

from typing import List, Optional
from model.endereco_model import Endereco
from sql.endereco_sql import *
from util.db_util import get_connection


def _row_to_endereco(row) -> Endereco:
    """Converte row em objeto Endereco."""
    return Endereco(
        id_endereco=row["id_endereco"],
        id_usuario=row["id_usuario"],
        titulo=row["titulo"],
        logradouro=row["logradouro"],
        numero=row["numero"],
        complemento=row["complemento"],
        bairro=row["bairro"],
        cidade=row["cidade"],
        uf=row["uf"],
        cep=row["cep"]
    )


def criar_tabela():
    """Cria a tabela endereco."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)


def inserir(endereco: Endereco) -> int:
    """Insere um novo endereço."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            endereco.id_usuario,
            endereco.titulo,
            endereco.logradouro,
            endereco.numero,
            endereco.complemento,
            endereco.bairro,
            endereco.cidade,
            endereco.uf,
            endereco.cep
        ))
        return cursor.lastrowid


def obter_todos() -> List[Endereco]:
    """Retorna todos os endereços."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        return [_row_to_endereco(row) for row in cursor.fetchall()]


def obter_por_id(endereco_id: int) -> Optional[Endereco]:
    """Retorna um endereço pelo ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (endereco_id,))
        row = cursor.fetchone()
        return _row_to_endereco(row) if row else None


def obter_por_usuario(usuario_id: int) -> List[Endereco]:
    """Retorna todos os endereços de um usuário."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_USUARIO, (usuario_id,))
        return [_row_to_endereco(row) for row in cursor.fetchall()]


def atualizar(endereco: Endereco):
    """Atualiza um endereço."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            endereco.titulo,
            endereco.logradouro,
            endereco.numero,
            endereco.complemento,
            endereco.bairro,
            endereco.cidade,
            endereco.uf,
            endereco.cep,
            endereco.id_endereco
        ))


def excluir(endereco_id: int):
    """Exclui um endereço."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (endereco_id,))


def excluir_por_usuario(usuario_id: int):
    """Exclui todos os endereços de um usuário."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR_POR_USUARIO, (usuario_id,))
```

### ✅ Verificação
- [ ] CRUD completo
- [ ] Queries por usuário

---

## 1.5 Criar DTOs

### 📝 Objetivo
Criar os DTOs (Data Transfer Objects) com validações usando Pydantic para garantir integridade dos dados.

---

### 1.5.1 DTO de Empresa

### 📂 Arquivo a Criar
`dtos/empresa_dto.py`

### ✏️ Estrutura Completa

```python
"""
DTOs para validação de dados de empresa.
Usa os validadores reutilizáveis de dtos/validators.py
"""

from pydantic import BaseModel, field_validator
from typing import Optional

from dtos.validators import (
    validar_string_obrigatoria,
    validar_cnpj,
    validar_email,
    validar_telefone_br
)


class EmpresaCriarDTO(BaseModel):
    """DTO para criação de empresa."""

    nome: str
    cnpj: str
    descricao: str
    setor: Optional[str] = None
    site: Optional[str] = None
    telefone: Optional[str] = None
    email_contato: Optional[str] = None

    # Validadores usando os validadores reutilizáveis
    _validar_nome = field_validator('nome')(
        validar_string_obrigatoria('Nome da Empresa', tamanho_minimo=3, tamanho_maximo=200)
    )

    _validar_cnpj = field_validator('cnpj')(validar_cnpj())

    _validar_descricao = field_validator('descricao')(
        validar_string_obrigatoria('Descrição', tamanho_minimo=10, tamanho_maximo=1000)
    )

    _validar_email = field_validator('email_contato')(validar_email())

    _validar_telefone = field_validator('telefone')(validar_telefone_br())


class EmpresaAlterarDTO(BaseModel):
    """DTO para alteração de empresa."""

    nome: str
    descricao: str
    setor: Optional[str] = None
    site: Optional[str] = None
    telefone: Optional[str] = None
    email_contato: Optional[str] = None

    _validar_nome = field_validator('nome')(
        validar_string_obrigatoria('Nome da Empresa', tamanho_minimo=3, tamanho_maximo=200)
    )

    _validar_descricao = field_validator('descricao')(
        validar_string_obrigatoria('Descrição', tamanho_minimo=10, tamanho_maximo=1000)
    )

    _validar_email = field_validator('email_contato')(validar_email())

    _validar_telefone = field_validator('telefone')(validar_telefone_br())
```

### 💡 Dica
Os validadores já existem em `dtos/validators.py`. Basta importar e usar!

---

### 1.5.2 DTO de Vaga

### 📂 Arquivo a Criar
`dtos/vaga_dto.py`

### ✏️ Estrutura Completa

```python
"""
DTOs para validação de dados de vaga.
"""

from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date

from dtos.validators import (
    validar_string_obrigatoria,
    validar_inteiro_positivo,
    validar_decimal_positivo,
    validar_data_futura
)


class VagaCriarDTO(BaseModel):
    """DTO para criação de vaga."""

    id_area: int
    titulo: str
    descricao: str
    requisitos: str
    numero_vagas: int
    salario: float
    beneficios: Optional[str] = None
    carga_horaria: str
    modalidade: str
    cidade: str
    estado: str
    prazo_candidatura: Optional[date] = None

    _validar_id_area = field_validator('id_area')(validar_inteiro_positivo())

    _validar_titulo = field_validator('titulo')(
        validar_string_obrigatoria('Título', tamanho_minimo=5, tamanho_maximo=200)
    )

    _validar_descricao = field_validator('descricao')(
        validar_string_obrigatoria('Descrição', tamanho_minimo=20, tamanho_maximo=2000)
    )

    _validar_requisitos = field_validator('requisitos')(
        validar_string_obrigatoria('Requisitos', tamanho_minimo=10, tamanho_maximo=1000)
    )

    _validar_numero_vagas = field_validator('numero_vagas')(validar_inteiro_positivo())

    _validar_salario = field_validator('salario')(validar_decimal_positivo())

    _validar_cidade = field_validator('cidade')(
        validar_string_obrigatoria('Cidade', tamanho_minimo=2, tamanho_maximo=100)
    )

    _validar_estado = field_validator('estado')(
        validar_string_obrigatoria('Estado', tamanho_minimo=2, tamanho_maximo=2)
    )

    _validar_prazo = field_validator('prazo_candidatura')(validar_data_futura())

    @field_validator('modalidade')
    @classmethod
    def validar_modalidade(cls, v: str) -> str:
        modalidades_validas = ['Presencial', 'Remoto', 'Híbrido']
        if v not in modalidades_validas:
            raise ValueError(f'Modalidade inválida. Use: {", ".join(modalidades_validas)}')
        return v


class VagaAlterarDTO(BaseModel):
    """DTO para alteração de vaga."""

    titulo: str
    descricao: str
    requisitos: str
    numero_vagas: int
    salario: float
    beneficios: Optional[str] = None
    carga_horaria: str
    modalidade: str
    cidade: str
    estado: str
    prazo_candidatura: Optional[date] = None

    # Mesmas validações do VagaCriarDTO
    _validar_titulo = field_validator('titulo')(
        validar_string_obrigatoria('Título', tamanho_minimo=5, tamanho_maximo=200)
    )

    _validar_descricao = field_validator('descricao')(
        validar_string_obrigatoria('Descrição', tamanho_minimo=20, tamanho_maximo=2000)
    )

    _validar_requisitos = field_validator('requisitos')(
        validar_string_obrigatoria('Requisitos', tamanho_minimo=10, tamanho_maximo=1000)
    )

    _validar_numero_vagas = field_validator('numero_vagas')(validar_inteiro_positivo())

    _validar_salario = field_validator('salario')(validar_decimal_positivo())

    @field_validator('modalidade')
    @classmethod
    def validar_modalidade(cls, v: str) -> str:
        modalidades_validas = ['Presencial', 'Remoto', 'Híbrido']
        if v not in modalidades_validas:
            raise ValueError(f'Modalidade inválida. Use: {", ".join(modalidades_validas)}')
        return v


class VagaBuscarDTO(BaseModel):
    """DTO para busca de vagas com filtros."""

    area_id: Optional[int] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    modalidade: Optional[str] = None
    salario_min: Optional[float] = None
    salario_max: Optional[float] = None
    termo_busca: Optional[str] = None
    pagina: int = 1
    por_pagina: int = 20

    @field_validator('pagina')
    @classmethod
    def validar_pagina(cls, v: int) -> int:
        if v < 1:
            raise ValueError('Página deve ser maior que 0')
        return v

    @field_validator('por_pagina')
    @classmethod
    def validar_por_pagina(cls, v: int) -> int:
        if v < 1 or v > 100:
            raise ValueError('Por página deve estar entre 1 e 100')
        return v
```

### 💡 Destaque
Note o `VagaBuscarDTO` para os filtros de busca. Isso mantém a validação centralizada.

---

### 1.5.3 DTO de Candidatura

### 📂 Arquivo a Criar
`dtos/candidatura_dto.py`

### ✏️ Estrutura

```python
"""
DTOs para validação de dados de candidatura.
"""

from pydantic import BaseModel, field_validator
from typing import Optional

from dtos.validators import validar_inteiro_positivo


class CandidaturaCriarDTO(BaseModel):
    """DTO para criação de candidatura."""

    id_vaga: int

    _validar_id_vaga = field_validator('id_vaga')(validar_inteiro_positivo())


class CandidaturaAtualizarStatusDTO(BaseModel):
    """DTO para atualização de status de candidatura."""

    status: str
    observacoes: Optional[str] = None

    @field_validator('status')
    @classmethod
    def validar_status(cls, v: str) -> str:
        status_validos = ['em_analise', 'entrevista_agendada', 'aprovado', 'reprovado']
        if v not in status_validos:
            raise ValueError(f'Status inválido. Use: {", ".join(status_validos)}')
        return v
```

---

### 1.5.4 DTO de Área

### 📂 Arquivo a Criar
`dtos/area_dto.py`

### ✏️ Estrutura

```python
"""
DTOs para validação de dados de área.
"""

from pydantic import BaseModel, field_validator
from typing import Optional

from dtos.validators import validar_string_obrigatoria


class AreaCriarDTO(BaseModel):
    """DTO para criação de área."""

    nome: str
    descricao: Optional[str] = None

    _validar_nome = field_validator('nome')(
        validar_string_obrigatoria('Nome da Área', tamanho_minimo=2, tamanho_maximo=100)
    )


class AreaAlterarDTO(BaseModel):
    """DTO para alteração de área."""

    nome: str
    descricao: Optional[str] = None

    _validar_nome = field_validator('nome')(
        validar_string_obrigatoria('Nome da Área', tamanho_minimo=2, tamanho_maximo=100)
    )
```

---

### 1.5.5 DTO de Estudante

### 📂 Arquivo a Criar
`dtos/estudante_dto.py`

### ✏️ Estrutura

```python
"""
DTOs para validação de dados específicos de estudante.
"""

from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date

from dtos.validators import (
    validar_string_obrigatoria,
    validar_cpf,
    validar_telefone_br,
    validar_data_passada
)


class EstudantePerfilDTO(BaseModel):
    """DTO para atualização de perfil de estudante."""

    nome: str
    cpf: str
    telefone: str
    data_nascimento: date
    curso: str
    instituicao: str
    periodo: str
    habilidades: Optional[str] = None

    _validar_nome = field_validator('nome')(
        validar_string_obrigatoria('Nome', tamanho_minimo=3, tamanho_maximo=200)
    )

    _validar_cpf = field_validator('cpf')(validar_cpf())

    _validar_telefone = field_validator('telefone')(validar_telefone_br())

    _validar_data_nascimento = field_validator('data_nascimento')(validar_data_passada())

    _validar_curso = field_validator('curso')(
        validar_string_obrigatoria('Curso', tamanho_minimo=3, tamanho_maximo=100)
    )

    _validar_instituicao = field_validator('instituicao')(
        validar_string_obrigatoria('Instituição', tamanho_minimo=3, tamanho_maximo=200)
    )

    _validar_periodo = field_validator('periodo')(
        validar_string_obrigatoria('Período', tamanho_minimo=1, tamanho_maximo=20)
    )
```

### ✅ Verificação dos DTOs
- [ ] Todos os 5 DTOs criados
- [ ] Validadores importados de validators.py
- [ ] Validações customizadas (modalidade, status) implementadas

---

## 1.6 Atualizar main.py

### 📝 Objetivo
Registrar as novas tabelas e routers no arquivo principal da aplicação.

### 📂 Arquivo a Modificar
`main.py`

### ✏️ O que fazer

1. **Adicione os imports dos novos repositories** (após a linha 23):

```python
# Repositórios EXISTENTES
from repo import usuario_repo, configuracao_repo, tarefa_repo

# NOVOS Repositórios - ADICIONAR ESTAS LINHAS:
from repo import empresa_repo, vaga_repo, candidatura_repo, area_repo, endereco_repo
```

2. **Adicione a criação das novas tabelas** (após a linha 66):

```python
# Tabelas existentes
logger.info("Criando tabelas do banco de dados...")
try:
    usuario_repo.criar_tabela()
    logger.info("Tabela 'usuario' criada/verificada")

    configuracao_repo.criar_tabela()
    logger.info("Tabela 'configuracao' criada/verificada")

    tarefa_repo.criar_tabela()
    logger.info("Tabela 'tarefa' criada/verificada")

    # NOVAS TABELAS - ADICIONAR ESTAS LINHAS:
    area_repo.criar_tabela()
    logger.info("Tabela 'area' criada/verificada")

    empresa_repo.criar_tabela()
    logger.info("Tabela 'empresa' criada/verificada")

    vaga_repo.criar_tabela()
    logger.info("Tabela 'vaga' criada/verificada")

    candidatura_repo.criar_tabela()
    logger.info("Tabela 'candidatura' criada/verificada")

    endereco_repo.criar_tabela()
    logger.info("Tabela 'endereco' criada/verificada")

except Exception as e:
    logger.error(f"Erro ao criar tabelas: {e}")
    raise
```

3. **Quando criar as rotas do Estagiou, adicione os imports** (você fará isso na Fase 2):

```python
# Rotas do Estagiou - ADICIONAR DEPOIS NA FASE 2
# from routes import estudante_routes, empresa_routes, public_vagas_routes
# from routes import admin_vagas_routes, admin_areas_routes
```

### ✅ Verificação
- [ ] Imports adicionados
- [ ] Criação de tabelas adicionada
- [ ] Sistema inicializa sem erros
- [ ] Verificar banco de dados criado

### 🧪 Testar

Execute a aplicação:

```bash
python main.py
```

Você deve ver no log:
```
INFO - Tabela 'area' criada/verificada
INFO - Tabela 'empresa' criada/verificada
INFO - Tabela 'vaga' criada/verificada
INFO - Tabela 'candidatura' criada/verificada
INFO - Tabela 'endereco' criada/verificada
```

---

## 1.7 Criar Seeds Iniciais (Opcional mas Recomendado)

### 📝 Objetivo
Criar dados iniciais para testar o sistema.

### 📂 Arquivo a Criar
`data/areas_seed.json`

### ✏️ Conteúdo

```json
[
    {
        "nome": "Tecnologia da Informação",
        "descricao": "Vagas relacionadas a desenvolvimento, infraestrutura e suporte em TI"
    },
    {
        "nome": "Administração",
        "descricao": "Vagas na área administrativa e de gestão"
    },
    {
        "nome": "Marketing",
        "descricao": "Vagas em marketing digital, comunicação e publicidade"
    },
    {
        "nome": "Recursos Humanos",
        "descricao": "Vagas em gestão de pessoas e departamento pessoal"
    },
    {
        "nome": "Engenharia",
        "descricao": "Vagas para diversas engenharias"
    },
    {
        "nome": "Contabilidade",
        "descricao": "Vagas em contabilidade e finanças"
    },
    {
        "nome": "Design",
        "descricao": "Vagas em design gráfico e UX/UI"
    },
    {
        "nome": "Vendas",
        "descricao": "Vagas em vendas e relacionamento com cliente"
    }
]
```

### 📂 Arquivo a Criar
`util/seed_areas.py`

### ✏️ Conteúdo

```python
"""
Inicializa áreas padrão no banco de dados.
"""

import json
from pathlib import Path
from model.area_model import Area
import repo.area_repo as area_repo
from util.logger_config import logger


def inicializar_areas():
    """Carrega áreas do JSON e insere no banco se não existirem."""

    seed_file = Path("data/areas_seed.json")

    if not seed_file.exists():
        logger.warning(f"Arquivo {seed_file} não encontrado")
        return

    try:
        with open(seed_file, 'r', encoding='utf-8') as f:
            areas_data = json.load(f)

        for area_data in areas_data:
            # Verifica se já existe
            area_existente = area_repo.obter_por_nome(area_data['nome'])
            if area_existente:
                logger.debug(f"Área '{area_data['nome']}' já existe")
                continue

            # Criar nova área
            nova_area = Area(
                id_area=0,
                nome=area_data['nome'],
                descricao=area_data['descricao']
            )

            area_repo.inserir(nova_area)
            logger.info(f"Área '{area_data['nome']}' criada com sucesso")

        logger.info("Seed de áreas concluído")

    except Exception as e:
        logger.error(f"Erro ao carregar seed de áreas: {e}", exc_info=True)
```

### 📂 Atualizar `util/seed_data.py`

Adicione no final do arquivo:

```python
# No final do arquivo, na função inicializar_dados():

def inicializar_dados():
    """Inicializa todos os dados seed."""

    # Seed existente de usuários
    inicializar_usuarios_seed()

    # ADICIONAR ESTA LINHA:
    from util.seed_areas import inicializar_areas
    inicializar_areas()
```

### ✅ Verificação
- [ ] Arquivo JSON criado
- [ ] Script de seed criado
- [ ] Seed integrado ao inicializar_dados()
- [ ] Áreas criadas ao iniciar aplicação

---

## 📌 Checkpoint da Fase 1 (Completa)

### ✅ O que foi concluído

1. ✅ **Perfis ajustados** - Estudante, Recrutador, Admin
2. ✅ **6 Models completos** - Usuario, Empresa, Vaga, Candidatura, Area, Endereco
3. ✅ **6 Arquivos SQL criados** - Com todas as queries necessárias
4. ✅ **5 Repositories criados** - Com CRUD completo e funções específicas
5. ✅ **5 DTOs criados** - Com validações usando Pydantic
6. ✅ **main.py atualizado** - Com registro das novas tabelas
7. ✅ **Seeds opcionais** - Para dados iniciais

### 🧪 Teste da Fase 1

Execute e verifique:

```bash
python main.py
```

**Resultado esperado:**
- Aplicação inicia sem erros
- Todas as 9 tabelas são criadas
- Áreas seed são inseridas
- Logs mostram sucesso

### 🎯 Próxima Fase

**FASE 2: Funcionalidades Core**
- Rotas públicas (visualizar vagas)
- Rotas de estudante (buscar, candidatar)
- Rotas de empresa (CRUD de vagas)
- Templates principais

---

# FASE 2: FUNCIONALIDADES CORE

Duração estimada: 2-3 semanas

Esta fase implementa as funcionalidades principais do Estagiou.

---

## 2.1 Rotas Públicas

### 📝 Objetivo
Criar rotas acessíveis sem login para visitantes explorarem vagas e empresas.

---

### 2.1.1 Rotas de Vagas Públicas

### 📂 Arquivo a Criar
`routes/public_vagas_routes.py`

### ✏️ Estrutura Completa

```python
"""
Rotas públicas para visualização de vagas (sem autenticação).
"""

from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from typing import Optional

from util.template_util import criar_templates
import repo.vaga_repo as vaga_repo
import repo.area_repo as area_repo
import repo.empresa_repo as empresa_repo

router = APIRouter(prefix="/vagas", tags=["Vagas Públicas"])
templates = criar_templates("templates")


@router.get("", response_class=HTMLResponse)
async def listar_vagas(
    request: Request,
    area: Optional[int] = Query(None),
    cidade: Optional[str] = Query(None),
    estado: Optional[str] = Query(None),
    modalidade: Optional[str] = Query(None),
    salario_min: Optional[float] = Query(None),
    salario_max: Optional[float] = Query(None),
    busca: Optional[str] = Query(None),
    pagina: int = Query(1, ge=1)
):
    """
    Lista vagas abertas com filtros.
    Rota pública - não requer autenticação.
    """

    por_pagina = 20
    offset = (pagina - 1) * por_pagina

    # Buscar vagas com filtros
    vagas, total = vaga_repo.buscar_com_filtros(
        area_id=area,
        cidade=cidade,
        estado=estado,
        modalidade=modalidade,
        salario_min=salario_min,
        salario_max=salario_max,
        termo_busca=busca,
        limite=por_pagina,
        offset=offset
    )

    # Buscar áreas para filtro
    areas = area_repo.obter_todas()

    # Calcular paginação
    total_paginas = (total + por_pagina - 1) // por_pagina

    return templates.TemplateResponse(
        "public/vagas.html",
        {
            "request": request,
            "vagas": vagas,
            "areas": areas,
            "total": total,
            "pagina": pagina,
            "total_paginas": total_paginas,
            "filtros": {
                "area": area,
                "cidade": cidade,
                "estado": estado,
                "modalidade": modalidade,
                "salario_min": salario_min,
                "salario_max": salario_max,
                "busca": busca
            }
        }
    )


@router.get("/{vaga_id}", response_class=HTMLResponse)
async def detalhes_vaga(request: Request, vaga_id: int):
    """
    Exibe detalhes completos de uma vaga.
    Rota pública - não requer autenticação.
    """

    vaga = vaga_repo.obter_por_id(vaga_id)

    if not vaga:
        return templates.TemplateResponse(
            "errors/404.html",
            {"request": request},
            status_code=404
        )

    # Incrementar contador de visualizações
    vaga_repo.incrementar_visualizacoes(vaga_id)

    # Buscar outras vagas da mesma empresa
    vagas_relacionadas = vaga_repo.obter_por_empresa(vaga.id_empresa)
    vagas_relacionadas = [v for v in vagas_relacionadas if v.id_vaga != vaga_id and v.status_vaga == 'aberta'][:3]

    return templates.TemplateResponse(
        "public/vaga_detalhes.html",
        {
            "request": request,
            "vaga": vaga,
            "vagas_relacionadas": vagas_relacionadas
        }
    )


@router.get("/empresas/listar", response_class=HTMLResponse)
async def listar_empresas(request: Request):
    """
    Lista empresas cadastradas.
    Rota pública - não requer autenticação.
    """

    empresas = empresa_repo.obter_todos()

    return templates.TemplateResponse(
        "public/empresas.html",
        {
            "request": request,
            "empresas": empresas
        }
    )


@router.get("/empresa/{empresa_id}", response_class=HTMLResponse)
async def detalhes_empresa(request: Request, empresa_id: int):
    """
    Exibe perfil público de uma empresa.
    Rota pública - não requer autenticação.
    """

    empresa = empresa_repo.obter_por_id(empresa_id)

    if not empresa:
        return templates.TemplateResponse(
            "errors/404.html",
            {"request": request},
            status_code=404
        )

    # Buscar vagas abertas da empresa
    vagas = vaga_repo.obter_por_empresa(empresa_id)
    vagas_abertas = [v for v in vagas if v.status_vaga == 'aberta']

    return templates.TemplateResponse(
        "public/empresa_detalhes.html",
        {
            "request": request,
            "empresa": empresa,
            "vagas": vagas_abertas
        }
    )
```

### 💡 Destaques

1. **Paginação implementada** - 20 vagas por página
2. **Filtros dinâmicos** - Passados via query params
3. **Incremento de visualizações** - Contador de popularidade
4. **Vagas relacionadas** - Até 3 vagas da mesma empresa

### ✅ Verificação
- [ ] Arquivo criado
- [ ] 4 rotas implementadas
- [ ] Paginação funcionando
- [ ] Filtros aplicados

---

### 2.1.2 Registrar Rotas Públicas no main.py

### 📂 Arquivo a Modificar
`main.py`

### ✏️ O que fazer

1. **Adicione o import** (próximo aos outros imports de rotas):

```python
# Rotas do Estagiou - ADICIONAR
from routes import public_vagas_routes
```

2. **Registre o router** (antes do public_router padrão):

```python
# Incluir routers do Estagiou
app.include_router(public_vagas_routes.router, tags=["Vagas Públicas"])
logger.info("Router de vagas públicas incluído")

# Rotas públicas padrão (deve ser por último)
app.include_router(public_router, tags=["Público"])
logger.info("Router público incluído")
```

---

## 2.2 Rotas de Estudante

### 📝 Objetivo
Criar rotas para estudantes gerenciarem suas candidaturas e perfil.

---

### 2.2.1 Rotas de Candidaturas

### 📂 Arquivo a Criar
`routes/estudante_routes.py`

### ✏️ Estrutura (Primeira Parte)

```python
"""
Rotas para estudantes (buscar vagas, candidatar-se, gerenciar candidaturas).
"""

from fastapi import APIRouter, Request, status, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import ValidationError

from util.auth_decorator import requer_autenticacao
from util.perfis import Perfil
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro, informar_aviso

import repo.vaga_repo as vaga_repo
import repo.candidatura_repo as candidatura_repo
import repo.area_repo as area_repo
from model.candidatura_model import Candidatura

router = APIRouter(prefix="/estudante", tags=["Estudante"])
templates = criar_templates("templates")


@router.get("/vagas", response_class=HTMLResponse)
@requer_autenticacao([Perfil.ESTUDANTE.value])
async def buscar_vagas(request: Request, usuario_logado: dict):
    """Página de busca de vagas para estudantes."""

    vagas = vaga_repo.obter_abertas()
    areas = area_repo.obter_todas()

    return templates.TemplateResponse(
        "estudante/buscar_vagas.html",
        {
            "request": request,
            "vagas": vagas,
            "areas": areas,
            "usuario_logado": usuario_logado
        }
    )


@router.post("/candidatar/{vaga_id}")
@requer_autenticacao([Perfil.ESTUDANTE.value])
async def candidatar_se(
    request: Request,
    vaga_id: int,
    usuario_logado: dict
):
    """Candidata o estudante a uma vaga."""

    # Verificar se já se candidatou
    ja_candidatou = candidatura_repo.verificar_candidatura_existente(
        vaga_id, usuario_logado["id"]
    )

    if ja_candidatou:
        informar_aviso(request, "Você já se candidatou a esta vaga.")
        return RedirectResponse(
            f"/vagas/{vaga_id}",
            status_code=status.HTTP_303_SEE_OTHER
        )

    # Criar candidatura
    candidatura = Candidatura(
        id_candidatura=0,
        id_vaga=vaga_id,
        id_candidato=usuario_logado["id"],
        data_candidatura=None,
        status="em_analise"
    )

    candidatura_repo.inserir(candidatura)
    informar_sucesso(request, "Candidatura realizada com sucesso!")

    return RedirectResponse(
        "/estudante/minhas-candidaturas",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/minhas-candidaturas", response_class=HTMLResponse)
@requer_autenticacao([Perfil.ESTUDANTE.value])
async def minhas_candidaturas(request: Request, usuario_logado: dict):
    """Lista todas as candidaturas do estudante."""

    candidaturas = candidatura_repo.obter_por_estudante(usuario_logado["id"])

    return templates.TemplateResponse(
        "estudante/minhas_candidaturas.html",
        {
            "request": request,
            "candidaturas": candidaturas,
            "usuario_logado": usuario_logado
        }
    )


@router.post("/cancelar-candidatura/{candidatura_id}")
@requer_autenticacao([Perfil.ESTUDANTE.value])
async def cancelar_candidatura(
    request: Request,
    candidatura_id: int,
    usuario_logado: dict
):
    """Cancela uma candidatura do estudante."""

    candidatura = candidatura_repo.obter_por_id(candidatura_id)

    if not candidatura:
        informar_erro(request, "Candidatura não encontrada.")
        return RedirectResponse(
            "/estudante/minhas-candidaturas",
            status_code=status.HTTP_303_SEE_OTHER
        )

    # Verificar se é o dono da candidatura
    if candidatura.id_candidato != usuario_logado["id"]:
        informar_erro(request, "Você não tem permissão para cancelar esta candidatura.")
        return RedirectResponse(
            "/estudante/minhas-candidaturas",
            status_code=status.HTTP_303_SEE_OTHER
        )

    candidatura_repo.excluir(candidatura_id)
    informar_sucesso(request, "Candidatura cancelada com sucesso.")

    return RedirectResponse(
        "/estudante/minhas-candidaturas",
        status_code=status.HTTP_303_SEE_OTHER
    )
```

### 💡 Destaques

1. **Proteção por perfil** - `@requer_autenticacao([Perfil.ESTUDANTE.value])`
2. **Verificação de duplicata** - Impede candidaturas duplicadas
3. **Verificação de ownership** - Só pode cancelar suas próprias candidaturas
4. **Flash messages** - Feedback visual ao usuário

---

---

## 🔷 Passo 2.3: Completar Rotas de Estudante

Adicione as rotas de gerenciamento de perfil e currículo ao arquivo `routes/estudante_routes.py`:

```python
@router.get("/perfil", response_class=HTMLResponse)
@requer_autenticacao([Perfil.ESTUDANTE.value])
async def meu_perfil(request: Request, usuario_logado: dict):
    """Exibe o perfil do estudante."""

    usuario = usuario_repo.obter_por_id(usuario_logado["id"])
    endereco = endereco_repo.obter_por_usuario(usuario_logado["id"])

    return templates.TemplateResponse(
        "estudante/perfil.html",
        {
            "request": request,
            "usuario": usuario,
            "endereco": endereco,
            "usuario_logado": usuario_logado
        }
    )


@router.post("/perfil/atualizar")
@requer_autenticacao([Perfil.ESTUDANTE.value])
async def atualizar_perfil(
    request: Request,
    usuario_logado: dict,
    dto: EstudantePerfilDTO
):
    """Atualiza o perfil do estudante."""

    try:
        usuario_repo.atualizar_perfil_estudante(
            usuario_logado["id"],
            dto.cpf,
            dto.telefone,
            dto.data_nascimento,
            dto.curso,
            dto.instituicao,
            dto.periodo,
            dto.habilidades
        )

        informar_sucesso(request, "Perfil atualizado com sucesso!")

    except Exception as e:
        logger.error(f"Erro ao atualizar perfil: {e}")
        informar_erro(request, "Erro ao atualizar perfil.")

    return RedirectResponse(
        "/estudante/perfil",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/curriculo/upload")
@requer_autenticacao([Perfil.ESTUDANTE.value])
async def upload_curriculo(
    request: Request,
    usuario_logado: dict,
    arquivo: UploadFile = File(...)
):
    """Faz upload do currículo do estudante."""

    # Validar tipo de arquivo
    if not arquivo.filename.endswith('.pdf'):
        informar_erro(request, "Apenas arquivos PDF são permitidos.")
        return RedirectResponse(
            "/estudante/perfil",
            status_code=status.HTTP_303_SEE_OTHER
        )

    # Salvar arquivo
    upload_dir = Path("static/uploads/curriculos")
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Nome único para o arquivo
    nome_arquivo = f"{usuario_logado['id']}_{arquivo.filename}"
    caminho_arquivo = upload_dir / nome_arquivo

    try:
        with caminho_arquivo.open("wb") as f:
            conteudo = await arquivo.read()
            f.write(conteudo)

        # Atualizar no banco
        usuario_repo.atualizar_curriculo(
            usuario_logado["id"],
            f"/static/uploads/curriculos/{nome_arquivo}"
        )

        informar_sucesso(request, "Currículo enviado com sucesso!")

    except Exception as e:
        logger.error(f"Erro ao fazer upload do currículo: {e}")
        informar_erro(request, "Erro ao enviar currículo.")

    return RedirectResponse(
        "/estudante/perfil",
        status_code=status.HTTP_303_SEE_OTHER
    )
```

### ✅ Checklist - Rotas de Estudante Completas
- [ ] Busca de vagas implementada
- [ ] Sistema de candidatura implementado
- [ ] Listagem de candidaturas implementada
- [ ] Cancelamento de candidatura implementado
- [ ] Perfil do estudante implementado
- [ ] Upload de currículo implementado

---

## 🔷 Passo 2.4: Criar Rotas de Empresa/Recrutador

Crie o arquivo **routes/empresa_routes.py** com as rotas para recrutadores gerenciarem vagas:

```python
"""
Rotas para empresas e recrutadores.
"""
from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status
from pathlib import Path
from typing import Optional
from datetime import datetime

from util.auth_utils import requer_autenticacao
from util.templates import criar_templates
from util.mensagens import informar_sucesso, informar_erro, informar_aviso
from util.perfis import Perfil
from util.logger_config import logger

# DTOs
from dtos.vaga_dto import VagaCriarDTO, VagaAlterarDTO

# Repositórios
import repo.vaga_repo as vaga_repo
import repo.empresa_repo as empresa_repo
import repo.candidatura_repo as candidatura_repo
import repo.area_repo as area_repo
from model.vaga_model import Vaga

router = APIRouter(prefix="/empresa", tags=["Empresa"])
templates = criar_templates("templates")


@router.get("/dashboard", response_class=HTMLResponse)
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def dashboard(request: Request, usuario_logado: dict):
    """Dashboard da empresa com estatísticas."""

    empresa = empresa_repo.obter_por_id(usuario_logado["id_empresa"])

    if not empresa:
        informar_erro(request, "Empresa não encontrada.")
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

    # Estatísticas
    vagas = vaga_repo.obter_por_empresa(empresa.id_empresa)
    total_vagas = len(vagas)
    vagas_abertas = len([v for v in vagas if v.status == "aberta"])

    total_candidaturas = sum(
        candidatura_repo.contar_por_vaga(v.id_vaga) for v in vagas
    )

    return templates.TemplateResponse(
        "empresa/dashboard.html",
        {
            "request": request,
            "empresa": empresa,
            "total_vagas": total_vagas,
            "vagas_abertas": vagas_abertas,
            "total_candidaturas": total_candidaturas,
            "vagas": vagas[:5],  # Últimas 5 vagas
            "usuario_logado": usuario_logado
        }
    )


@router.get("/vagas", response_class=HTMLResponse)
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def listar_vagas(request: Request, usuario_logado: dict):
    """Lista todas as vagas da empresa."""

    empresa = empresa_repo.obter_por_id(usuario_logado["id_empresa"])
    vagas = vaga_repo.obter_por_empresa(empresa.id_empresa)

    return templates.TemplateResponse(
        "empresa/vagas.html",
        {
            "request": request,
            "vagas": vagas,
            "empresa": empresa,
            "usuario_logado": usuario_logado
        }
    )


@router.get("/vagas/nova", response_class=HTMLResponse)
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def nova_vaga_form(request: Request, usuario_logado: dict):
    """Formulário para criar nova vaga."""

    empresa = empresa_repo.obter_por_id(usuario_logado["id_empresa"])

    # Verificar se empresa pode publicar mais vagas
    if not empresa_repo.pode_publicar_vaga(empresa.id_empresa):
        informar_aviso(
            request,
            f"Limite de vagas mensais atingido ({empresa.plano}). "
            "Entre em contato para fazer upgrade do plano."
        )
        return RedirectResponse(
            "/empresa/vagas",
            status_code=status.HTTP_303_SEE_OTHER
        )

    areas = area_repo.obter_todas()

    return templates.TemplateResponse(
        "empresa/vaga_form.html",
        {
            "request": request,
            "empresa": empresa,
            "areas": areas,
            "vaga": None,  # Indica criação
            "usuario_logado": usuario_logado
        }
    )


@router.post("/vagas/criar")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def criar_vaga(
    request: Request,
    usuario_logado: dict,
    titulo: str = Form(...),
    descricao: str = Form(...),
    requisitos: str = Form(...),
    beneficios: str = Form(""),
    id_area: int = Form(...),
    carga_horaria: str = Form(...),
    modalidade: str = Form(...),
    cidade: str = Form(...),
    estado: str = Form(...),
    prazo_candidatura: Optional[str] = Form(None)
):
    """Cria uma nova vaga."""

    empresa = empresa_repo.obter_por_id(usuario_logado["id_empresa"])

    # Verificar limite novamente
    if not empresa_repo.pode_publicar_vaga(empresa.id_empresa):
        informar_erro(request, "Limite de vagas mensais atingido.")
        return RedirectResponse(
            "/empresa/vagas",
            status_code=status.HTTP_303_SEE_OTHER
        )

    try:
        # Validar com DTO
        dto = VagaCriarDTO(
            titulo=titulo,
            descricao=descricao,
            requisitos=requisitos,
            beneficios=beneficios,
            id_area=id_area,
            carga_horaria=carga_horaria,
            modalidade=modalidade,
            cidade=cidade,
            estado=estado,
            prazo_candidatura=prazo_candidatura
        )

        # Criar vaga
        vaga = Vaga(
            id_vaga=0,
            titulo=dto.titulo,
            descricao=dto.descricao,
            requisitos=dto.requisitos,
            beneficios=dto.beneficios,
            id_empresa=empresa.id_empresa,
            id_area=dto.id_area,
            carga_horaria=dto.carga_horaria,
            modalidade=dto.modalidade,
            cidade=dto.cidade,
            estado=dto.estado,
            status="aberta",
            destaque=False,
            visualizacoes=0,
            data_publicacao=None,
            prazo_candidatura=dto.prazo_candidatura
        )

        vaga_repo.inserir(vaga)
        empresa_repo.incrementar_contador_vagas(empresa.id_empresa)

        informar_sucesso(request, "Vaga criada com sucesso!")

    except ValueError as e:
        informar_erro(request, str(e))
        return RedirectResponse(
            "/empresa/vagas/nova",
            status_code=status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        logger.error(f"Erro ao criar vaga: {e}")
        informar_erro(request, "Erro ao criar vaga.")

    return RedirectResponse(
        "/empresa/vagas",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/vagas/{vaga_id}/editar", response_class=HTMLResponse)
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def editar_vaga_form(
    request: Request,
    vaga_id: int,
    usuario_logado: dict
):
    """Formulário para editar vaga."""

    vaga = vaga_repo.obter_por_id(vaga_id)

    if not vaga:
        informar_erro(request, "Vaga não encontrada.")
        return RedirectResponse(
            "/empresa/vagas",
            status_code=status.HTTP_303_SEE_OTHER
        )

    # Verificar se a vaga pertence à empresa
    if vaga.id_empresa != usuario_logado["id_empresa"]:
        informar_erro(request, "Você não tem permissão para editar esta vaga.")
        return RedirectResponse(
            "/empresa/vagas",
            status_code=status.HTTP_303_SEE_OTHER
        )

    empresa = empresa_repo.obter_por_id(usuario_logado["id_empresa"])
    areas = area_repo.obter_todas()

    return templates.TemplateResponse(
        "empresa/vaga_form.html",
        {
            "request": request,
            "empresa": empresa,
            "areas": areas,
            "vaga": vaga,  # Indica edição
            "usuario_logado": usuario_logado
        }
    )


@router.post("/vagas/{vaga_id}/atualizar")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def atualizar_vaga(
    request: Request,
    vaga_id: int,
    usuario_logado: dict,
    titulo: str = Form(...),
    descricao: str = Form(...),
    requisitos: str = Form(...),
    beneficios: str = Form(""),
    id_area: int = Form(...),
    carga_horaria: str = Form(...),
    modalidade: str = Form(...),
    cidade: str = Form(...),
    estado: str = Form(...),
    status_vaga: str = Form(...),
    prazo_candidatura: Optional[str] = Form(None)
):
    """Atualiza uma vaga existente."""

    vaga = vaga_repo.obter_por_id(vaga_id)

    if not vaga or vaga.id_empresa != usuario_logado["id_empresa"]:
        informar_erro(request, "Vaga não encontrada ou sem permissão.")
        return RedirectResponse(
            "/empresa/vagas",
            status_code=status.HTTP_303_SEE_OTHER
        )

    try:
        # Validar com DTO
        dto = VagaAlterarDTO(
            titulo=titulo,
            descricao=descricao,
            requisitos=requisitos,
            beneficios=beneficios,
            id_area=id_area,
            carga_horaria=carga_horaria,
            modalidade=modalidade,
            cidade=cidade,
            estado=estado,
            status=status_vaga,
            prazo_candidatura=prazo_candidatura
        )

        # Atualizar vaga
        vaga_repo.atualizar(
            vaga_id,
            dto.titulo,
            dto.descricao,
            dto.requisitos,
            dto.beneficios,
            dto.id_area,
            dto.carga_horaria,
            dto.modalidade,
            dto.cidade,
            dto.estado,
            dto.prazo_candidatura
        )

        vaga_repo.atualizar_status(vaga_id, dto.status)

        informar_sucesso(request, "Vaga atualizada com sucesso!")

    except ValueError as e:
        informar_erro(request, str(e))
    except Exception as e:
        logger.error(f"Erro ao atualizar vaga: {e}")
        informar_erro(request, "Erro ao atualizar vaga.")

    return RedirectResponse(
        f"/empresa/vagas/{vaga_id}/candidatos",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/vagas/{vaga_id}/candidatos", response_class=HTMLResponse)
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def listar_candidatos(
    request: Request,
    vaga_id: int,
    usuario_logado: dict,
    filtro_status: Optional[str] = None
):
    """Lista candidatos de uma vaga."""

    vaga = vaga_repo.obter_por_id(vaga_id)

    if not vaga or vaga.id_empresa != usuario_logado["id_empresa"]:
        informar_erro(request, "Vaga não encontrada ou sem permissão.")
        return RedirectResponse(
            "/empresa/vagas",
            status_code=status.HTTP_303_SEE_OTHER
        )

    # Buscar candidaturas
    if filtro_status:
        candidaturas = [
            c for c in candidatura_repo.obter_por_vaga(vaga_id)
            if c.status == filtro_status
        ]
    else:
        candidaturas = candidatura_repo.obter_por_vaga(vaga_id)

    # Estatísticas
    stats = {
        "total": candidatura_repo.contar_por_vaga(vaga_id),
        "em_analise": candidatura_repo.contar_por_status(vaga_id, "em_analise"),
        "entrevista": candidatura_repo.contar_por_status(vaga_id, "entrevista"),
        "aprovado": candidatura_repo.contar_por_status(vaga_id, "aprovado"),
        "recusado": candidatura_repo.contar_por_status(vaga_id, "recusado")
    }

    return templates.TemplateResponse(
        "empresa/candidatos.html",
        {
            "request": request,
            "vaga": vaga,
            "candidaturas": candidaturas,
            "stats": stats,
            "filtro_atual": filtro_status,
            "usuario_logado": usuario_logado
        }
    )


@router.post("/candidaturas/{candidatura_id}/atualizar-status")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def atualizar_status_candidatura(
    request: Request,
    candidatura_id: int,
    usuario_logado: dict,
    novo_status: str = Form(...),
    observacoes: Optional[str] = Form(None)
):
    """Atualiza o status de uma candidatura."""

    candidatura = candidatura_repo.obter_por_id(candidatura_id)

    if not candidatura:
        informar_erro(request, "Candidatura não encontrada.")
        return RedirectResponse(
            "/empresa/vagas",
            status_code=status.HTTP_303_SEE_OTHER
        )

    # Verificar se a vaga pertence à empresa
    vaga = vaga_repo.obter_por_id(candidatura.id_vaga)
    if vaga.id_empresa != usuario_logado["id_empresa"]:
        informar_erro(request, "Você não tem permissão para atualizar esta candidatura.")
        return RedirectResponse(
            "/empresa/vagas",
            status_code=status.HTTP_303_SEE_OTHER
        )

    try:
        candidatura_repo.atualizar_status(candidatura_id, novo_status, observacoes)
        informar_sucesso(request, f"Status atualizado para: {novo_status}")
    except Exception as e:
        logger.error(f"Erro ao atualizar status: {e}")
        informar_erro(request, "Erro ao atualizar status.")

    return RedirectResponse(
        f"/empresa/vagas/{candidatura.id_vaga}/candidatos",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/vagas/{vaga_id}/excluir")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def excluir_vaga(
    request: Request,
    vaga_id: int,
    usuario_logado: dict
):
    """Exclui uma vaga."""

    vaga = vaga_repo.obter_por_id(vaga_id)

    if not vaga or vaga.id_empresa != usuario_logado["id_empresa"]:
        informar_erro(request, "Vaga não encontrada ou sem permissão.")
        return RedirectResponse(
            "/empresa/vagas",
            status_code=status.HTTP_303_SEE_OTHER
        )

    try:
        vaga_repo.excluir(vaga_id)
        informar_sucesso(request, "Vaga excluída com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao excluir vaga: {e}")
        informar_erro(request, "Erro ao excluir vaga.")

    return RedirectResponse(
        "/empresa/vagas",
        status_code=status.HTTP_303_SEE_OTHER
    )
```

### ✅ Checklist - Rotas de Empresa/Recrutador
- [ ] Dashboard com estatísticas implementado
- [ ] Listagem de vagas da empresa implementada
- [ ] Criação de vagas implementada
- [ ] Edição de vagas implementada
- [ ] Verificação de limites do plano implementada
- [ ] Listagem de candidatos por vaga implementada
- [ ] Atualização de status de candidatura implementada
- [ ] Exclusão de vagas implementada

---

## 🔷 Passo 2.5: Criar Rotas Administrativas

Crie o arquivo **routes/admin_vagas_routes.py** para administradores gerenciarem vagas:

```python
"""
Rotas administrativas para gerenciamento de vagas.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status

from util.auth_utils import requer_autenticacao
from util.templates import criar_templates
from util.mensagens import informar_sucesso, informar_erro
from util.perfis import Perfil
from util.logger_config import logger

import repo.vaga_repo as vaga_repo

router = APIRouter(prefix="/admin/vagas", tags=["Admin - Vagas"])
templates = criar_templates("templates")


@router.get("", response_class=HTMLResponse)
@requer_autenticacao([Perfil.ADMIN.value])
async def listar_todas_vagas(request: Request, usuario_logado: dict):
    """Lista todas as vagas do sistema."""

    vagas = vaga_repo.obter_todas()

    return templates.TemplateResponse(
        "admin/vagas.html",
        {
            "request": request,
            "vagas": vagas,
            "usuario_logado": usuario_logado
        }
    )


@router.post("/{vaga_id}/aprovar")
@requer_autenticacao([Perfil.ADMIN.value])
async def aprovar_vaga(
    request: Request,
    vaga_id: int,
    usuario_logado: dict
):
    """Aprova uma vaga (abre para candidaturas)."""

    try:
        vaga_repo.atualizar_status(vaga_id, "aberta")
        informar_sucesso(request, "Vaga aprovada com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao aprovar vaga: {e}")
        informar_erro(request, "Erro ao aprovar vaga.")

    return RedirectResponse(
        "/admin/vagas",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/{vaga_id}/destacar")
@requer_autenticacao([Perfil.ADMIN.value])
async def destacar_vaga(
    request: Request,
    vaga_id: int,
    usuario_logado: dict
):
    """Destaca uma vaga na página principal."""

    try:
        vaga = vaga_repo.obter_por_id(vaga_id)
        novo_destaque = not vaga.destaque

        vaga_repo.atualizar_destaque(vaga_id, novo_destaque)

        msg = "Vaga destacada!" if novo_destaque else "Destaque removido!"
        informar_sucesso(request, msg)

    except Exception as e:
        logger.error(f"Erro ao destacar vaga: {e}")
        informar_erro(request, "Erro ao destacar vaga.")

    return RedirectResponse(
        "/admin/vagas",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/{vaga_id}/fechar")
@requer_autenticacao([Perfil.ADMIN.value])
async def fechar_vaga(
    request: Request,
    vaga_id: int,
    usuario_logado: dict
):
    """Fecha uma vaga administrativamente."""

    try:
        vaga_repo.atualizar_status(vaga_id, "fechada")
        informar_sucesso(request, "Vaga fechada com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao fechar vaga: {e}")
        informar_erro(request, "Erro ao fechar vaga.")

    return RedirectResponse(
        "/admin/vagas",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/{vaga_id}/excluir")
@requer_autenticacao([Perfil.ADMIN.value])
async def excluir_vaga_admin(
    request: Request,
    vaga_id: int,
    usuario_logado: dict
):
    """Exclui uma vaga (admin tem permissão total)."""

    try:
        vaga_repo.excluir(vaga_id)
        informar_sucesso(request, "Vaga excluída com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao excluir vaga: {e}")
        informar_erro(request, "Erro ao excluir vaga.")

    return RedirectResponse(
        "/admin/vagas",
        status_code=status.HTTP_303_SEE_OTHER
    )
```

Crie o arquivo **routes/admin_areas_routes.py** para administradores gerenciarem áreas:

```python
"""
Rotas administrativas para gerenciamento de áreas.
"""
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status

from util.auth_utils import requer_autenticacao
from util.templates import criar_templates
from util.mensagens import informar_sucesso, informar_erro
from util.perfis import Perfil
from util.logger_config import logger

from dtos.area_dto import AreaCriarDTO, AreaAlterarDTO
import repo.area_repo as area_repo
from model.area_model import Area

router = APIRouter(prefix="/admin/areas", tags=["Admin - Áreas"])
templates = criar_templates("templates")


@router.get("", response_class=HTMLResponse)
@requer_autenticacao([Perfil.ADMIN.value])
async def listar_areas(request: Request, usuario_logado: dict):
    """Lista todas as áreas."""

    areas = area_repo.obter_todas()

    return templates.TemplateResponse(
        "admin/areas.html",
        {
            "request": request,
            "areas": areas,
            "usuario_logado": usuario_logado
        }
    )


@router.post("/criar")
@requer_autenticacao([Perfil.ADMIN.value])
async def criar_area(
    request: Request,
    usuario_logado: dict,
    nome: str = Form(...),
    descricao: str = Form("")
):
    """Cria uma nova área."""

    try:
        dto = AreaCriarDTO(nome=nome, descricao=descricao)

        area = Area(
            id_area=0,
            nome=dto.nome,
            descricao=dto.descricao
        )

        area_repo.inserir(area)
        informar_sucesso(request, "Área criada com sucesso!")

    except ValueError as e:
        informar_erro(request, str(e))
    except Exception as e:
        logger.error(f"Erro ao criar área: {e}")
        informar_erro(request, "Erro ao criar área.")

    return RedirectResponse(
        "/admin/areas",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/{area_id}/atualizar")
@requer_autenticacao([Perfil.ADMIN.value])
async def atualizar_area(
    request: Request,
    area_id: int,
    usuario_logado: dict,
    nome: str = Form(...),
    descricao: str = Form("")
):
    """Atualiza uma área existente."""

    try:
        dto = AreaAlterarDTO(nome=nome, descricao=descricao)

        area_repo.atualizar(area_id, dto.nome, dto.descricao)
        informar_sucesso(request, "Área atualizada com sucesso!")

    except ValueError as e:
        informar_erro(request, str(e))
    except Exception as e:
        logger.error(f"Erro ao atualizar área: {e}")
        informar_erro(request, "Erro ao atualizar área.")

    return RedirectResponse(
        "/admin/areas",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/{area_id}/excluir")
@requer_autenticacao([Perfil.ADMIN.value])
async def excluir_area(
    request: Request,
    area_id: int,
    usuario_logado: dict
):
    """Exclui uma área."""

    try:
        # Verificar se há vagas usando esta área
        total_vagas = area_repo.contar_vagas_por_area(area_id)

        if total_vagas > 0:
            informar_aviso(
                request,
                f"Não é possível excluir esta área pois existem {total_vagas} vaga(s) associada(s)."
            )
        else:
            area_repo.excluir(area_id)
            informar_sucesso(request, "Área excluída com sucesso!")

    except Exception as e:
        logger.error(f"Erro ao excluir área: {e}")
        informar_erro(request, "Erro ao excluir área.")

    return RedirectResponse(
        "/admin/areas",
        status_code=status.HTTP_303_SEE_OTHER
    )
```

Crie o arquivo **routes/admin_empresas_routes.py** para administradores gerenciarem empresas:

```python
"""
Rotas administrativas para gerenciamento de empresas.
"""
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status
from typing import Optional

from util.auth_utils import requer_autenticacao
from util.templates import criar_templates
from util.mensagens import informar_sucesso, informar_erro, informar_aviso
from util.perfis import Perfil
from util.logger_config import logger

import repo.empresa_repo as empresa_repo
import repo.vaga_repo as vaga_repo

router = APIRouter(prefix="/admin/empresas", tags=["Admin - Empresas"])
templates = criar_templates("templates")


@router.get("", response_class=HTMLResponse)
@requer_autenticacao([Perfil.ADMIN.value])
async def listar_empresas(request: Request, usuario_logado: dict):
    """Lista todas as empresas cadastradas."""

    empresas = empresa_repo.obter_todas()

    return templates.TemplateResponse(
        "admin/empresas.html",
        {
            "request": request,
            "empresas": empresas,
            "usuario_logado": usuario_logado
        }
    )


@router.get("/{empresa_id}", response_class=HTMLResponse)
@requer_autenticacao([Perfil.ADMIN.value])
async def detalhes_empresa(
    request: Request,
    empresa_id: int,
    usuario_logado: dict
):
    """Visualiza detalhes de uma empresa."""

    empresa = empresa_repo.obter_por_id(empresa_id)

    if not empresa:
        informar_erro(request, "Empresa não encontrada.")
        return RedirectResponse(
            "/admin/empresas",
            status_code=status.HTTP_303_SEE_OTHER
        )

    vagas = vaga_repo.obter_por_empresa(empresa_id)

    return templates.TemplateResponse(
        "admin/empresa_detalhes.html",
        {
            "request": request,
            "empresa": empresa,
            "vagas": vagas,
            "usuario_logado": usuario_logado
        }
    )


@router.post("/{empresa_id}/alterar-plano")
@requer_autenticacao([Perfil.ADMIN.value])
async def alterar_plano_empresa(
    request: Request,
    empresa_id: int,
    usuario_logado: dict,
    novo_plano: str = Form(...)
):
    """Altera o plano de uma empresa."""

    planos_validos = ["Gratuito", "Básico", "Premium"]

    if novo_plano not in planos_validos:
        informar_erro(request, "Plano inválido.")
        return RedirectResponse(
            f"/admin/empresas/{empresa_id}",
            status_code=status.HTTP_303_SEE_OTHER
        )

    try:
        empresa_repo.atualizar_plano(empresa_id, novo_plano)
        informar_sucesso(request, f"Plano alterado para: {novo_plano}")
    except Exception as e:
        logger.error(f"Erro ao alterar plano: {e}")
        informar_erro(request, "Erro ao alterar plano.")

    return RedirectResponse(
        f"/admin/empresas/{empresa_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/{empresa_id}/ativar")
@requer_autenticacao([Perfil.ADMIN.value])
async def ativar_empresa(
    request: Request,
    empresa_id: int,
    usuario_logado: dict
):
    """Ativa uma empresa desativada."""

    try:
        empresa = empresa_repo.obter_por_id(empresa_id)

        if empresa.ativo:
            informar_aviso(request, "Empresa já está ativa.")
        else:
            # Reativar (atualizar campo ativo=True no banco)
            # Nota: você precisará adicionar este método no repositório
            informar_sucesso(request, "Empresa reativada com sucesso!")

    except Exception as e:
        logger.error(f"Erro ao ativar empresa: {e}")
        informar_erro(request, "Erro ao ativar empresa.")

    return RedirectResponse(
        f"/admin/empresas/{empresa_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/{empresa_id}/desativar")
@requer_autenticacao([Perfil.ADMIN.value])
async def desativar_empresa(
    request: Request,
    empresa_id: int,
    usuario_logado: dict
):
    """Desativa uma empresa."""

    try:
        empresa_repo.desativar(empresa_id)
        informar_sucesso(request, "Empresa desativada com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao desativar empresa: {e}")
        informar_erro(request, "Erro ao desativar empresa.")

    return RedirectResponse(
        "/admin/empresas",
        status_code=status.HTTP_303_SEE_OTHER
    )
```

### ✅ Checklist - Rotas Administrativas
- [ ] Gerenciamento de vagas implementado
- [ ] Gerenciamento de áreas implementado
- [ ] Gerenciamento de empresas implementado
- [ ] Sistema de planos implementado
- [ ] Ativação/desativação de empresas implementada

---

## 🔷 Passo 2.6: Registrar Novas Rotas no main.py

Abra o arquivo **main.py** e adicione os imports e registros das novas rotas:

```python
# Adicionar aos imports existentes
from routes.estudante_routes import router as estudante_router
from routes.empresa_routes import router as empresa_router
from routes.admin_vagas_routes import router as admin_vagas_router
from routes.admin_areas_routes import router as admin_areas_router
from routes.admin_empresas_routes import router as admin_empresas_router
```

```python
# Adicionar após os routers já existentes (antes de public_router)

app.include_router(estudante_router, tags=["Estudante"])
logger.info("Router de estudante incluído")

app.include_router(empresa_router, tags=["Empresa"])
logger.info("Router de empresa incluído")

app.include_router(admin_vagas_router, tags=["Admin - Vagas"])
logger.info("Router admin de vagas incluído")

app.include_router(admin_areas_router, tags=["Admin - Áreas"])
logger.info("Router admin de áreas incluído")

app.include_router(admin_empresas_router, tags=["Admin - Empresas"])
logger.info("Router admin de empresas incluído")
```

### ✅ Checklist - Registro de Rotas
- [ ] Rotas de estudante registradas
- [ ] Rotas de empresa registradas
- [ ] Rotas administrativas de vagas registradas
- [ ] Rotas administrativas de áreas registradas
- [ ] Rotas administrativas de empresas registradas

---

## ✅ CHECKPOINT - FASE 2 COMPLETA

Parabéns! Você completou a **Fase 2 - Funcionalidades Principais**. Agora você tem:

✅ Sistema completo de rotas públicas para visualizar vagas
✅ Sistema de candidatura para estudantes
✅ Painel completo para empresas gerenciarem vagas
✅ Sistema de gerenciamento de candidatos
✅ Painel administrativo completo

**📊 Progresso: ~60% do guia completo**

---

# 🎨 FASE 3: Templates e Interface

Nesta fase vamos criar os templates HTML principais para a interface do usuário.

## 🔷 Passo 3.1: Template Base para Estudante

Crie o arquivo **templates/estudante/buscar_vagas.html**:

```html
{% extends "base.html" %}

{% block title %}Buscar Vagas - Estagiou{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="mb-4">Buscar Vagas de Estágio</h1>

    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-body">
            <form method="GET" action="/estudante/vagas">
                <div class="row g-3">
                    <div class="col-md-4">
                        <label for="area" class="form-label">Área</label>
                        <select class="form-select" id="area" name="area">
                            <option value="">Todas as áreas</option>
                            {% for area in areas %}
                            <option value="{{ area.id_area }}">{{ area.nome }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="col-md-3">
                        <label for="modalidade" class="form-label">Modalidade</label>
                        <select class="form-select" id="modalidade" name="modalidade">
                            <option value="">Todas</option>
                            <option value="presencial">Presencial</option>
                            <option value="remoto">Remoto</option>
                            <option value="hibrido">Híbrido</option>
                        </select>
                    </div>

                    <div class="col-md-3">
                        <label for="cidade" class="form-label">Cidade</label>
                        <input type="text" class="form-control" id="cidade" name="cidade"
                               placeholder="Ex: São Paulo">
                    </div>

                    <div class="col-md-2 d-flex align-items-end">
                        <button type="submit" class="btn btn-primary w-100">
                            <i class="bi bi-search"></i> Buscar
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>

    <!-- Lista de Vagas -->
    <div class="row">
        {% if vagas %}
            {% for vaga in vagas %}
            <div class="col-md-6 mb-4">
                <div class="card h-100 {% if vaga.destaque %}border-warning{% endif %}">
                    {% if vaga.destaque %}
                    <div class="card-header bg-warning text-dark">
                        <i class="bi bi-star-fill"></i> Vaga em Destaque
                    </div>
                    {% endif %}

                    <div class="card-body">
                        <h5 class="card-title">{{ vaga.titulo }}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">
                            {{ vaga.empresa.nome if vaga.empresa else "Empresa Confidencial" }}
                        </h6>

                        <p class="card-text">
                            {{ vaga.descricao[:150] }}{% if vaga.descricao|length > 150 %}...{% endif %}
                        </p>

                        <div class="mb-2">
                            <span class="badge bg-primary">{{ vaga.area.nome if vaga.area else "Geral" }}</span>
                            <span class="badge bg-secondary">{{ vaga.modalidade }}</span>
                            <span class="badge bg-info text-dark">
                                <i class="bi bi-geo-alt"></i> {{ vaga.cidade }}, {{ vaga.estado }}
                            </span>
                        </div>

                        <div class="d-flex justify-content-between align-items-center mt-3">
                            <small class="text-muted">
                                <i class="bi bi-eye"></i> {{ vaga.visualizacoes }} visualizações
                            </small>

                            <div>
                                <a href="/vagas/{{ vaga.id_vaga }}" class="btn btn-outline-primary btn-sm">
                                    Ver Detalhes
                                </a>
                                <form method="POST" action="/estudante/candidatar/{{ vaga.id_vaga }}"
                                      style="display: inline;">
                                    <button type="submit" class="btn btn-success btn-sm">
                                        <i class="bi bi-file-earmark-text"></i> Candidatar
                                    </button>
                                </form>
                            </div>
                        </div>
                    </div>

                    {% if vaga.prazo_candidatura %}
                    <div class="card-footer text-muted">
                        <small>
                            <i class="bi bi-calendar-event"></i>
                            Prazo: {{ vaga.prazo_candidatura.strftime('%d/%m/%Y') }}
                        </small>
                    </div>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        {% else %}
            <div class="col-12">
                <div class="alert alert-info text-center">
                    <i class="bi bi-info-circle"></i>
                    Nenhuma vaga encontrada com os filtros selecionados.
                </div>
            </div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

## 🔷 Passo 3.2: Template de Candidaturas do Estudante

Crie o arquivo **templates/estudante/minhas_candidaturas.html**:

```html
{% extends "base.html" %}

{% block title %}Minhas Candidaturas - Estagiou{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="mb-4">Minhas Candidaturas</h1>

    {% if candidaturas %}
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Vaga</th>
                        <th>Empresa</th>
                        <th>Data da Candidatura</th>
                        <th>Status</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {% for candidatura in candidaturas %}
                    <tr>
                        <td>
                            <strong>{{ candidatura.vaga.titulo }}</strong><br>
                            <small class="text-muted">{{ candidatura.vaga.cidade }}, {{ candidatura.vaga.estado }}</small>
                        </td>
                        <td>{{ candidatura.vaga.empresa.nome }}</td>
                        <td>{{ candidatura.data_candidatura.strftime('%d/%m/%Y %H:%M') }}</td>
                        <td>
                            {% if candidatura.status == 'em_analise' %}
                                <span class="badge bg-warning text-dark">Em Análise</span>
                            {% elif candidatura.status == 'entrevista' %}
                                <span class="badge bg-info">Entrevista</span>
                            {% elif candidatura.status == 'aprovado' %}
                                <span class="badge bg-success">Aprovado</span>
                            {% elif candidatura.status == 'recusado' %}
                                <span class="badge bg-danger">Recusado</span>
                            {% endif %}

                            {% if candidatura.observacoes %}
                                <button class="btn btn-sm btn-link" data-bs-toggle="tooltip"
                                        title="{{ candidatura.observacoes }}">
                                    <i class="bi bi-info-circle"></i>
                                </button>
                            {% endif %}
                        </td>
                        <td>
                            <a href="/vagas/{{ candidatura.id_vaga }}"
                               class="btn btn-sm btn-outline-primary">
                                Ver Vaga
                            </a>

                            {% if candidatura.status == 'em_analise' %}
                            <form method="POST"
                                  action="/estudante/cancelar-candidatura/{{ candidatura.id_candidatura }}"
                                  style="display: inline;"
                                  onsubmit="return confirm('Deseja realmente cancelar esta candidatura?');">
                                <button type="submit" class="btn btn-sm btn-outline-danger">
                                    Cancelar
                                </button>
                            </form>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    {% else %}
        <div class="alert alert-info text-center">
            <i class="bi bi-info-circle"></i>
            Você ainda não se candidatou a nenhuma vaga.
            <br><br>
            <a href="/estudante/vagas" class="btn btn-primary">
                Buscar Vagas
            </a>
        </div>
    {% endif %}
</div>

<script>
// Inicializar tooltips do Bootstrap
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})
</script>
{% endblock %}
```

## 🔷 Passo 3.3: Template Dashboard da Empresa

Crie o arquivo **templates/empresa/dashboard.html**:

```html
{% extends "base.html" %}

{% block title %}Dashboard - {{ empresa.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard - {{ empresa.nome }}</h1>
        <span class="badge bg-{% if empresa.plano == 'Premium' %}success{% elif empresa.plano == 'Básico' %}primary{% else %}secondary{% endif %} fs-6">
            Plano {{ empresa.plano }}
        </span>
    </div>

    <!-- Estatísticas -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card text-white bg-primary">
                <div class="card-body">
                    <h5 class="card-title">
                        <i class="bi bi-briefcase"></i> Total de Vagas
                    </h5>
                    <h2>{{ total_vagas }}</h2>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card text-white bg-success">
                <div class="card-body">
                    <h5 class="card-title">
                        <i class="bi bi-check-circle"></i> Vagas Abertas
                    </h5>
                    <h2>{{ vagas_abertas }}</h2>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card text-white bg-info">
                <div class="card-body">
                    <h5 class="card-title">
                        <i class="bi bi-people"></i> Candidaturas
                    </h5>
                    <h2>{{ total_candidaturas }}</h2>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card text-white bg-warning">
                <div class="card-body">
                    <h5 class="card-title">
                        <i class="bi bi-calendar-month"></i> Limite Mensal
                    </h5>
                    <h2>{{ empresa.vagas_publicadas_mes }}/{{ empresa.vagas_mensais_limite }}</h2>
                </div>
            </div>
        </div>
    </div>

    <!-- Ações Rápidas -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Ações Rápidas</h5>
                </div>
                <div class="card-body">
                    <a href="/empresa/vagas/nova" class="btn btn-success me-2">
                        <i class="bi bi-plus-circle"></i> Nova Vaga
                    </a>
                    <a href="/empresa/vagas" class="btn btn-primary me-2">
                        <i class="bi bi-list"></i> Gerenciar Vagas
                    </a>
                    <a href="/perfil" class="btn btn-secondary">
                        <i class="bi bi-building"></i> Editar Perfil da Empresa
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- Últimas Vagas -->
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Últimas Vagas Publicadas</h5>
                </div>
                <div class="card-body">
                    {% if vagas %}
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>Título</th>
                                        <th>Status</th>
                                        <th>Candidatos</th>
                                        <th>Visualizações</th>
                                        <th>Ações</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for vaga in vagas %}
                                    <tr>
                                        <td>
                                            <strong>{{ vaga.titulo }}</strong><br>
                                            <small class="text-muted">{{ vaga.cidade }}, {{ vaga.estado }}</small>
                                        </td>
                                        <td>
                                            {% if vaga.status == 'aberta' %}
                                                <span class="badge bg-success">Aberta</span>
                                            {% elif vaga.status == 'fechada' %}
                                                <span class="badge bg-danger">Fechada</span>
                                            {% elif vaga.status == 'pausada' %}
                                                <span class="badge bg-warning">Pausada</span>
                                            {% endif %}
                                        </td>
                                        <td>{{ vaga.total_candidaturas or 0 }}</td>
                                        <td>{{ vaga.visualizacoes }}</td>
                                        <td>
                                            <a href="/empresa/vagas/{{ vaga.id_vaga }}/candidatos"
                                               class="btn btn-sm btn-primary">
                                                Ver Candidatos
                                            </a>
                                            <a href="/empresa/vagas/{{ vaga.id_vaga }}/editar"
                                               class="btn btn-sm btn-outline-secondary">
                                                Editar
                                            </a>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>

                        <div class="text-center mt-3">
                            <a href="/empresa/vagas" class="btn btn-outline-primary">
                                Ver Todas as Vagas
                            </a>
                        </div>
                    {% else %}
                        <div class="alert alert-info text-center">
                            Você ainda não publicou nenhuma vaga.
                            <br><br>
                            <a href="/empresa/vagas/nova" class="btn btn-success">
                                Publicar Primeira Vaga
                            </a>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### ✅ Checklist - Templates Principais
- [ ] Template de busca de vagas criado
- [ ] Template de candidaturas do estudante criado
- [ ] Template de dashboard da empresa criado
- [ ] Templates responsivos com Bootstrap 5
- [ ] Badges e ícones implementados

---

---

## 🔷 Passo 3.4: Template Formulário de Vaga

Crie o arquivo **templates/empresa/vaga_form.html**:

```html
{% extends "base.html" %}

{% block title %}{% if vaga %}Editar{% else %}Nova{% endif %} Vaga - Estagiou{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="mb-4">{% if vaga %}Editar Vaga{% else %}Publicar Nova Vaga{% endif %}</h1>

    <div class="row">
        <div class="col-lg-8">
            <div class="card">
                <div class="card-body">
                    <form method="POST"
                          action="{% if vaga %}/empresa/vagas/{{ vaga.id_vaga }}/atualizar{% else %}/empresa/vagas/criar{% endif %}">

                        <!-- Título -->
                        <div class="mb-3">
                            <label for="titulo" class="form-label">Título da Vaga *</label>
                            <input type="text" class="form-control" id="titulo" name="titulo"
                                   value="{{ vaga.titulo if vaga else '' }}"
                                   required maxlength="200"
                                   placeholder="Ex: Estágio em Desenvolvimento Web">
                        </div>

                        <!-- Descrição -->
                        <div class="mb-3">
                            <label for="descricao" class="form-label">Descrição *</label>
                            <textarea class="form-control" id="descricao" name="descricao"
                                      rows="5" required
                                      placeholder="Descreva as atividades e responsabilidades do estágio...">{{ vaga.descricao if vaga else '' }}</textarea>
                            <small class="text-muted">Seja claro e objetivo sobre o que o estagiário irá fazer.</small>
                        </div>

                        <!-- Requisitos -->
                        <div class="mb-3">
                            <label for="requisitos" class="form-label">Requisitos *</label>
                            <textarea class="form-control" id="requisitos" name="requisitos"
                                      rows="4" required
                                      placeholder="Liste os requisitos necessários (conhecimentos, curso, período, etc.)">{{ vaga.requisitos if vaga else '' }}</textarea>
                        </div>

                        <!-- Benefícios -->
                        <div class="mb-3">
                            <label for="beneficios" class="form-label">Benefícios</label>
                            <textarea class="form-control" id="beneficios" name="beneficios"
                                      rows="3"
                                      placeholder="Vale transporte, vale refeição, seguro de vida, etc.">{{ vaga.beneficios if vaga else '' }}</textarea>
                        </div>

                        <div class="row">
                            <!-- Área -->
                            <div class="col-md-6 mb-3">
                                <label for="id_area" class="form-label">Área *</label>
                                <select class="form-select" id="id_area" name="id_area" required>
                                    <option value="">Selecione...</option>
                                    {% for area in areas %}
                                    <option value="{{ area.id_area }}"
                                            {% if vaga and vaga.id_area == area.id_area %}selected{% endif %}>
                                        {{ area.nome }}
                                    </option>
                                    {% endfor %}
                                </select>
                            </div>

                            <!-- Carga Horária -->
                            <div class="col-md-6 mb-3">
                                <label for="carga_horaria" class="form-label">Carga Horária *</label>
                                <input type="text" class="form-control" id="carga_horaria" name="carga_horaria"
                                       value="{{ vaga.carga_horaria if vaga else '' }}"
                                       required maxlength="50"
                                       placeholder="Ex: 6h/dia, 30h/semana">
                            </div>
                        </div>

                        <div class="row">
                            <!-- Modalidade -->
                            <div class="col-md-4 mb-3">
                                <label for="modalidade" class="form-label">Modalidade *</label>
                                <select class="form-select" id="modalidade" name="modalidade" required>
                                    <option value="">Selecione...</option>
                                    <option value="presencial" {% if vaga and vaga.modalidade == 'presencial' %}selected{% endif %}>Presencial</option>
                                    <option value="remoto" {% if vaga and vaga.modalidade == 'remoto' %}selected{% endif %}>Remoto</option>
                                    <option value="hibrido" {% if vaga and vaga.modalidade == 'hibrido' %}selected{% endif %}>Híbrido</option>
                                </select>
                            </div>

                            <!-- Cidade -->
                            <div class="col-md-4 mb-3">
                                <label for="cidade" class="form-label">Cidade *</label>
                                <input type="text" class="form-control" id="cidade" name="cidade"
                                       value="{{ vaga.cidade if vaga else '' }}"
                                       required maxlength="100"
                                       placeholder="Ex: São Paulo">
                            </div>

                            <!-- Estado -->
                            <div class="col-md-4 mb-3">
                                <label for="estado" class="form-label">Estado *</label>
                                <select class="form-select" id="estado" name="estado" required>
                                    <option value="">UF</option>
                                    <option value="AC" {% if vaga and vaga.estado == 'AC' %}selected{% endif %}>AC</option>
                                    <option value="AL" {% if vaga and vaga.estado == 'AL' %}selected{% endif %}>AL</option>
                                    <option value="ES" {% if vaga and vaga.estado == 'ES' %}selected{% endif %}>ES</option>
                                    <option value="MG" {% if vaga and vaga.estado == 'MG' %}selected{% endif %}>MG</option>
                                    <option value="RJ" {% if vaga and vaga.estado == 'RJ' %}selected{% endif %}>RJ</option>
                                    <option value="SP" {% if vaga and vaga.estado == 'SP' %}selected{% endif %}>SP</option>
                                    <!-- Adicionar outros estados conforme necessário -->
                                </select>
                            </div>
                        </div>

                        <div class="row">
                            <!-- Prazo de Candidatura -->
                            <div class="col-md-6 mb-3">
                                <label for="prazo_candidatura" class="form-label">Prazo de Candidatura</label>
                                <input type="date" class="form-control" id="prazo_candidatura" name="prazo_candidatura"
                                       value="{{ vaga.prazo_candidatura.strftime('%Y-%m-%d') if vaga and vaga.prazo_candidatura else '' }}">
                                <small class="text-muted">Deixe vazio para aceitar candidaturas indefinidamente.</small>
                            </div>

                            {% if vaga %}
                            <!-- Status (apenas na edição) -->
                            <div class="col-md-6 mb-3">
                                <label for="status_vaga" class="form-label">Status *</label>
                                <select class="form-select" id="status_vaga" name="status_vaga" required>
                                    <option value="aberta" {% if vaga.status == 'aberta' %}selected{% endif %}>Aberta</option>
                                    <option value="pausada" {% if vaga.status == 'pausada' %}selected{% endif %}>Pausada</option>
                                    <option value="fechada" {% if vaga.status == 'fechada' %}selected{% endif %}>Fechada</option>
                                </select>
                            </div>
                            {% endif %}
                        </div>

                        <!-- Botões -->
                        <div class="d-flex justify-content-between mt-4">
                            <a href="/empresa/vagas" class="btn btn-secondary">
                                <i class="bi bi-arrow-left"></i> Cancelar
                            </a>
                            <button type="submit" class="btn btn-success">
                                <i class="bi bi-check-circle"></i>
                                {% if vaga %}Atualizar Vaga{% else %}Publicar Vaga{% endif %}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- Sidebar com dicas -->
        <div class="col-lg-4">
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0"><i class="bi bi-lightbulb"></i> Dicas</h5>
                </div>
                <div class="card-body">
                    <h6>Título atrativo</h6>
                    <p class="small">Use palavras-chave que estudantes buscam. Seja específico sobre a área.</p>

                    <h6>Descrição clara</h6>
                    <p class="small">Explique as responsabilidades diárias e oportunidades de aprendizado.</p>

                    <h6>Requisitos realistas</h6>
                    <p class="small">Liste apenas requisitos essenciais. Seja flexível com estudantes em formação.</p>

                    <h6>Benefícios transparentes</h6>
                    <p class="small">Mencione bolsa-auxílio, vale-transporte, horário flexível, etc.</p>
                </div>
            </div>

            {% if empresa %}
            <div class="card mt-3">
                <div class="card-body">
                    <h6>Seu Plano: {{ empresa.plano }}</h6>
                    <div class="progress mb-2">
                        <div class="progress-bar" role="progressbar"
                             style="width: {{ (empresa.vagas_publicadas_mes / empresa.vagas_mensais_limite * 100) if empresa.vagas_mensais_limite > 0 else 0 }}%">
                        </div>
                    </div>
                    <small class="text-muted">
                        {{ empresa.vagas_publicadas_mes }} / {{ empresa.vagas_mensais_limite }} vagas este mês
                    </small>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

## 🔷 Passo 3.5: Template Lista de Candidatos

Crie o arquivo **templates/empresa/candidatos.html**:

```html
{% extends "base.html" %}

{% block title %}Candidatos - {{ vaga.titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho da Vaga -->
    <div class="d-flex justify-content-between align-items-start mb-4">
        <div>
            <h1>{{ vaga.titulo }}</h1>
            <p class="text-muted">
                <i class="bi bi-geo-alt"></i> {{ vaga.cidade }}, {{ vaga.estado }} •
                <i class="bi bi-briefcase"></i> {{ vaga.modalidade }}
            </p>
        </div>
        <div>
            <a href="/empresa/vagas/{{ vaga.id_vaga }}/editar" class="btn btn-outline-primary">
                <i class="bi bi-pencil"></i> Editar Vaga
            </a>
            <a href="/empresa/vagas" class="btn btn-secondary">
                <i class="bi bi-arrow-left"></i> Voltar
            </a>
        </div>
    </div>

    <!-- Estatísticas -->
    <div class="row mb-4">
        <div class="col-md-2">
            <div class="card text-center">
                <div class="card-body">
                    <h3 class="mb-0">{{ stats.total }}</h3>
                    <small class="text-muted">Total</small>
                </div>
            </div>
        </div>
        <div class="col-md-2">
            <div class="card text-center border-warning">
                <div class="card-body">
                    <h3 class="mb-0 text-warning">{{ stats.em_analise }}</h3>
                    <small class="text-muted">Em Análise</small>
                </div>
            </div>
        </div>
        <div class="col-md-2">
            <div class="card text-center border-info">
                <div class="card-body">
                    <h3 class="mb-0 text-info">{{ stats.entrevista }}</h3>
                    <small class="text-muted">Entrevista</small>
                </div>
            </div>
        </div>
        <div class="col-md-2">
            <div class="card text-center border-success">
                <div class="card-body">
                    <h3 class="mb-0 text-success">{{ stats.aprovado }}</h3>
                    <small class="text-muted">Aprovado</small>
                </div>
            </div>
        </div>
        <div class="col-md-2">
            <div class="card text-center border-danger">
                <div class="card-body">
                    <h3 class="mb-0 text-danger">{{ stats.recusado }}</h3>
                    <small class="text-muted">Recusado</small>
                </div>
            </div>
        </div>
    </div>

    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-body">
            <div class="btn-group" role="group">
                <a href="/empresa/vagas/{{ vaga.id_vaga }}/candidatos"
                   class="btn btn-outline-primary {% if not filtro_atual %}active{% endif %}">
                    Todos
                </a>
                <a href="/empresa/vagas/{{ vaga.id_vaga }}/candidatos?filtro_status=em_analise"
                   class="btn btn-outline-warning {% if filtro_atual == 'em_analise' %}active{% endif %}">
                    Em Análise
                </a>
                <a href="/empresa/vagas/{{ vaga.id_vaga }}/candidatos?filtro_status=entrevista"
                   class="btn btn-outline-info {% if filtro_atual == 'entrevista' %}active{% endif %}">
                    Entrevista
                </a>
                <a href="/empresa/vagas/{{ vaga.id_vaga }}/candidatos?filtro_status=aprovado"
                   class="btn btn-outline-success {% if filtro_atual == 'aprovado' %}active{% endif %}">
                    Aprovado
                </a>
                <a href="/empresa/vagas/{{ vaga.id_vaga }}/candidatos?filtro_status=recusado"
                   class="btn btn-outline-danger {% if filtro_atual == 'recusado' %}active{% endif %}">
                    Recusado
                </a>
            </div>
        </div>
    </div>

    <!-- Lista de Candidatos -->
    {% if candidaturas %}
        <div class="row">
            {% for candidatura in candidaturas %}
            <div class="col-md-6 mb-4">
                <div class="card h-100">
                    <div class="card-header">
                        <div class="d-flex justify-content-between align-items-center">
                            <h5 class="mb-0">{{ candidatura.candidato.nome }}</h5>
                            {% if candidatura.status == 'em_analise' %}
                                <span class="badge bg-warning text-dark">Em Análise</span>
                            {% elif candidatura.status == 'entrevista' %}
                                <span class="badge bg-info">Entrevista</span>
                            {% elif candidatura.status == 'aprovado' %}
                                <span class="badge bg-success">Aprovado</span>
                            {% elif candidatura.status == 'recusado' %}
                                <span class="badge bg-danger">Recusado</span>
                            {% endif %}
                        </div>
                    </div>
                    <div class="card-body">
                        <p class="mb-2">
                            <i class="bi bi-envelope"></i> {{ candidatura.candidato.email }}
                        </p>
                        {% if candidatura.candidato.telefone %}
                        <p class="mb-2">
                            <i class="bi bi-telephone"></i> {{ candidatura.candidato.telefone }}
                        </p>
                        {% endif %}
                        {% if candidatura.candidato.curso %}
                        <p class="mb-2">
                            <i class="bi bi-book"></i> {{ candidatura.candidato.curso }}
                            {% if candidatura.candidato.periodo %}
                                - {{ candidatura.candidato.periodo }}º período
                            {% endif %}
                        </p>
                        {% endif %}
                        {% if candidatura.candidato.instituicao %}
                        <p class="mb-2">
                            <i class="bi bi-building"></i> {{ candidatura.candidato.instituicao }}
                        </p>
                        {% endif %}

                        {% if candidatura.candidato.habilidades %}
                        <div class="mt-3">
                            <strong>Habilidades:</strong>
                            <div class="mt-1">
                                {% for habilidade in candidatura.candidato.habilidades.split(',') %}
                                <span class="badge bg-secondary me-1">{{ habilidade.strip() }}</span>
                                {% endfor %}
                            </div>
                        </div>
                        {% endif %}

                        {% if candidatura.observacoes %}
                        <div class="alert alert-info mt-3 mb-0">
                            <small><strong>Observações:</strong> {{ candidatura.observacoes }}</small>
                        </div>
                        {% endif %}

                        <div class="mt-3">
                            <small class="text-muted">
                                Candidatura em: {{ candidatura.data_candidatura.strftime('%d/%m/%Y às %H:%M') }}
                            </small>
                        </div>
                    </div>
                    <div class="card-footer">
                        <div class="d-flex justify-content-between align-items-center">
                            {% if candidatura.candidato.curriculo_arquivo %}
                            <a href="{{ candidatura.candidato.curriculo_arquivo }}"
                               target="_blank"
                               class="btn btn-sm btn-outline-primary">
                                <i class="bi bi-file-pdf"></i> Ver Currículo
                            </a>
                            {% else %}
                            <span class="text-muted small">Sem currículo</span>
                            {% endif %}

                            <button type="button" class="btn btn-sm btn-primary"
                                    data-bs-toggle="modal"
                                    data-bs-target="#modalStatus{{ candidatura.id_candidatura }}">
                                <i class="bi bi-gear"></i> Alterar Status
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Modal para alterar status -->
            <div class="modal fade" id="modalStatus{{ candidatura.id_candidatura }}" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <form method="POST" action="/empresa/candidaturas/{{ candidatura.id_candidatura }}/atualizar-status">
                            <div class="modal-header">
                                <h5 class="modal-title">Atualizar Status - {{ candidatura.candidato.nome }}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div class="mb-3">
                                    <label for="novo_status_{{ candidatura.id_candidatura }}" class="form-label">
                                        Novo Status
                                    </label>
                                    <select class="form-select"
                                            id="novo_status_{{ candidatura.id_candidatura }}"
                                            name="novo_status"
                                            required>
                                        <option value="em_analise" {% if candidatura.status == 'em_analise' %}selected{% endif %}>
                                            Em Análise
                                        </option>
                                        <option value="entrevista" {% if candidatura.status == 'entrevista' %}selected{% endif %}>
                                            Convocar para Entrevista
                                        </option>
                                        <option value="aprovado" {% if candidatura.status == 'aprovado' %}selected{% endif %}>
                                            Aprovar
                                        </option>
                                        <option value="recusado" {% if candidatura.status == 'recusado' %}selected{% endif %}>
                                            Recusar
                                        </option>
                                    </select>
                                </div>

                                <div class="mb-3">
                                    <label for="observacoes_{{ candidatura.id_candidatura }}" class="form-label">
                                        Observações (opcional)
                                    </label>
                                    <textarea class="form-control"
                                              id="observacoes_{{ candidatura.id_candidatura }}"
                                              name="observacoes"
                                              rows="3"
                                              placeholder="Adicione observações sobre esta candidatura...">{{ candidatura.observacoes if candidatura.observacoes else '' }}</textarea>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                    Cancelar
                                </button>
                                <button type="submit" class="btn btn-primary">
                                    Salvar Alterações
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="alert alert-info text-center">
            <i class="bi bi-info-circle"></i>
            {% if filtro_atual %}
                Nenhum candidato com status "{{ filtro_atual }}" nesta vaga.
            {% else %}
                Ainda não há candidatos para esta vaga.
            {% endif %}
        </div>
    {% endif %}
</div>
{% endblock %}
```

## 🔷 Passo 3.6: Template Detalhes de Vaga Pública

Crie o arquivo **templates/public/vaga_detalhes.html**:

```html
{% extends "base.html" %}

{% block title %}{{ vaga.titulo }} - Estagiou{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-lg-8">
            <!-- Cabeçalho -->
            <div class="card mb-4">
                <div class="card-body">
                    {% if vaga.destaque %}
                    <div class="alert alert-warning mb-3">
                        <i class="bi bi-star-fill"></i> <strong>Vaga em Destaque</strong>
                    </div>
                    {% endif %}

                    <h1 class="mb-3">{{ vaga.titulo }}</h1>

                    <div class="d-flex flex-wrap gap-2 mb-3">
                        <span class="badge bg-primary fs-6">
                            <i class="bi bi-tag"></i> {{ vaga.area.nome if vaga.area else "Geral" }}
                        </span>
                        <span class="badge bg-secondary fs-6">
                            <i class="bi bi-laptop"></i> {{ vaga.modalidade.capitalize() }}
                        </span>
                        <span class="badge bg-info fs-6">
                            <i class="bi bi-geo-alt"></i> {{ vaga.cidade }}, {{ vaga.estado }}
                        </span>
                        <span class="badge bg-dark fs-6">
                            <i class="bi bi-clock"></i> {{ vaga.carga_horaria }}
                        </span>
                    </div>

                    {% if vaga.empresa %}
                    <div class="d-flex align-items-center mb-3">
                        {% if vaga.empresa.logo %}
                        <img src="{{ vaga.empresa.logo }}" alt="{{ vaga.empresa.nome }}"
                             class="rounded me-3" style="width: 60px; height: 60px; object-fit: cover;">
                        {% endif %}
                        <div>
                            <h5 class="mb-0">{{ vaga.empresa.nome }}</h5>
                            <p class="text-muted mb-0 small">{{ vaga.empresa.setor if vaga.empresa.setor else '' }}</p>
                        </div>
                    </div>
                    {% endif %}

                    <div class="text-muted small">
                        <i class="bi bi-calendar"></i> Publicada em {{ vaga.data_publicacao.strftime('%d/%m/%Y') if vaga.data_publicacao else 'Hoje' }}
                        <span class="ms-3"><i class="bi bi-eye"></i> {{ vaga.visualizacoes }} visualizações</span>
                    </div>
                </div>
            </div>

            <!-- Descrição -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Descrição da Vaga</h5>
                </div>
                <div class="card-body">
                    <p style="white-space: pre-line;">{{ vaga.descricao }}</p>
                </div>
            </div>

            <!-- Requisitos -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Requisitos</h5>
                </div>
                <div class="card-body">
                    <p style="white-space: pre-line;">{{ vaga.requisitos }}</p>
                </div>
            </div>

            <!-- Benefícios -->
            {% if vaga.beneficios %}
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Benefícios</h5>
                </div>
                <div class="card-body">
                    <p style="white-space: pre-line;">{{ vaga.beneficios }}</p>
                </div>
            </div>
            {% endif %}
        </div>

        <!-- Sidebar -->
        <div class="col-lg-4">
            <!-- Botão de Candidatura -->
            <div class="card mb-4">
                <div class="card-body text-center">
                    {% if usuario_logado and usuario_logado.perfil == 'Estudante' %}
                        <form method="POST" action="/estudante/candidatar/{{ vaga.id_vaga }}">
                            <button type="submit" class="btn btn-success btn-lg w-100">
                                <i class="bi bi-file-earmark-text"></i> Candidatar-se
                            </button>
                        </form>
                        <small class="text-muted d-block mt-2">
                            Sua candidatura será enviada para análise
                        </small>
                    {% elif not usuario_logado %}
                        <a href="/login" class="btn btn-primary btn-lg w-100">
                            <i class="bi bi-box-arrow-in-right"></i> Fazer Login para Candidatar
                        </a>
                        <small class="text-muted d-block mt-2">
                            Ou <a href="/cadastro">criar uma conta</a>
                        </small>
                    {% endif %}
                </div>
            </div>

            <!-- Informações Adicionais -->
            <div class="card mb-4">
                <div class="card-header">
                    <h6 class="mb-0">Informações</h6>
                </div>
                <div class="card-body">
                    <div class="mb-2">
                        <strong>Status:</strong>
                        {% if vaga.status == 'aberta' %}
                            <span class="badge bg-success">Aberta</span>
                        {% elif vaga.status == 'fechada' %}
                            <span class="badge bg-danger">Fechada</span>
                        {% elif vaga.status == 'pausada' %}
                            <span class="badge bg-warning">Pausada</span>
                        {% endif %}
                    </div>

                    {% if vaga.prazo_candidatura %}
                    <div class="mb-2">
                        <strong>Prazo:</strong>
                        <span class="text-danger">
                            {{ vaga.prazo_candidatura.strftime('%d/%m/%Y') }}
                        </span>
                    </div>
                    {% endif %}

                    <div class="mb-2">
                        <strong>Modalidade:</strong> {{ vaga.modalidade.capitalize() }}
                    </div>

                    <div class="mb-2">
                        <strong>Carga Horária:</strong> {{ vaga.carga_horaria }}
                    </div>

                    <div class="mb-2">
                        <strong>Localização:</strong> {{ vaga.cidade }}, {{ vaga.estado }}
                    </div>
                </div>
            </div>

            <!-- Sobre a Empresa -->
            {% if vaga.empresa %}
            <div class="card">
                <div class="card-header">
                    <h6 class="mb-0">Sobre a Empresa</h6>
                </div>
                <div class="card-body">
                    <h6>{{ vaga.empresa.nome }}</h6>
                    {% if vaga.empresa.setor %}
                    <p class="small mb-2"><strong>Setor:</strong> {{ vaga.empresa.setor }}</p>
                    {% endif %}
                    {% if vaga.empresa.site %}
                    <a href="{{ vaga.empresa.site }}" target="_blank" class="btn btn-sm btn-outline-primary w-100">
                        <i class="bi bi-globe"></i> Visitar Site
                    </a>
                    {% endif %}
                    <a href="/empresas/{{ vaga.id_empresa }}" class="btn btn-sm btn-outline-secondary w-100 mt-2">
                        Ver Todas as Vagas
                    </a>
                </div>
            </div>
            {% endif %}
        </div>
    </div>

    <!-- Botão Voltar -->
    <div class="row mt-4">
        <div class="col-12">
            <a href="/vagas" class="btn btn-secondary">
                <i class="bi bi-arrow-left"></i> Voltar para Vagas
            </a>
        </div>
    </div>
</div>
{% endblock %}
```

### ✅ Checklist - Templates Completos
- [ ] Formulário de vaga (criar/editar) criado
- [ ] Lista de candidatos com modais criada
- [ ] Detalhes de vaga pública criado
- [ ] Sistema de badges e cards implementado
- [ ] Modais do Bootstrap implementados
- [ ] Templates responsivos finalizados

---

## ✅ CHECKPOINT - FASE 3 COMPLETA

Parabéns! Você completou a **Fase 3 - Templates e Interface**. Agora você tem:

✅ Templates completos para estudantes (busca, candidaturas)
✅ Templates completos para empresas (dashboard, formulário, candidatos)
✅ Templates públicos (detalhes de vaga)
✅ Interface responsiva com Bootstrap 5
✅ Componentes interativos (modals, tooltips, badges)

**📊 Progresso: ~85% do guia completo**

---

# 🚀 FASE 4: Melhorias e Recursos Adicionais

Nesta fase vamos adicionar melhorias e recursos extras para tornar o sistema mais completo.

## 🔷 Passo 4.1: Adicionar Método de Reativação de Empresa

No arquivo **sql/empresa_sql.py**, adicione a query:

```python
# Adicionar no final do arquivo
REATIVAR = """
    UPDATE empresa
    SET ativo = 1
    WHERE id_empresa = ?
"""
```

No arquivo **repo/empresa_repo.py**, adicione o método:

```python
def reativar(id_empresa: int) -> None:
    """Reativa uma empresa desativada."""
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(sql.REATIVAR, (id_empresa,))
        conn.commit()
        logger.info(f"Empresa ID {id_empresa} reativada")
```

## 🔷 Passo 4.2: Criar Sistema de Reset Mensal de Vagas

Crie o arquivo **util/cron_tasks.py** para tarefas agendadas:

```python
"""
Tarefas agendadas (cron jobs) do sistema.
"""
from datetime import datetime
from util.logger_config import logger
import repo.empresa_repo as empresa_repo


def resetar_contadores_mensais():
    """
    Reseta os contadores mensais de vagas publicadas.
    Deve ser executado no primeiro dia de cada mês.
    """
    try:
        empresas = empresa_repo.obter_todas()

        for empresa in empresas:
            if empresa.vagas_publicadas_mes > 0:
                empresa_repo.resetar_contador_mensal(empresa.id_empresa)

        logger.info(f"Contadores mensais resetados para {len(empresas)} empresas")

    except Exception as e:
        logger.error(f"Erro ao resetar contadores mensais: {e}", exc_info=True)


def verificar_prazos_vencidos():
    """
    Verifica e fecha vagas com prazo de candidatura vencido.
    Deve ser executado diariamente.
    """
    from datetime import date
    import repo.vaga_repo as vaga_repo

    try:
        vagas = vaga_repo.obter_abertas()
        hoje = date.today()
        vagas_fechadas = 0

        for vaga in vagas:
            if vaga.prazo_candidatura and vaga.prazo_candidatura < hoje:
                vaga_repo.atualizar_status(vaga.id_vaga, "fechada")
                vagas_fechadas += 1

        if vagas_fechadas > 0:
            logger.info(f"{vagas_fechadas} vagas fechadas automaticamente por prazo vencido")

    except Exception as e:
        logger.error(f"Erro ao verificar prazos: {e}", exc_info=True)


# Nota: Para usar essas funções em produção, você pode:
# 1. Usar APScheduler para agendamento dentro do FastAPI
# 2. Usar cron do sistema operacional
# 3. Usar Celery para tarefas assíncronas
```

## 🔷 Passo 4.3: Adicionar Validações Extras nos DTOs

Abra **dtos/vaga_dto.py** e adicione validações de data:

```python
from datetime import date
from pydantic import field_validator

# Adicionar ao VagaCriarDTO:
@field_validator('prazo_candidatura')
def validar_prazo_futuro(cls, v):
    """Valida se o prazo é no futuro."""
    if v and v < date.today():
        raise ValueError('O prazo de candidatura deve ser uma data futura')
    return v
```

## 🔷 Passo 4.4: Criar Página Inicial Melhorada

Atualize o arquivo **templates/index.html** (ou crie se não existir):

```html
{% extends "base.html" %}

{% block title %}Estagiou - Conectando Estudantes e Empresas{% endblock %}

{% block content %}
<!-- Hero Section -->
<div class="bg-primary text-white py-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <h1 class="display-4 fw-bold mb-4">
                    Encontre seu estágio ideal
                </h1>
                <p class="lead mb-4">
                    A plataforma que conecta estudantes talentosos com empresas inovadoras.
                </p>
                <div class="d-flex gap-3">
                    {% if not usuario_logado %}
                    <a href="/cadastro" class="btn btn-light btn-lg">
                        <i class="bi bi-person-plus"></i> Cadastrar-se
                    </a>
                    <a href="/vagas" class="btn btn-outline-light btn-lg">
                        <i class="bi bi-search"></i> Buscar Vagas
                    </a>
                    {% else %}
                        {% if usuario_logado.perfil == 'Estudante' %}
                        <a href="/estudante/vagas" class="btn btn-light btn-lg">
                            <i class="bi bi-search"></i> Buscar Vagas
                        </a>
                        {% elif usuario_logado.perfil == 'Recrutador' %}
                        <a href="/empresa/dashboard" class="btn btn-light btn-lg">
                            <i class="bi bi-speedometer2"></i> Dashboard
                        </a>
                        {% endif %}
                    {% endif %}
                </div>
            </div>
            <div class="col-lg-6 d-none d-lg-block">
                <img src="/static/img/hero-illustration.svg" alt="Ilustração" class="img-fluid">
            </div>
        </div>
    </div>
</div>

<!-- Estatísticas -->
<div class="container my-5">
    <div class="row text-center">
        <div class="col-md-3">
            <div class="card border-0 shadow-sm">
                <div class="card-body">
                    <h2 class="text-primary">{{ stats.total_vagas }}</h2>
                    <p class="text-muted">Vagas Disponíveis</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-0 shadow-sm">
                <div class="card-body">
                    <h2 class="text-success">{{ stats.total_empresas }}</h2>
                    <p class="text-muted">Empresas Parceiras</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-0 shadow-sm">
                <div class="card-body">
                    <h2 class="text-info">{{ stats.total_estudantes }}</h2>
                    <p class="text-muted">Estudantes Cadastrados</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-0 shadow-sm">
                <div class="card-body">
                    <h2 class="text-warning">{{ stats.total_candidaturas }}</h2>
                    <p class="text-muted">Candidaturas Enviadas</p>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Vagas em Destaque -->
{% if vagas_destaque %}
<div class="bg-light py-5">
    <div class="container">
        <h2 class="text-center mb-5">Vagas em Destaque</h2>
        <div class="row">
            {% for vaga in vagas_destaque %}
            <div class="col-md-4 mb-4">
                <div class="card h-100 border-warning shadow">
                    <div class="card-header bg-warning text-dark">
                        <i class="bi bi-star-fill"></i> Destaque
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">{{ vaga.titulo }}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">
                            {{ vaga.empresa.nome if vaga.empresa else '' }}
                        </h6>
                        <p class="card-text">
                            {{ vaga.descricao[:100] }}...
                        </p>
                        <div class="mb-2">
                            <span class="badge bg-primary">{{ vaga.area.nome if vaga.area else 'Geral' }}</span>
                            <span class="badge bg-secondary">{{ vaga.modalidade }}</span>
                        </div>
                    </div>
                    <div class="card-footer">
                        <a href="/vagas/{{ vaga.id_vaga }}" class="btn btn-primary w-100">
                            Ver Detalhes
                        </a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        <div class="text-center mt-4">
            <a href="/vagas" class="btn btn-outline-primary btn-lg">
                Ver Todas as Vagas
            </a>
        </div>
    </div>
</div>
{% endif %}

<!-- Como Funciona -->
<div class="container my-5">
    <h2 class="text-center mb-5">Como Funciona</h2>
    <div class="row">
        <div class="col-md-4 text-center mb-4">
            <div class="mb-3">
                <i class="bi bi-person-plus-fill text-primary" style="font-size: 3rem;"></i>
            </div>
            <h4>1. Cadastre-se</h4>
            <p class="text-muted">
                Crie sua conta como estudante ou empresa em poucos minutos
            </p>
        </div>
        <div class="col-md-4 text-center mb-4">
            <div class="mb-3">
                <i class="bi bi-search text-success" style="font-size: 3rem;"></i>
            </div>
            <h4>2. Busque ou Publique</h4>
            <p class="text-muted">
                Estudantes buscam vagas, empresas publicam oportunidades
            </p>
        </div>
        <div class="col-md-4 text-center mb-4">
            <div class="mb-3">
                <i class="bi bi-check-circle-fill text-info" style="font-size: 3rem;"></i>
            </div>
            <h4>3. Conecte-se</h4>
            <p class="text-muted">
                Candidaturas são enviadas e empresas analisam perfis
            </p>
        </div>
    </div>
</div>

<!-- Call to Action -->
<div class="bg-primary text-white py-5">
    <div class="container text-center">
        <h2 class="mb-4">Pronto para começar?</h2>
        <p class="lead mb-4">
            Junte-se a centenas de estudantes e empresas que já encontraram sua oportunidade ideal
        </p>
        {% if not usuario_logado %}
        <a href="/cadastro" class="btn btn-light btn-lg me-2">
            Cadastrar como Estudante
        </a>
        <a href="/cadastro?tipo=empresa" class="btn btn-outline-light btn-lg">
            Cadastrar Empresa
        </a>
        {% endif %}
    </div>
</div>
{% endblock %}
```

Atualize **routes/public_routes.py** para incluir estatísticas:

```python
@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Página inicial."""

    # Obter estatísticas
    stats = {
        "total_vagas": len(vaga_repo.obter_abertas()),
        "total_empresas": len(empresa_repo.obter_todas()),
        "total_estudantes": len([u for u in usuario_repo.obter_todos() if u.perfil == Perfil.ESTUDANTE.value]),
        "total_candidaturas": len(candidatura_repo.obter_todas()) if hasattr(candidatura_repo, 'obter_todas') else 0
    }

    # Obter vagas em destaque
    vagas_destaque = [v for v in vaga_repo.obter_abertas() if v.destaque][:3]

    usuario_logado = obter_usuario_logado(request)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "stats": stats,
            "vagas_destaque": vagas_destaque
        }
    )
```

### ✅ Checklist - Melhorias Adicionadas
- [ ] Sistema de reativação de empresa implementado
- [ ] Tarefas agendadas criadas (reset mensal, prazos)
- [ ] Validações extras nos DTOs
- [ ] Página inicial melhorada com estatísticas
- [ ] Vagas em destaque na home

---

## ✅ CHECKPOINT - FASE 4 COMPLETA

Você completou a **Fase 4 - Melhorias e Recursos Adicionais**!

**📊 Progresso: ~95% do guia completo**

---

# 📝 FASE 5: Finalização e Próximos Passos

## 🔷 Resumo do que foi implementado

### ✅ Infraestrutura Base (Já existia)
- FastAPI + Uvicorn
- SQLite com queries SQL
- Sistema de autenticação
- Templates Jinja2
- Bootstrap 5

### ✅ Fase 1 - Fundação (Implementado neste guia)
- 3 perfis de usuário (Admin, Estudante, Recrutador)
- 6 modelos completos (Usuario, Empresa, Vaga, Candidatura, Area, Endereco)
- 6 arquivos SQL com todas as queries
- 5 repositórios completos
- 5 DTOs com validações Pydantic
- Seeds de dados iniciais

### ✅ Fase 2 - Funcionalidades (Implementado neste guia)
- Rotas públicas (visualizar vagas, empresas)
- Rotas de estudante (buscar, candidatar, perfil)
- Rotas de empresa (dashboard, CRUD vagas, candidatos)
- Rotas administrativas (vagas, áreas, empresas)
- Sistema de planos e limites mensais

### ✅ Fase 3 - Interface (Implementado neste guia)
- Templates para estudantes
- Templates para empresas
- Templates administrativos
- Templates públicos
- Interface responsiva completa

### ✅ Fase 4 - Melhorias (Implementado neste guia)
- Tarefas agendadas
- Validações extras
- Página inicial melhorada
- Sistema de destaques

## 🔷 Próximos Passos Recomendados

### 1. Testes
```bash
# Criar testes unitários
pytest tests/test_repos.py
pytest tests/test_routes.py
```

### 2. Deploy
- Configurar variáveis de ambiente para produção
- Usar PostgreSQL em vez de SQLite
- Configurar HTTPS
- Deploy em Heroku, Railway ou AWS

### 3. Funcionalidades Futuras
- Sistema de mensagens entre empresa e estudante
- Sistema de avaliações
- Notificações por email
- Dashboard de analytics
- Sistema de match automático
- API REST completa

### 4. Segurança
- Rate limiting
- CORS configurado
- Validação de CSRF tokens
- Sanitização de inputs
- Backup automático do banco

## 🎉 PARABÉNS!

Você tem agora um guia completo para implementar o sistema **Estagiou** do zero!

Tempo estimado de implementação: **6-8 semanas** (seguindo este guia passo a passo)

**Boa sorte com o desenvolvimento! 🚀**
