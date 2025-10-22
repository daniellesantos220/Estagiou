# PLANO DE IMPLEMENTAÇÃO DO BACKEND - ESTAGIOU

**Projeto**: Estagiou - Oportunidades que Transformam
**Objetivo**: Transformar o projeto atual em uma plataforma completa de gestão de estágios
**Foco**: Backend apenas (models, repos, DTOs, routes) - sem templates

---

## SUMÁRIO

1. [INTRODUÇÃO E ANÁLISE](#1-introdução-e-análise)
2. [ESTADO ATUAL DO PROJETO](#2-estado-atual-do-projeto)
3. [ANÁLISE DOS REQUISITOS](#3-análise-dos-requisitos)
4. [MAPEAMENTO BACKEND](#4-mapeamento-backend)
5. [GUIA DE IMPLEMENTAÇÃO](#5-guia-de-implementação)
   - [5.1 Adaptação dos Perfis](#51-adaptação-dos-perfis)
   - [5.2 Expansão do Model Usuario](#52-expansão-do-model-usuario)
   - [5.3 Novos Models](#53-novos-models)
   - [5.4 Novos SQL Statements](#54-novos-sql-statements)
   - [5.5 Novos Repositórios](#55-novos-repositórios)
   - [5.6 Novos DTOs](#56-novos-dtos)
   - [5.7 Novas Rotas](#57-novas-rotas)
   - [5.8 Sistema de Mensagens](#58-sistema-de-mensagens)
   - [5.9 Sistema de Notificações](#59-sistema-de-notificações)
   - [5.10 Sistema de Avaliações](#510-sistema-de-avaliações)

---

## 1. INTRODUÇÃO E ANÁLISE

### 1.1 Visão Geral do Estagiou

O **Estagiou** é uma plataforma de gestão de estágios que conecta estudantes, empresas e instituições de ensino. Principais características:

- **Para Estudantes**: Buscar vagas, candidatar-se, acompanhar status, gerenciar currículo
- **Para Empresas/Recrutadores**: Publicar vagas, gerenciar candidaturas, avaliar candidatos
- **Para Administradores**: Gerenciar usuários, áreas de atuação, configurações da plataforma
- **Para Visitantes Anônimos**: Visualizar vagas disponíveis, informações públicas

### 1.2 Análise do PDF

O PDF apresenta 32 páginas com:
- **Briefing completo**: objetivos, público-alvo, tecnologias, modelo de monetização
- **Requisitos Funcionais**: 68 requisitos divididos em alta, média e baixa prioridade
- **Requisitos Não-Funcionais**: 19 requisitos focando segurança, performance, usabilidade
- **Diagramas de Casos de Uso**: para Usuário, Anônimo, Estudante, Administrador, Recrutador
- **Diagrama ER**: Candidatura, Vaga, Area, Usuário, Empresa, Endereco

### 1.3 Objetivos deste Documento

Este documento fornece:
1. **Análise detalhada**: comparação entre estado atual e requisitos do PDF
2. **Mapeamento completo**: quais requisitos geram quais componentes backend
3. **Guia passo a passo**: como implementar cada componente, mantendo os padrões do projeto

---

## 2. ESTADO ATUAL DO PROJETO

### 2.1 Estrutura Existente

O projeto atual já possui uma base sólida:

#### Models Existentes
- ✅ `usuario_model.py` - Model de usuário (id, nome, email, senha, perfil)
- ✅ `area_model.py` - Model de área (id_area, nome, descricao)
- ✅ `empresa_model.py` - Model de empresa (id_empresa, nome, cnpj, descricao)
- ✅ `vaga_model.py` - Model de vaga (com relacionamentos)
- ✅ `candidatura_model.py` - Model de candidatura
- ✅ `endereco_model.py` - Model de endereço
- ✅ `tarefa_model.py` - Model de tarefa (pode ser removido ou adaptado)
- ✅ `configuracao_model.py` - Model de configuração

#### Repositórios Existentes
- ✅ `usuario_repo.py` - CRUD completo para usuários
- ✅ `configuracao_repo.py` - Gerenciamento de configurações
- ✅ `tarefa_repo.py` - Gerenciamento de tarefas (pode ser removido)

#### DTOs Existentes
- ✅ `auth_dto.py` - LoginDTO, CadastroDTO, EsqueciSenhaDTO, RedefinirSenhaDTO
- ✅ `usuario_dto.py` - CriarUsuarioDTO, AlterarUsuarioDTO
- ✅ `perfil_dto.py` - AlterarPerfilDTO, AlterarSenhaDTO
- ✅ `validators.py` - Validadores reutilizáveis

#### Rotas Existentes
- ✅ `auth_routes.py` - Login, cadastro, recuperação de senha (completo)
- ✅ `usuario_routes.py` - Gerenciamento de usuários
- ✅ `perfil_routes.py` - Edição de perfil
- ✅ `admin_usuarios_routes.py` - Admin gerencia usuários
- ✅ `admin_configuracoes_routes.py` - Admin gerencia configurações
- ✅ `admin_backups_routes.py` - Admin gerencia backups
- ✅ `public_routes.py` - Rotas públicas
- ✅ `tarefas_routes.py` - Gerenciamento de tarefas (pode ser removido)

#### Utilitários Existentes
- ✅ `security.py` - Hash de senhas, tokens, verificação
- ✅ `email_service.py` - Envio de emails
- ✅ `foto_util.py` - Gerenciamento de fotos
- ✅ `perfis.py` - Enum de perfis (ADMIN, CLIENTE, VENDEDOR)
- ✅ `auth_decorator.py` - Decorators para autenticação/autorização
- ✅ `exceptions.py` e `exception_handlers.py` - Tratamento de erros
- ✅ `db_util.py` - Conexão com banco de dados

### 2.2 Padrões Identificados

O projeto segue padrões consistentes:

1. **Models**: Dataclasses simples em `model/*.py`
2. **SQL Statements**: Constantes em `sql/*_sql.py`
3. **Repositórios**: Funções em `repo/*_repo.py` usando context manager
4. **DTOs**: Pydantic BaseModel em `dtos/*_dto.py` com validadores
5. **Rotas**: FastAPI Router em `routes/*_routes.py`
6. **Validação**: Decorators `@exigir_login` e `@exigir_perfil`

---

## 3. ANÁLISE DOS REQUISITOS

### 3.1 Requisitos Funcionais por Ator

#### ESTUDANTE (RFs: 1-9, 29-35, 48-51, 52-57, 68)
- **Gerenciamento de Conta**: cadastro, login, edição de perfil, alterar senha, recuperar senha, excluir conta
- **Busca e Candidatura**: buscar vagas, candidatar-se, cancelar candidatura, acompanhar status
- **Currículo**: gerenciar currículo em PDF, exportar currículo
- **Recursos Extras**: salvar vagas favoritas, avaliar empresas, receber notificações, enviar mensagens

#### RECRUTADOR/EMPRESA (RFs: 10-21, 38-43, 58-63)
- **Gerenciamento de Conta**: cadastrar empresa, editar perfil, login/logout, recuperar senha
- **Gerenciamento de Vagas**: criar, editar, excluir, arquivar, renovar vagas, alterar status
- **Gerenciamento de Candidaturas**: visualizar candidatos, filtrar, marcar status, enviar mensagens
- **Recursos Extras**: visualizar estatísticas, exportar dados, relatórios, notificações

#### ADMINISTRADOR (RFs: 22-24, 44)
- **Gerenciamento de Usuários**: criar, editar, ativar/desativar, definir níveis de acesso
- **Gerenciamento de Vagas**: aprovar, editar, remover, destacar vagas
- **Gerenciamento de Áreas**: criar e gerenciar áreas de atuação
- **Configurações**: ajustar regras do sistema, termos de uso, políticas
- **Relatórios**: acompanhar estatísticas da plataforma

#### ANÔNIMO (RFs: 25-28, 45-47, 65-67)
- **Visualização**: ver vagas, informações de empresas, estatísticas gerais, FAQ
- **Ações**: fazer login, cadastrar-se, compartilhar vagas, contatar suporte

### 3.2 Entidades do Diagrama ER

Conforme página 31 do PDF:

1. **Usuario** - id, nome, data_nascimento, email, numero_documento, telefone, senha, perfil, confirmado
2. **Empresa** - id_empresa, nome, cnpj, descricao
3. **Endereco** - id_endereco, id_usuario, titulo, logradouro, numero, complemento, bairro, cidade, uf, cep
4. **Area** - id_area, nome, descricao
5. **Vaga** - id_vaga, id_area, id_empresa, id_recrutador, status_vaga, descricao, numero_vaga, salario, data_cadastro
6. **Candidatura** - id_candidatura, id_vaga, id_candidato, data_candidatura, status

### 3.3 Gaps Identificados

Comparando estado atual vs requisitos:

| Componente | Status | Ação Necessária |
|-----------|--------|-----------------|
| **Perfis** | ❌ Parcial | Adaptar de CLIENTE/VENDEDOR para ESTUDANTE/RECRUTADOR |
| **Usuario Model** | ⚠️ Incompleto | Adicionar: data_nascimento, telefone, numero_documento, confirmado |
| **Empresa Repo** | ❌ Não existe | Criar repositório completo |
| **Vaga Repo** | ❌ Não existe | Criar repositório completo |
| **Candidatura Repo** | ❌ Não existe | Criar repositório completo |
| **Area Repo** | ❌ Não existe | Criar repositório completo |
| **Endereco Repo** | ❌ Não existe | Criar repositório completo |
| **Rotas de Empresa** | ❌ Não existe | Criar rotas completas |
| **Rotas de Vaga** | ❌ Não existe | Criar rotas completas |
| **Rotas de Candidatura** | ❌ Não existe | Criar rotas completas |
| **Rotas de Estudante** | ❌ Não existe | Criar rotas específicas |
| **Rotas de Recrutador** | ❌ Não existe | Criar rotas específicas |
| **Sistema de Mensagens** | ❌ Não existe | Criar do zero |
| **Sistema de Notificações** | ❌ Não existe | Criar do zero |
| **Sistema de Avaliações** | ❌ Não existe | Criar do zero |

---

## 4. MAPEAMENTO BACKEND

### 4.1 Requisitos → Componentes

#### RF1-RF9: Estudante - Gerenciamento Básico
**Componentes necessários:**
- ✅ `auth_routes.py` - já existe (login, cadastro, recuperação)
- ✅ `perfil_routes.py` - já existe (editar perfil, alterar senha)
- ⚠️ Adaptar cadastro para incluir perfil ESTUDANTE
- 🆕 `estudante_routes.py` - rotas específicas de estudante

#### RF10-RF21: Empresa/Recrutador
**Componentes necessários:**
- 🆕 `empresa_model.py` - já existe (modelo básico)
- 🆕 `empresa_repo.py` - criar CRUD completo
- 🆕 `empresa_sql.py` - criar statements SQL
- 🆕 `empresa_dto.py` - criar DTOs com validação
- 🆕 `empresa_routes.py` - criar rotas de gerenciamento

#### RF6, RF15-RF19, RF32, RF41, RF48: Vagas
**Componentes necessários:**
- 🆕 `vaga_model.py` - já existe (modelo básico)
- 🆕 `vaga_repo.py` - criar CRUD completo
- 🆕 `vaga_sql.py` - criar statements SQL
- 🆕 `vaga_dto.py` - criar DTOs com validação
- 🆕 `vaga_routes.py` - criar rotas de gerenciamento
- 🆕 Funções de busca com filtros avançados

#### RF7-RF9, RF20-RF21, RF33-RF34, RF38-RF42: Candidaturas
**Componentes necessários:**
- 🆕 `candidatura_model.py` - já existe (modelo básico)
- 🆕 `candidatura_repo.py` - criar CRUD completo
- 🆕 `candidatura_sql.py` - criar statements SQL
- 🆕 `candidatura_dto.py` - criar DTOs com validação
- 🆕 `candidatura_routes.py` - criar rotas de gerenciamento

#### RF22-RF24, RF44: Administrador
**Componentes necessários:**
- ✅ `admin_usuarios_routes.py` - já existe
- 🆕 `admin_areas_routes.py` - criar para gerenciar áreas
- 🆕 `area_repo.py` - criar CRUD
- 🆕 `area_sql.py` - criar statements
- 🆕 `area_dto.py` - criar DTOs

#### RF25-RF28, RF45-RF47, RF65-RF67: Anônimo
**Componentes necessários:**
- ✅ `public_routes.py` - já existe
- ⚠️ Adaptar para mostrar vagas públicas
- 🆕 Adicionar endpoints de estatísticas

#### RF31, RF51, RF68: Currículo
**Componentes necessários:**
- 🆕 Adaptar `foto_util.py` para `arquivo_util.py`
- 🆕 Adicionar campo `curriculo_path` em Usuario
- 🆕 Funções upload/download/exclusão de PDF

#### RF43, RF50: Mensagens
**Componentes necessários:**
- 🆕 `mensagem_model.py`
- 🆕 `mensagem_repo.py`
- 🆕 `mensagem_sql.py`
- 🆕 `mensagem_dto.py`
- 🆕 `mensagem_routes.py`

#### RF49, RF56: Notificações
**Componentes necessários:**
- 🆕 `notificacao_model.py`
- 🆕 `notificacao_repo.py`
- 🆕 `notificacao_sql.py`
- 🆕 Sistema de geração automática de notificações

#### RF52, RF36: Avaliações
**Componentes necessários:**
- 🆕 `avaliacao_model.py`
- 🆕 `avaliacao_repo.py`
- 🆕 `avaliacao_sql.py`
- 🆕 `avaliacao_dto.py`
- 🆕 `avaliacao_routes.py`

### 4.2 Priorização da Implementação

**FASE 1 - FUNDAÇÃO (Alta Prioridade)**
1. Adaptar perfis (util/perfis.py)
2. Expandir Usuario model
3. Criar repos básicos (empresa, area, vaga, candidatura)
4. Criar DTOs básicos
5. Criar rotas principais (empresa, vaga, candidatura)

**FASE 2 - FUNCIONALIDADES CORE (Alta Prioridade)**
6. Sistema de busca de vagas
7. Sistema de candidaturas
8. Gerenciamento de empresas
9. Rotas de estudante e recrutador
10. Adaptações nas rotas públicas

**FASE 3 - RECURSOS EXTRAS (Média Prioridade)**
11. Sistema de mensagens
12. Sistema de notificações
13. Sistema de avaliações
14. Gerenciamento de currículo
15. Estatísticas e relatórios

**FASE 4 - MELHORIAS (Baixa Prioridade)**
16. Vagas favoritas
17. Integração com LinkedIn/Google
18. Exportação de dados
19. Agendamento de entrevistas
20. Comunicados automáticos

---

## 5. GUIA DE IMPLEMENTAÇÃO

### 5.1 Adaptação dos Perfis

**Arquivo:** `util/perfis.py`

#### O que modificar:
Substituir os perfis atuais (ADMIN, CLIENTE, VENDEDOR) pelos perfis do Estagiou (ADMIN, ESTUDANTE, RECRUTADOR).

#### Código completo atualizado:

```python
from enum import Enum
from typing import Optional

class Perfil(str, Enum):
    """
    Enum centralizado para perfis de usuário do Estagiou.

    Este é a FONTE ÚNICA DA VERDADE para perfis no sistema.
    SEMPRE use este Enum ao referenciar perfis, NUNCA strings literais.

    Exemplos:
        - Correto: perfil = Perfil.ADMIN.value
        - Correto: perfil = Perfil.ESTUDANTE.value
        - Correto: perfil = Perfil.RECRUTADOR.value
        - ERRADO: perfil = "Administrador"
        - ERRADO: perfil = "Estudante"
    """

    # PERFIS DO ESTAGIOU #######################################
    ADMIN = "Administrador"
    ESTUDANTE = "Estudante"
    RECRUTADOR = "Recrutador"
    # FIM DOS PERFIS ############################################

    def __str__(self) -> str:
        """Retorna o valor do perfil como string"""
        return self.value

    @classmethod
    def valores(cls) -> list[str]:
        """
        Retorna lista de todos os valores de perfis.

        Returns:
            Lista com os valores: ["Administrador", "Estudante", "Recrutador"]
        """
        return [perfil.value for perfil in cls]

    @classmethod
    def existe(cls, valor: str) -> bool:
        """Verifica se um valor de perfil é válido."""
        return valor in cls.valores()

    @classmethod
    def from_string(cls, valor: str) -> Optional['Perfil']:
        """Converte uma string para o Enum Perfil correspondente."""
        try:
            return cls(valor)
        except ValueError:
            return None

    @classmethod
    def validar(cls, valor: str) -> str:
        """Valida e retorna o valor do perfil."""
        if not cls.existe(valor):
            raise ValueError(f'Perfil inválido: {valor}. Use: {", ".join(cls.valores())}')
        return valor
```

#### Impactos dessa mudança:
- ✅ Atualizar valor padrão em `sql/usuario_sql.py` (CRIAR_TABELA)
- ✅ Atualizar templates de cadastro (não coberto neste documento)
- ✅ Atualizar seeds em `util/seed_data.py`

---

### 5.2 Expansão do Model Usuario

**Arquivo:** `model/usuario_model.py`

#### O que adicionar:
Campos necessários conforme diagrama ER do PDF.

#### Código completo atualizado:

```python
from dataclasses import dataclass
from typing import Optional
from util.perfis import Perfil

@dataclass
class Usuario:
    """
    Model de usuário do sistema Estagiou.

    Attributes:
        id: Identificador único do usuário
        nome: Nome completo do usuário
        email: E-mail único do usuário
        senha: Hash da senha do usuário
        perfil: Perfil do usuário (Perfil.ADMIN.value, Perfil.ESTUDANTE.value, Perfil.RECRUTADOR.value)

        # Novos campos do Estagiou
        data_nascimento: Data de nascimento (formato: YYYY-MM-DD)
        telefone: Telefone de contato (opcional)
        numero_documento: CPF ou outro documento (opcional)
        confirmado: Se o usuário confirmou o e-mail (boolean)
        curriculo_path: Caminho para o arquivo de currículo em PDF (opcional)

        # Campos de recuperação de senha
        token_redefinicao: Token para redefinição de senha (opcional)
        data_token: Data de expiração do token (opcional)
        data_cadastro: Data de cadastro do usuário (opcional)

    Nota: A foto do usuário é armazenada no filesystem em /static/img/usuarios/{id:06d}.jpg
          O currículo é armazenado em /static/curriculos/{id:06d}.pdf
    """
    id: int
    nome: str
    email: str
    senha: str
    perfil: str

    # Novos campos
    data_nascimento: Optional[str] = None
    telefone: Optional[str] = None
    numero_documento: Optional[str] = None
    confirmado: bool = False
    curriculo_path: Optional[str] = None

    # Campos existentes
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None
    data_cadastro: Optional[str] = None
```

#### SQL correspondente:
Atualizar `sql/usuario_sql.py`:

```python
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
```

#### Atualizar repositório:
Modificar `repo/usuario_repo.py` para usar os novos campos:

```python
def inserir(usuario: Usuario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            usuario.nome,
            usuario.email,
            usuario.senha,
            usuario.perfil,
            usuario.data_nascimento,
            usuario.telefone,
            usuario.numero_documento
        ))
        usuario_id = cursor.lastrowid

        if usuario_id:
            criar_foto_padrao_usuario(usuario_id)

        return usuario_id

def alterar(usuario: Usuario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            usuario.nome,
            usuario.email,
            usuario.perfil,
            usuario.data_nascimento,
            usuario.telefone,
            usuario.numero_documento,
            usuario.id
        ))
        return cursor.rowcount > 0

def atualizar_curriculo(id: int, curriculo_path: str) -> bool:
    """Atualiza o caminho do currículo do usuário."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_CURRICULO, (curriculo_path, id))
        return cursor.rowcount > 0

def confirmar_email(id: int) -> bool:
    """Marca o e-mail do usuário como confirmado."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONFIRMAR_EMAIL, (id,))
        return cursor.rowcount > 0
```

#### Atualizar obter_por_id e obter_todos:
```python
def obter_por_id(id: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Usuario(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                data_nascimento=row.get("data_nascimento"),
                telefone=row.get("telefone"),
                numero_documento=row.get("numero_documento"),
                confirmado=bool(row.get("confirmado", 0)),
                curriculo_path=row.get("curriculo_path"),
                token_redefinicao=row.get("token_redefinicao"),
                data_token=row.get("data_token"),
                data_cadastro=row.get("data_cadastro")
            )
        return None
```

---

### 5.3 Novos Models

Os models já existem como esqueletos básicos. Vamos validá-los e ajustá-los conforme o diagrama ER do PDF.

#### 5.3.1 Area Model

**Arquivo:** `model/area_model.py`

✅ **Já está correto!** Não precisa modificar.

```python
from dataclasses import dataclass

@dataclass
class Area:
    id_area: int
    nome: str
    descricao: str
```

#### 5.3.2 Empresa Model

**Arquivo:** `model/empresa_model.py`

⚠️ **Precisa ajustar o tipo do CNPJ**:

```python
from dataclasses import dataclass

@dataclass
class Empresa:
    """
    Model de empresa no sistema Estagiou.

    Attributes:
        id_empresa: Identificador único da empresa
        nome: Nome da empresa
        cnpj: CNPJ da empresa (string para preservar formatação)
        descricao: Descrição da empresa
    """
    id_empresa: int
    nome: str
    cnpj: str  # Alterado de int para str
    descricao: str
```

#### 5.3.3 Endereco Model

**Arquivo:** `model/endereco_model.py`

✅ **Já está correto!** Não precisa modificar.

```python
from dataclasses import dataclass

@dataclass
class Endereco:
    id_endereco: int
    id_usuario: int
    titulo: str
    logradouro: str
    numero: str
    complemento: str
    bairro: str
    cidade: str
    uf: str
    cep: str
```

#### 5.3.4 Vaga Model

**Arquivo:** `model/vaga_model.py`

⚠️ **Precisa ajustar campos conforme PDF**:

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Vaga:
    """
    Model de vaga de estágio no sistema Estagiou.

    Attributes:
        id_vaga: Identificador único da vaga
        id_area: FK para Area
        id_empresa: FK para Empresa
        id_recrutador: FK para Usuario (recrutador que criou a vaga)
        status_vaga: Status da vaga (aberta, fechada, pausada, arquivada)
        descricao: Descrição detalhada da vaga
        numero_vagas: Quantidade de vagas disponíveis
        salario: Valor da bolsa/salário
        data_cadastro: Data de criação da vaga

        # Campos adicionais sugeridos (não estão no diagrama ER mas são úteis)
        titulo: Título da vaga
        requisitos: Requisitos da vaga
        beneficios: Benefícios oferecidos
        carga_horaria: Carga horária semanal
        modalidade: Presencial, Remoto ou Híbrido
        cidade: Cidade da vaga
        uf: Estado da vaga

        # Relacionamentos (populados via JOIN)
        area: Objeto Area (opcional)
        empresa: Objeto Empresa (opcional)
        recrutador: Objeto Usuario (opcional)
    """
    id_vaga: int
    id_area: int
    id_empresa: int
    id_recrutador: int
    status_vaga: str
    descricao: str
    numero_vagas: int
    salario: float
    data_cadastro: str

    # Campos adicionais
    titulo: Optional[str] = None
    requisitos: Optional[str] = None
    beneficios: Optional[str] = None
    carga_horaria: Optional[int] = None
    modalidade: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None

    # Relacionamentos
    area: Optional[object] = None  # Será Area
    empresa: Optional[object] = None  # Será Empresa
    recrutador: Optional[object] = None  # Será Usuario
```

#### 5.3.5 Candidatura Model

**Arquivo:** `model/candidatura_model.py`

⚠️ **Precisa corrigir nome do campo (Status → status)**:

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Candidatura:
    """
    Model de candidatura a uma vaga no sistema Estagiou.

    Attributes:
        id_candidatura: Identificador único da candidatura
        id_vaga: FK para Vaga
        id_candidato: FK para Usuario (estudante que se candidatou)
        data_candidatura: Data da candidatura
        status: Status da candidatura (pendente, em_analise, aprovado, rejeitado, cancelado)

        # Relacionamentos (populados via JOIN)
        vaga: Objeto Vaga (opcional)
        candidato: Objeto Usuario (opcional)
    """
    id_candidatura: int
    id_vaga: int
    id_candidato: int
    data_candidatura: str
    status: str  # Corrigido de "Status" para "status"

    # Relacionamentos
    vaga: Optional[object] = None  # Será Vaga
    candidato: Optional[object] = None  # Será Usuario
```

---

### 5.4 Novos SQL Statements

Criar arquivos SQL para cada entidade, seguindo o padrão do `sql/usuario_sql.py`.

#### 5.4.1 Area SQL

**Arquivo:** `sql/area_sql.py`

```python
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
```

#### 5.4.2 Empresa SQL

**Arquivo:** `sql/empresa_sql.py`

```python
"""
SQL statements para gerenciamento de empresas.
"""

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS empresa (
    id_empresa INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cnpj TEXT UNIQUE NOT NULL,
    descricao TEXT,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

INSERIR = """
INSERT INTO empresa (nome, cnpj, descricao)
VALUES (?, ?, ?)
"""

ALTERAR = """
UPDATE empresa
SET nome = ?, cnpj = ?, descricao = ?
WHERE id_empresa = ?
"""

EXCLUIR = "DELETE FROM empresa WHERE id_empresa = ?"

OBTER_POR_ID = "SELECT * FROM empresa WHERE id_empresa = ?"

OBTER_TODAS = "SELECT * FROM empresa ORDER BY nome"

OBTER_POR_CNPJ = "SELECT * FROM empresa WHERE cnpj = ?"

OBTER_QUANTIDADE = "SELECT COUNT(*) as quantidade FROM empresa"

# Buscar empresas com filtros
BUSCAR = """
SELECT * FROM empresa
WHERE (? IS NULL OR nome LIKE '%' || ? || '%')
ORDER BY nome
LIMIT ? OFFSET ?
"""
```

#### 5.4.3 Vaga SQL

**Arquivo:** `sql/vaga_sql.py`

```python
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
    id_area, id_empresa, id_recrutador, titulo, descricao,
    numero_vagas, salario, requisitos, beneficios,
    carga_horaria, modalidade, cidade, uf
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
```

#### 5.4.4 Candidatura SQL

**Arquivo:** `sql/candidatura_sql.py`

```python
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

# Obter candidaturas com filtros
BUSCAR_POR_STATUS_E_VAGA = """
SELECT c.*,
       u.nome as candidato_nome, u.email as candidato_email
FROM candidatura c
LEFT JOIN usuario u ON c.id_candidato = u.id
WHERE c.id_vaga = ? AND c.status = ?
ORDER BY c.data_candidatura DESC
"""
```

#### 5.4.5 Endereco SQL

**Arquivo:** `sql/endereco_sql.py`

```python
"""
SQL statements para gerenciamento de endereços.
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
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

ALTERAR = """
UPDATE endereco
SET titulo = ?, logradouro = ?, numero = ?, complemento = ?,
    bairro = ?, cidade = ?, uf = ?, cep = ?
WHERE id_endereco = ?
"""

EXCLUIR = "DELETE FROM endereco WHERE id_endereco = ?"

OBTER_POR_ID = "SELECT * FROM endereco WHERE id_endereco = ?"

OBTER_POR_USUARIO = """
SELECT * FROM endereco
WHERE id_usuario = ?
ORDER BY titulo
"""

OBTER_TODOS = "SELECT * FROM endereco ORDER BY cidade, bairro"
```

---

### 5.5 Novos Repositórios

Criar repositórios seguindo o padrão do `repo/usuario_repo.py`.

#### 5.5.1 Area Repo

**Arquivo:** `repo/area_repo.py`

```python
from typing import Optional
from model.area_model import Area
from sql.area_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    """Cria a tabela de áreas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(area: Area) -> Optional[int]:
    """Insere uma nova área."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (area.nome, area.descricao))
        return cursor.lastrowid

def alterar(area: Area) -> bool:
    """Altera uma área existente."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (area.nome, area.descricao, area.id_area))
        return cursor.rowcount > 0

def excluir(id_area: int) -> bool:
    """Exclui uma área."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_area,))
        return cursor.rowcount > 0

def obter_por_id(id_area: int) -> Optional[Area]:
    """Obtém uma área por ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_area,))
        row = cursor.fetchone()
        if row:
            return Area(
                id_area=row["id_area"],
                nome=row["nome"],
                descricao=row["descricao"]
            )
        return None

def obter_todas() -> list[Area]:
    """Obtém todas as áreas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        rows = cursor.fetchall()
        return [
            Area(
                id_area=row["id_area"],
                nome=row["nome"],
                descricao=row["descricao"]
            )
            for row in rows
        ]

def obter_por_nome(nome: str) -> Optional[Area]:
    """Obtém uma área por nome."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_NOME, (nome,))
        row = cursor.fetchone()
        if row:
            return Area(
                id_area=row["id_area"],
                nome=row["nome"],
                descricao=row["descricao"]
            )
        return None

def obter_quantidade() -> int:
    """Obtém a quantidade total de áreas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def verificar_uso(id_area: int) -> int:
    """Verifica quantas vagas estão usando esta área."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(VERIFICAR_USO, (id_area,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0
```

#### 5.5.2 Empresa Repo

**Arquivo:** `repo/empresa_repo.py`

```python
from typing import Optional
from model.empresa_model import Empresa
from sql.empresa_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    """Cria a tabela de empresas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(empresa: Empresa) -> Optional[int]:
    """Insere uma nova empresa."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (empresa.nome, empresa.cnpj, empresa.descricao))
        return cursor.lastrowid

def alterar(empresa: Empresa) -> bool:
    """Altera uma empresa existente."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            empresa.nome,
            empresa.cnpj,
            empresa.descricao,
            empresa.id_empresa
        ))
        return cursor.rowcount > 0

def excluir(id_empresa: int) -> bool:
    """Exclui uma empresa."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_empresa,))
        return cursor.rowcount > 0

def obter_por_id(id_empresa: int) -> Optional[Empresa]:
    """Obtém uma empresa por ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_empresa,))
        row = cursor.fetchone()
        if row:
            return Empresa(
                id_empresa=row["id_empresa"],
                nome=row["nome"],
                cnpj=row["cnpj"],
                descricao=row["descricao"]
            )
        return None

def obter_todas() -> list[Empresa]:
    """Obtém todas as empresas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        rows = cursor.fetchall()
        return [
            Empresa(
                id_empresa=row["id_empresa"],
                nome=row["nome"],
                cnpj=row["cnpj"],
                descricao=row["descricao"]
            )
            for row in rows
        ]

def obter_por_cnpj(cnpj: str) -> Optional[Empresa]:
    """Obtém uma empresa por CNPJ."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_CNPJ, (cnpj,))
        row = cursor.fetchone()
        if row:
            return Empresa(
                id_empresa=row["id_empresa"],
                nome=row["nome"],
                cnpj=row["cnpj"],
                descricao=row["descricao"]
            )
        return None

def obter_quantidade() -> int:
    """Obtém a quantidade total de empresas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def buscar(termo: Optional[str] = None, limite: int = 50, offset: int = 0) -> list[Empresa]:
    """Busca empresas com filtros."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(BUSCAR, (termo, termo, limite, offset))
        rows = cursor.fetchall()
        return [
            Empresa(
                id_empresa=row["id_empresa"],
                nome=row["nome"],
                cnpj=row["cnpj"],
                descricao=row["descricao"]
            )
            for row in rows
        ]
```

#### 5.5.3 Vaga Repo

**Arquivo:** `repo/vaga_repo.py`

```python
from typing import Optional
from model.vaga_model import Vaga
from model.area_model import Area
from model.empresa_model import Empresa
from model.usuario_model import Usuario
from sql.vaga_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    """Cria a tabela de vagas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(vaga: Vaga) -> Optional[int]:
    """Insere uma nova vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            vaga.id_area,
            vaga.id_empresa,
            vaga.id_recrutador,
            vaga.titulo,
            vaga.descricao,
            vaga.numero_vagas,
            vaga.salario,
            vaga.requisitos,
            vaga.beneficios,
            vaga.carga_horaria,
            vaga.modalidade,
            vaga.cidade,
            vaga.uf
        ))
        return cursor.lastrowid

def alterar(vaga: Vaga) -> bool:
    """Altera uma vaga existente."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            vaga.id_area,
            vaga.titulo,
            vaga.descricao,
            vaga.numero_vagas,
            vaga.salario,
            vaga.requisitos,
            vaga.beneficios,
            vaga.carga_horaria,
            vaga.modalidade,
            vaga.cidade,
            vaga.uf,
            vaga.id_vaga
        ))
        return cursor.rowcount > 0

def alterar_status(id_vaga: int, status: str) -> bool:
    """Altera o status de uma vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR_STATUS, (status, id_vaga))
        return cursor.rowcount > 0

def excluir(id_vaga: int) -> bool:
    """Exclui uma vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_vaga,))
        return cursor.rowcount > 0

def _montar_vaga_completa(row) -> Vaga:
    """Monta objeto Vaga com relacionamentos."""
    vaga = Vaga(
        id_vaga=row["id_vaga"],
        id_area=row["id_area"],
        id_empresa=row["id_empresa"],
        id_recrutador=row["id_recrutador"],
        status_vaga=row["status_vaga"],
        descricao=row["descricao"],
        numero_vagas=row["numero_vagas"],
        salario=row["salario"],
        data_cadastro=row["data_cadastro"],
        titulo=row.get("titulo"),
        requisitos=row.get("requisitos"),
        beneficios=row.get("beneficios"),
        carga_horaria=row.get("carga_horaria"),
        modalidade=row.get("modalidade"),
        cidade=row.get("cidade"),
        uf=row.get("uf")
    )

    # Adicionar área se disponível
    if "area_nome" in row.keys():
        vaga.area = Area(
            id_area=row["id_area"],
            nome=row["area_nome"],
            descricao=row.get("area_descricao", "")
        )

    # Adicionar empresa se disponível
    if "empresa_nome" in row.keys():
        vaga.empresa = Empresa(
            id_empresa=row["id_empresa"],
            nome=row["empresa_nome"],
            cnpj=row.get("empresa_cnpj", ""),
            descricao=row.get("empresa_descricao", "")
        )

    return vaga

def obter_por_id(id_vaga: int) -> Optional[Vaga]:
    """Obtém uma vaga por ID com relacionamentos."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_vaga,))
        row = cursor.fetchone()
        if row:
            return _montar_vaga_completa(row)
        return None

def obter_todas() -> list[Vaga]:
    """Obtém todas as vagas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        rows = cursor.fetchall()
        return [_montar_vaga_completa(row) for row in rows]

def obter_por_empresa(id_empresa: int) -> list[Vaga]:
    """Obtém vagas de uma empresa específica."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_EMPRESA, (id_empresa,))
        rows = cursor.fetchall()
        return [_montar_vaga_completa(row) for row in rows]

def obter_por_recrutador(id_recrutador: int) -> list[Vaga]:
    """Obtém vagas de um recrutador específico."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_RECRUTADOR, (id_recrutador,))
        rows = cursor.fetchall()
        return [_montar_vaga_completa(row) for row in rows]

def buscar(
    id_area: Optional[int] = None,
    cidade: Optional[str] = None,
    uf: Optional[str] = None,
    modalidade: Optional[str] = None,
    salario_minimo: Optional[float] = None,
    limite: int = 50,
    offset: int = 0
) -> list[Vaga]:
    """Busca vagas com filtros."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(BUSCAR, (
            id_area, id_area,
            cidade, cidade,
            uf, uf,
            modalidade, modalidade,
            salario_minimo, salario_minimo,
            limite, offset
        ))
        rows = cursor.fetchall()
        return [_montar_vaga_completa(row) for row in rows]

def obter_vagas_abertas(limite: int = 50, offset: int = 0) -> list[Vaga]:
    """Obtém apenas vagas abertas (para visualização pública)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_VAGAS_ABERTAS, (limite, offset))
        rows = cursor.fetchall()
        return [_montar_vaga_completa(row) for row in rows]

def obter_quantidade() -> int:
    """Obtém a quantidade total de vagas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def obter_quantidade_por_status(status: str) -> int:
    """Obtém a quantidade de vagas por status."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_STATUS, (status,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0
```

#### 5.5.4 Candidatura Repo

**Arquivo:** `repo/candidatura_repo.py`

```python
from typing import Optional
from model.candidatura_model import Candidatura
from sql.candidatura_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    """Cria a tabela de candidaturas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(candidatura: Candidatura) -> Optional[int]:
    """Insere uma nova candidatura."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            candidatura.id_vaga,
            candidatura.id_candidato
        ))
        return cursor.lastrowid

def alterar_status(id_candidatura: int, status: str) -> bool:
    """Altera o status de uma candidatura."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR_STATUS, (status, id_candidatura))
        return cursor.rowcount > 0

def excluir(id_candidatura: int) -> bool:
    """Exclui uma candidatura (cancelar candidatura)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_candidatura,))
        return cursor.rowcount > 0

def obter_por_id(id_candidatura: int) -> Optional[Candidatura]:
    """Obtém uma candidatura por ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_candidatura,))
        row = cursor.fetchone()
        if row:
            return Candidatura(
                id_candidatura=row["id_candidatura"],
                id_vaga=row["id_vaga"],
                id_candidato=row["id_candidato"],
                data_candidatura=row["data_candidatura"],
                status=row["status"]
            )
        return None

def obter_por_vaga(id_vaga: int) -> list[Candidatura]:
    """Obtém todas as candidaturas de uma vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_VAGA, (id_vaga,))
        rows = cursor.fetchall()
        return [
            Candidatura(
                id_candidatura=row["id_candidatura"],
                id_vaga=row["id_vaga"],
                id_candidato=row["id_candidato"],
                data_candidatura=row["data_candidatura"],
                status=row["status"]
            )
            for row in rows
        ]

def obter_por_candidato(id_candidato: int) -> list[Candidatura]:
    """Obtém todas as candidaturas de um candidato."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_CANDIDATO, (id_candidato,))
        rows = cursor.fetchall()
        return [
            Candidatura(
                id_candidatura=row["id_candidatura"],
                id_vaga=row["id_vaga"],
                id_candidato=row["id_candidato"],
                data_candidatura=row["data_candidatura"],
                status=row["status"]
            )
            for row in rows
        ]

def verificar_candidatura_existente(id_vaga: int, id_candidato: int) -> bool:
    """Verifica se o candidato já se candidatou a essa vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(VERIFICAR_CANDIDATURA_EXISTENTE, (id_vaga, id_candidato))
        row = cursor.fetchone()
        return row is not None

def obter_quantidade_por_vaga(id_vaga: int) -> int:
    """Obtém quantidade de candidaturas de uma vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_VAGA, (id_vaga,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def obter_quantidade_por_candidato(id_candidato: int) -> int:
    """Obtém quantidade de candidaturas de um candidato."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_CANDIDATO, (id_candidato,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def buscar_por_status_e_vaga(id_vaga: int, status: str) -> list[Candidatura]:
    """Busca candidaturas por status e vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(BUSCAR_POR_STATUS_E_VAGA, (id_vaga, status))
        rows = cursor.fetchall()
        return [
            Candidatura(
                id_candidatura=row["id_candidatura"],
                id_vaga=row["id_vaga"],
                id_candidato=row["id_candidato"],
                data_candidatura=row["data_candidatura"],
                status=row["status"]
            )
            for row in rows
        ]
```

#### 5.5.5 Endereco Repo

**Arquivo:** `repo/endereco_repo.py`

```python
from typing import Optional
from model.endereco_model import Endereco
from sql.endereco_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    """Cria a tabela de endereços."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(endereco: Endereco) -> Optional[int]:
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

def alterar(endereco: Endereco) -> bool:
    """Altera um endereço existente."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
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
        return cursor.rowcount > 0

def excluir(id_endereco: int) -> bool:
    """Exclui um endereço."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_endereco,))
        return cursor.rowcount > 0

def obter_por_id(id_endereco: int) -> Optional[Endereco]:
    """Obtém um endereço por ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_endereco,))
        row = cursor.fetchone()
        if row:
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
        return None

def obter_por_usuario(id_usuario: int) -> list[Endereco]:
    """Obtém todos os endereços de um usuário."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_USUARIO, (id_usuario,))
        rows = cursor.fetchall()
        return [
            Endereco(
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
            for row in rows
        ]

def obter_todos() -> list[Endereco]:
    """Obtém todos os endereços."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [
            Endereco(
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
            for row in rows
        ]
```

---

### 5.6 Novos DTOs

Criar DTOs com validação usando Pydantic, seguindo o padrão do `dtos/usuario_dto.py`.

#### 5.6.1 Area DTO

**Arquivo:** `dtos/area_dto.py`

```python
from pydantic import BaseModel, field_validator
from dtos.validators import validar_nome_generico, validar_id_positivo

class CriarAreaDTO(BaseModel):
    """DTO para criação de área."""
    nome: str
    descricao: str

    _validar_nome = field_validator("nome")(validar_nome_generico(min_length=3, max_length=100))

class AlterarAreaDTO(BaseModel):
    """DTO para alteração de área."""
    id_area: int
    nome: str
    descricao: str

    _validar_id = field_validator("id_area")(validar_id_positivo())
    _validar_nome = field_validator("nome")(validar_nome_generico(min_length=3, max_length=100))
```

#### 5.6.2 Empresa DTO

**Arquivo:** `dtos/empresa_dto.py`

```python
from pydantic import BaseModel, field_validator
from dtos.validators import validar_cnpj, validar_nome_generico, validar_id_positivo

class CriarEmpresaDTO(BaseModel):
    """DTO para criação de empresa."""
    nome: str
    cnpj: str
    descricao: str

    _validar_nome = field_validator("nome")(validar_nome_generico(min_length=3, max_length=200))
    _validar_cnpj = field_validator("cnpj")(validar_cnpj())

class AlterarEmpresaDTO(BaseModel):
    """DTO para alteração de empresa."""
    id_empresa: int
    nome: str
    cnpj: str
    descricao: str

    _validar_id = field_validator("id_empresa")(validar_id_positivo())
    _validar_nome = field_validator("nome")(validar_nome_generico(min_length=3, max_length=200))
    _validar_cnpj = field_validator("cnpj")(validar_cnpj())
```

**Nota:** Adicionar validador de CNPJ em `dtos/validators.py`:

```python
def validar_cnpj():
    """Validador de CNPJ."""
    def validator(cls, v: str) -> str:
        import re
        # Remove caracteres não numéricos
        cnpj = re.sub(r'[^0-9]', '', v)

        if len(cnpj) != 14:
            raise ValueError('CNPJ deve ter 14 dígitos')

        # Validação básica (verificar se não são todos iguais)
        if cnpj == cnpj[0] * 14:
            raise ValueError('CNPJ inválido')

        # Aqui você pode adicionar validação completa de CNPJ se necessário
        return cnpj

    return validator
```

#### 5.6.3 Vaga DTO

**Arquivo:** `dtos/vaga_dto.py`

```python
from pydantic import BaseModel, field_validator
from typing import Optional
from dtos.validators import validar_id_positivo, validar_nome_generico

class CriarVagaDTO(BaseModel):
    """DTO para criação de vaga."""
    id_area: int
    id_empresa: int
    id_recrutador: int
    titulo: str
    descricao: str
    numero_vagas: int = 1
    salario: float = 0.0
    requisitos: Optional[str] = None
    beneficios: Optional[str] = None
    carga_horaria: Optional[int] = None
    modalidade: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None

    _validar_id_area = field_validator("id_area")(validar_id_positivo())
    _validar_id_empresa = field_validator("id_empresa")(validar_id_positivo())
    _validar_id_recrutador = field_validator("id_recrutador")(validar_id_positivo())
    _validar_titulo = field_validator("titulo")(validar_nome_generico(min_length=5, max_length=200))

    @field_validator("numero_vagas")
    @classmethod
    def validar_numero_vagas(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Número de vagas deve ser pelo menos 1")
        if v > 100:
            raise ValueError("Número de vagas não pode exceder 100")
        return v

    @field_validator("salario")
    @classmethod
    def validar_salario(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Salário não pode ser negativo")
        return v

    @field_validator("modalidade")
    @classmethod
    def validar_modalidade(cls, v: Optional[str]) -> Optional[str]:
        if v and v not in ["Presencial", "Remoto", "Híbrido"]:
            raise ValueError("Modalidade deve ser: Presencial, Remoto ou Híbrido")
        return v

class AlterarVagaDTO(BaseModel):
    """DTO para alteração de vaga."""
    id_vaga: int
    id_area: int
    titulo: str
    descricao: str
    numero_vagas: int
    salario: float
    requisitos: Optional[str]
    beneficios: Optional[str]
    carga_horaria: Optional[int]
    modalidade: Optional[str]
    cidade: Optional[str]
    uf: Optional[str]

    _validar_id_vaga = field_validator("id_vaga")(validar_id_positivo())
    _validar_id_area = field_validator("id_area")(validar_id_positivo())
    _validar_titulo = field_validator("titulo")(validar_nome_generico(min_length=5, max_length=200))

class BuscarVagasDTO(BaseModel):
    """DTO para busca de vagas com filtros."""
    id_area: Optional[int] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    modalidade: Optional[str] = None
    salario_minimo: Optional[float] = None
    limite: int = 50
    offset: int = 0
```

#### 5.6.4 Candidatura DTO

**Arquivo:** `dtos/candidatura_dto.py`

```python
from pydantic import BaseModel, field_validator
from dtos.validators import validar_id_positivo

class CriarCandidaturaDTO(BaseModel):
    """DTO para criação de candidatura."""
    id_vaga: int
    id_candidato: int

    _validar_id_vaga = field_validator("id_vaga")(validar_id_positivo())
    _validar_id_candidato = field_validator("id_candidato")(validar_id_positivo())

class AlterarStatusCandidaturaDTO(BaseModel):
    """DTO para alteração de status de candidatura."""
    id_candidatura: int
    status: str

    _validar_id = field_validator("id_candidatura")(validar_id_positivo())

    @field_validator("status")
    @classmethod
    def validar_status(cls, v: str) -> str:
        status_validos = ["pendente", "em_analise", "aprovado", "rejeitado", "cancelado"]
        if v not in status_validos:
            raise ValueError(f"Status deve ser um de: {', '.join(status_validos)}")
        return v
```

#### 5.6.5 Endereco DTO

**Arquivo:** `dtos/endereco_dto.py`

```python
from pydantic import BaseModel, field_validator
from dtos.validators import validar_id_positivo, validar_cep, validar_uf

class CriarEnderecoDTO(BaseModel):
    """DTO para criação de endereço."""
    id_usuario: int
    titulo: str
    logradouro: str
    numero: str
    complemento: str = ""
    bairro: str
    cidade: str
    uf: str
    cep: str

    _validar_id_usuario = field_validator("id_usuario")(validar_id_positivo())
    _validar_uf = field_validator("uf")(validar_uf())
    _validar_cep = field_validator("cep")(validar_cep())

class AlterarEnderecoDTO(BaseModel):
    """DTO para alteração de endereço."""
    id_endereco: int
    titulo: str
    logradouro: str
    numero: str
    complemento: str
    bairro: str
    cidade: str
    uf: str
    cep: str

    _validar_id = field_validator("id_endereco")(validar_id_positivo())
    _validar_uf = field_validator("uf")(validar_uf())
    _validar_cep = field_validator("cep")(validar_cep())
```

**Nota:** Adicionar validadores em `dtos/validators.py`:

```python
def validar_uf():
    """Validador de UF (estado)."""
    def validator(cls, v: str) -> str:
        ufs_validas = [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
            "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
            "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ]
        v = v.upper()
        if v not in ufs_validas:
            raise ValueError(f"UF inválida. Use uma de: {', '.join(ufs_validas)}")
        return v
    return validator

def validar_cep():
    """Validador de CEP."""
    def validator(cls, v: str) -> str:
        import re
        cep = re.sub(r'[^0-9]', '', v)
        if len(cep) != 8:
            raise ValueError("CEP deve ter 8 dígitos")
        return cep
    return validator
```

---

### 5.7 Novas Rotas

Criar rotas RESTful seguindo o padrão do projeto.

#### 5.7.1 Admin Areas Routes

**Arquivo:** `routes/admin_areas_routes.py`

```python
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from model.area_model import Area
from repo import area_repo
from dtos.area_dto import CriarAreaDTO, AlterarAreaDTO
from util.auth_decorator import exigir_login, exigir_perfil
from util.perfis import Perfil
from util.flash_messages import informar_sucesso, informar_erro
from util.template_util import criar_templates
from util.logger_config import logger
from util.exceptions import FormValidationError

router = APIRouter(prefix="/admin/areas")
templates = criar_templates("templates/admin/areas")

@router.get("/")
@exigir_login
@exigir_perfil(Perfil.ADMIN)
async def listar_areas(request: Request):
    """Lista todas as áreas."""
    areas = area_repo.obter_todas()
    return templates.TemplateResponse("listar.html", {
        "request": request,
        "areas": areas
    })

@router.get("/nova")
@exigir_login
@exigir_perfil(Perfil.ADMIN)
async def nova_area(request: Request):
    """Exibe formulário para nova área."""
    return templates.TemplateResponse("form.html", {
        "request": request,
        "area": None
    })

@router.post("/nova")
@exigir_login
@exigir_perfil(Perfil.ADMIN)
async def criar_area(
    request: Request,
    nome: str = Form(),
    descricao: str = Form()
):
    """Cria uma nova área."""
    dados_formulario = {"nome": nome, "descricao": descricao}

    try:
        # Validar com DTO
        dto = CriarAreaDTO(nome=nome, descricao=descricao)

        # Verificar se área já existe
        if area_repo.obter_por_nome(dto.nome):
            informar_erro(request, "Já existe uma área com este nome")
            return templates.TemplateResponse("form.html", {
                "request": request,
                "area": None,
                "dados": dados_formulario
            })

        # Criar área
        area = Area(id_area=0, nome=dto.nome, descricao=dto.descricao)
        area_id = area_repo.inserir(area)

        if area_id:
            logger.info(f"Área '{dto.nome}' criada com sucesso")
            informar_sucesso(request, "Área criada com sucesso!")
            return RedirectResponse("/admin/areas", status_code=status.HTTP_303_SEE_OTHER)
        else:
            informar_erro(request, "Erro ao criar área")
            return templates.TemplateResponse("form.html", {
                "request": request,
                "area": None,
                "dados": dados_formulario
            })

    except ValidationError as e:
        raise FormValidationError(
            validation_error=e,
            template_path="admin/areas/form.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome"
        )

@router.get("/{id_area}/editar")
@exigir_login
@exigir_perfil(Perfil.ADMIN)
async def editar_area(request: Request, id_area: int):
    """Exibe formulário para editar área."""
    area = area_repo.obter_por_id(id_area)
    if not area:
        informar_erro(request, "Área não encontrada")
        return RedirectResponse("/admin/areas", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("form.html", {
        "request": request,
        "area": area
    })

@router.post("/{id_area}/editar")
@exigir_login
@exigir_perfil(Perfil.ADMIN)
async def salvar_area(
    request: Request,
    id_area: int,
    nome: str = Form(),
    descricao: str = Form()
):
    """Salva alterações da área."""
    dados_formulario = {"nome": nome, "descricao": descricao}

    try:
        # Validar com DTO
        dto = AlterarAreaDTO(id_area=id_area, nome=nome, descricao=descricao)

        # Criar objeto Area
        area = Area(id_area=dto.id_area, nome=dto.nome, descricao=dto.descricao)

        # Alterar no banco
        if area_repo.alterar(area):
            logger.info(f"Área {id_area} alterada com sucesso")
            informar_sucesso(request, "Área alterada com sucesso!")
            return RedirectResponse("/admin/areas", status_code=status.HTTP_303_SEE_OTHER)
        else:
            informar_erro(request, "Erro ao alterar área")
            return templates.TemplateResponse("form.html", {
                "request": request,
                "area": area,
                "dados": dados_formulario
            })

    except ValidationError as e:
        raise FormValidationError(
            validation_error=e,
            template_path="admin/areas/form.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome"
        )

@router.post("/{id_area}/excluir")
@exigir_login
@exigir_perfil(Perfil.ADMIN)
async def excluir_area(request: Request, id_area: int):
    """Exclui uma área."""
    # Verificar se área está sendo usada
    if area_repo.verificar_uso(id_area) > 0:
        informar_erro(request, "Não é possível excluir área que possui vagas cadastradas")
        return RedirectResponse("/admin/areas", status_code=status.HTTP_303_SEE_OTHER)

    if area_repo.excluir(id_area):
        logger.info(f"Área {id_area} excluída")
        informar_sucesso(request, "Área excluída com sucesso!")
    else:
        informar_erro(request, "Erro ao excluir área")

    return RedirectResponse("/admin/areas", status_code=status.HTTP_303_SEE_OTHER)
```

#### 5.7.2 Vaga Routes

**Arquivo:** `routes/vaga_routes.py`

Este arquivo é compartilhado por recrutadores (criar/editar vagas) e estudantes/anônimos (visualizar vagas).

```python
from fastapi import APIRouter, Request, Query
from typing import Optional

from repo import vaga_repo
from util.template_util import criar_templates

router = APIRouter(prefix="/vagas")
templates = criar_templates("templates/vagas")

@router.get("/")
async def listar_vagas(
    request: Request,
    area: Optional[int] = Query(None),
    cidade: Optional[str] = Query(None),
    uf: Optional[str] = Query(None),
    modalidade: Optional[str] = Query(None),
    salario_min: Optional[float] = Query(None),
    pagina: int = Query(1, ge=1)
):
    """Lista vagas abertas com filtros (acesso público)."""
    limite = 20
    offset = (pagina - 1) * limite

    # Buscar vagas com filtros
    vagas = vaga_repo.buscar(
        id_area=area,
        cidade=cidade,
        uf=uf,
        modalidade=modalidade,
        salario_minimo=salario_min,
        limite=limite,
        offset=offset
    )

    return templates.TemplateResponse("listar.html", {
        "request": request,
        "vagas": vagas,
        "filtros": {
            "area": area,
            "cidade": cidade,
            "uf": uf,
            "modalidade": modalidade,
            "salario_min": salario_min
        },
        "pagina": pagina
    })

@router.get("/{id_vaga}")
async def detalhes_vaga(request: Request, id_vaga: int):
    """Exibe detalhes de uma vaga específica."""
    vaga = vaga_repo.obter_por_id(id_vaga)
    if not vaga:
        # Retornar 404 ou redirecionar
        return templates.TemplateResponse("404.html", {
            "request": request,
            "mensagem": "Vaga não encontrada"
        }, status_code=404)

    return templates.TemplateResponse("detalhes.html", {
        "request": request,
        "vaga": vaga
    })
```

#### 5.7.3 Recrutador Routes

**Arquivo:** `routes/recrutador_routes.py`

```python
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from model.vaga_model import Vaga
from repo import vaga_repo, empresa_repo, area_repo
from dtos.vaga_dto import CriarVagaDTO, AlterarVagaDTO
from util.auth_decorator import exigir_login, exigir_perfil
from util.perfis import Perfil
from util.flash_messages import informar_sucesso, informar_erro
from util.template_util import criar_templates
from util.logger_config import logger
from util.exceptions import FormValidationError

router = APIRouter(prefix="/recrutador")
templates = criar_templates("templates/recrutador")

@router.get("/dashboard")
@exigir_login
@exigir_perfil(Perfil.RECRUTADOR)
async def dashboard(request: Request):
    """Dashboard do recrutador."""
    usuario = request.session.get("usuario_logado")
    id_recrutador = usuario["id"]

    # Buscar vagas do recrutador
    vagas = vaga_repo.obter_por_recrutador(id_recrutador)

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "vagas": vagas
    })

@router.get("/vagas/nova")
@exigir_login
@exigir_perfil(Perfil.RECRUTADOR)
async def nova_vaga(request: Request):
    """Formulário para criar nova vaga."""
    areas = area_repo.obter_todas()
    empresas = empresa_repo.obter_todas()

    return templates.TemplateResponse("vaga_form.html", {
        "request": request,
        "vaga": None,
        "areas": areas,
        "empresas": empresas
    })

@router.post("/vagas/nova")
@exigir_login
@exigir_perfil(Perfil.RECRUTADOR)
async def criar_vaga(
    request: Request,
    id_area: int = Form(),
    id_empresa: int = Form(),
    titulo: str = Form(),
    descricao: str = Form(),
    numero_vagas: int = Form(1),
    salario: float = Form(0.0),
    requisitos: str = Form(""),
    beneficios: str = Form(""),
    carga_horaria: int = Form(None),
    modalidade: str = Form(None),
    cidade: str = Form(""),
    uf: str = Form("")
):
    """Cria nova vaga."""
    usuario = request.session.get("usuario_logado")
    id_recrutador = usuario["id"]

    dados_formulario = {
        "id_area": id_area,
        "id_empresa": id_empresa,
        "titulo": titulo,
        "descricao": descricao,
        "numero_vagas": numero_vagas,
        "salario": salario,
        "requisitos": requisitos,
        "beneficios": beneficios,
        "carga_horaria": carga_horaria,
        "modalidade": modalidade,
        "cidade": cidade,
        "uf": uf
    }

    try:
        # Validar com DTO
        dto = CriarVagaDTO(
            id_area=id_area,
            id_empresa=id_empresa,
            id_recrutador=id_recrutador,
            titulo=titulo,
            descricao=descricao,
            numero_vagas=numero_vagas,
            salario=salario,
            requisitos=requisitos or None,
            beneficios=beneficios or None,
            carga_horaria=carga_horaria,
            modalidade=modalidade or None,
            cidade=cidade or None,
            uf=uf or None
        )

        # Criar vaga
        vaga = Vaga(
            id_vaga=0,
            id_area=dto.id_area,
            id_empresa=dto.id_empresa,
            id_recrutador=dto.id_recrutador,
            status_vaga="aberta",
            descricao=dto.descricao,
            numero_vagas=dto.numero_vagas,
            salario=dto.salario,
            data_cadastro="",
            titulo=dto.titulo,
            requisitos=dto.requisitos,
            beneficios=dto.beneficios,
            carga_horaria=dto.carga_horaria,
            modalidade=dto.modalidade,
            cidade=dto.cidade,
            uf=dto.uf
        )

        vaga_id = vaga_repo.inserir(vaga)

        if vaga_id:
            logger.info(f"Vaga '{dto.titulo}' criada pelo recrutador {id_recrutador}")
            informar_sucesso(request, "Vaga criada com sucesso!")
            return RedirectResponse("/recrutador/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        else:
            informar_erro(request, "Erro ao criar vaga")
            areas = area_repo.obter_todas()
            empresas = empresa_repo.obter_todas()
            return templates.TemplateResponse("vaga_form.html", {
                "request": request,
                "vaga": None,
                "dados": dados_formulario,
                "areas": areas,
                "empresas": empresas
            })

    except ValidationError as e:
        raise FormValidationError(
            validation_error=e,
            template_path="recrutador/vaga_form.html",
            dados_formulario=dados_formulario,
            campo_padrao="titulo"
        )

# Adicionar rotas para editar, excluir, arquivar vagas
# Adicionar rotas para visualizar candidatos de uma vaga
# ... (seguir padrão similar)
```

---

### 5.8 Sistema de Mensagens

Sistema para troca de mensagens entre usuários (RF43, RF50).

#### 5.8.1 Mensagem Model

**Arquivo:** `model/mensagem_model.py`

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Mensagem:
    """
    Model de mensagem entre usuários.

    Attributes:
        id_mensagem: Identificador único
        id_remetente: FK para Usuario (quem enviou)
        id_destinatario: FK para Usuario (quem recebe)
        assunto: Assunto da mensagem
        conteudo: Corpo da mensagem
        lida: Se a mensagem foi lida
        data_envio: Data/hora de envio

        # Relacionamentos
        remetente: Objeto Usuario (opcional)
        destinatario: Objeto Usuario (opcional)
    """
    id_mensagem: int
    id_remetente: int
    id_destinatario: int
    assunto: str
    conteudo: str
    lida: bool
    data_envio: str

    # Relacionamentos
    remetente: Optional[object] = None
    destinatario: Optional[object] = None
```

#### 5.8.2 Mensagem SQL

**Arquivo:** `sql/mensagem_sql.py`

```python
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
```

#### 5.8.3 Mensagem Repo

**Arquivo:** `repo/mensagem_repo.py`

```python
from typing import Optional
from model.mensagem_model import Mensagem
from sql.mensagem_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(mensagem: Mensagem) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            mensagem.id_remetente,
            mensagem.id_destinatario,
            mensagem.assunto,
            mensagem.conteudo
        ))
        return cursor.lastrowid

def marcar_como_lida(id_mensagem: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(MARCAR_COMO_LIDA, (id_mensagem,))
        return cursor.rowcount > 0

def obter_recebidas(id_destinatario: int) -> list[Mensagem]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_RECEBIDAS, (id_destinatario,))
        rows = cursor.fetchall()
        return [
            Mensagem(
                id_mensagem=row["id_mensagem"],
                id_remetente=row["id_remetente"],
                id_destinatario=row["id_destinatario"],
                assunto=row["assunto"],
                conteudo=row["conteudo"],
                lida=bool(row["lida"]),
                data_envio=row["data_envio"]
            )
            for row in rows
        ]

def contar_nao_lidas(id_destinatario: int) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONTAR_NAO_LIDAS, (id_destinatario,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0
```

---

### 5.9 Sistema de Notificações

Sistema para notificar usuários sobre eventos (RF49, RF56).

#### 5.9.1 Notificacao Model

**Arquivo:** `model/notificacao_model.py`

```python
from dataclasses import dataclass

@dataclass
class Notificacao:
    """
    Model de notificação para usuários.

    Attributes:
        id_notificacao: Identificador único
        id_usuario: FK para Usuario
        tipo: Tipo da notificação (nova_vaga, candidatura_atualizada, mensagem_recebida, etc.)
        titulo: Título da notificação
        mensagem: Mensagem da notificação
        lida: Se foi lida
        data_criacao: Data/hora de criação
        link: Link relacionado (opcional)
    """
    id_notificacao: int
    id_usuario: int
    tipo: str
    titulo: str
    mensagem: str
    lida: bool
    data_criacao: str
    link: str = ""
```

#### 5.9.2 Notificacao SQL

**Arquivo:** `sql/notificacao_sql.py`

```python
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
```

#### 5.9.3 Notificacao Repo

**Arquivo:** `repo/notificacao_repo.py`

```python
from typing import Optional
from model.notificacao_model import Notificacao
from sql.notificacao_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(notificacao: Notificacao) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            notificacao.id_usuario,
            notificacao.tipo,
            notificacao.titulo,
            notificacao.mensagem,
            notificacao.link
        ))
        return cursor.lastrowid

def criar_notificacao(id_usuario: int, tipo: str, titulo: str, mensagem: str, link: str = "") -> Optional[int]:
    """Helper para criar notificação facilmente."""
    notificacao = Notificacao(
        id_notificacao=0,
        id_usuario=id_usuario,
        tipo=tipo,
        titulo=titulo,
        mensagem=mensagem,
        lida=False,
        data_criacao="",
        link=link
    )
    return inserir(notificacao)

def obter_nao_lidas(id_usuario: int) -> list[Notificacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_NAO_LIDAS, (id_usuario,))
        rows = cursor.fetchall()
        return [
            Notificacao(
                id_notificacao=row["id_notificacao"],
                id_usuario=row["id_usuario"],
                tipo=row["tipo"],
                titulo=row["titulo"],
                mensagem=row["mensagem"],
                lida=bool(row["lida"]),
                data_criacao=row["data_criacao"],
                link=row.get("link", "")
            )
            for row in rows
        ]

def contar_nao_lidas(id_usuario: int) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CONTAR_NAO_LIDAS, (id_usuario,))
        row = cursor.fetchone()
        return row["quantidade"] if row else 0

def marcar_como_lida(id_notificacao: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(MARCAR_COMO_LIDA, (id_notificacao,))
        return cursor.rowcount > 0
```

---

### 5.10 Sistema de Avaliações

Sistema para estudantes avaliarem empresas (RF52, RF36).

#### 5.10.1 Avaliacao Model

**Arquivo:** `model/avaliacao_model.py`

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Avaliacao:
    """
    Model de avaliação de empresa por estudante.

    Attributes:
        id_avaliacao: Identificador único
        id_empresa: FK para Empresa
        id_estudante: FK para Usuario
        nota: Nota de 1 a 5
        comentario: Comentário opcional
        data_avaliacao: Data da avaliação

        # Relacionamentos
        empresa: Objeto Empresa (opcional)
        estudante: Objeto Usuario (opcional)
    """
    id_avaliacao: int
    id_empresa: int
    id_estudante: int
    nota: int
    comentario: str
    data_avaliacao: str

    empresa: Optional[object] = None
    estudante: Optional[object] = None
```

#### 5.10.2 Avaliacao SQL

**Arquivo:** `sql/avaliacao_sql.py`

```python
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS avaliacao (
    id_avaliacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_empresa INTEGER NOT NULL,
    id_estudante INTEGER NOT NULL,
    nota INTEGER NOT NULL CHECK(nota >= 1 AND nota <= 5),
    comentario TEXT,
    data_avaliacao DATETIME DEFAULT CURRENT_TIMESTAMP,
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
```

#### 5.10.3 Avaliacao Repo

**Arquivo:** `repo/avaliacao_repo.py`

```python
from typing import Optional, Tuple
from model.avaliacao_model import Avaliacao
from sql.avaliacao_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(avaliacao: Avaliacao) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            avaliacao.id_empresa,
            avaliacao.id_estudante,
            avaliacao.nota,
            avaliacao.comentario
        ))
        return cursor.lastrowid

def obter_por_empresa(id_empresa: int) -> list[Avaliacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_EMPRESA, (id_empresa,))
        rows = cursor.fetchall()
        return [
            Avaliacao(
                id_avaliacao=row["id_avaliacao"],
                id_empresa=row["id_empresa"],
                id_estudante=row["id_estudante"],
                nota=row["nota"],
                comentario=row["comentario"],
                data_avaliacao=row["data_avaliacao"]
            )
            for row in rows
        ]

def obter_media_empresa(id_empresa: int) -> Tuple[float, int]:
    """Retorna (média, total de avaliações)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_MEDIA_EMPRESA, (id_empresa,))
        row = cursor.fetchone()
        if row and row["total"] > 0:
            return (round(row["media"], 1), row["total"])
        return (0.0, 0)

def verificar_avaliacao_existente(id_empresa: int, id_estudante: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(VERIFICAR_AVALIACAO_EXISTENTE, (id_empresa, id_estudante))
        return cursor.fetchone() is not None
```

---

## CONCLUSÃO

Este documento fornece um plano completo de implementação do backend do Estagiou.

### Resumo dos Componentes Criados/Modificados:

**Arquivos a Modificar:**
- `util/perfis.py` - Atualizar perfis
- `model/usuario_model.py` - Adicionar novos campos
- `sql/usuario_sql.py` - Atualizar SQL
- `repo/usuario_repo.py` - Atualizar funções

**Arquivos a Criar (30 novos arquivos):**

**SQL (6 arquivos):**
- `sql/area_sql.py`
- `sql/empresa_sql.py`
- `sql/vaga_sql.py`
- `sql/candidatura_sql.py`
- `sql/endereco_sql.py`
- `sql/mensagem_sql.py`
- `sql/notificacao_sql.py`
- `sql/avaliacao_sql.py`

**Repositórios (8 arquivos):**
- `repo/area_repo.py`
- `repo/empresa_repo.py`
- `repo/vaga_repo.py`
- `repo/candidatura_repo.py`
- `repo/endereco_repo.py`
- `repo/mensagem_repo.py`
- `repo/notificacao_repo.py`
- `repo/avaliacao_repo.py`

**DTOs (5 arquivos):**
- `dtos/area_dto.py`
- `dtos/empresa_dto.py`
- `dtos/vaga_dto.py`
- `dtos/candidatura_dto.py`
- `dtos/endereco_dto.py`

**Models (3 arquivos - ajustes):**
- `model/vaga_model.py` (ajustar)
- `model/empresa_model.py` (ajustar)
- `model/candidatura_model.py` (ajustar)
- `model/mensagem_model.py` (criar)
- `model/notificacao_model.py` (criar)
- `model/avaliacao_model.py` (criar)

**Rotas (4 arquivos principais):**
- `routes/admin_areas_routes.py`
- `routes/vaga_routes.py`
- `routes/recrutador_routes.py`
- `routes/estudante_routes.py`

### Próximos Passos:

1. **Implementar os arquivos na ordem sugerida** (Fase 1, 2, 3, 4)
2. **Atualizar main.py** para criar as novas tabelas no startup
3. **Criar templates** (não coberto neste documento - apenas backend)
4. **Testar cada componente** individualmente
5. **Integrar** os componentes
6. **Implementar testes automatizados**

### Estimativa de Linhas de Código:

- SQL: ~800 linhas
- Repositórios: ~1200 linhas
- DTOs: ~400 linhas
- Models: ~200 linhas (ajustes + novos)
- Rotas: ~1000 linhas
- **Total Backend: ~3600 linhas**

Este documento tem aproximadamente **3900 linhas**, dentro do limite solicitado de 4000 linhas.

---

**FIM DO PLANO DE IMPLEMENTAÇÃO DO BACKEND - ESTAGIOU**
