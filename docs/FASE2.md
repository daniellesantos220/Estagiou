# FASE 2 - Plano de Implementação: Rotas Administrativas do Estagiou

**Versão:** 2.0
**Data:** 2025-10-22
**Autor:** Análise baseada em Estagiou.pdf e padrões DefaultWebApp

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Padrões do Projeto Original](#padrões-do-projeto-original)
3. [Seção 1: Listagem de Áreas](#seção-1-listagem-de-áreas) - GET `/admin/areas/listar`
4. [Seção 2: Cadastro de Área](#seção-2-cadastro-de-área) - GET/POST `/admin/areas/cadastrar`
5. [Seção 3: Edição de Área](#seção-3-edição-de-área) - GET/POST `/admin/areas/editar/{id}`
6. [Seção 4: Exclusão de Área](#seção-4-exclusão-de-área) - POST `/admin/areas/excluir/{id}`
7. [Seção 5: Listagem de Vagas para Moderação](#seção-5-listagem-de-vagas-para-moderação) - GET `/admin/vagas/listar`
8. [Seção 6: Aprovação de Vaga](#seção-6-aprovação-de-vaga) - POST `/admin/vagas/aprovar/{id}`
9. [Seção 7: Reprovação de Vaga](#seção-7-reprovação-de-vaga) - POST `/admin/vagas/reprovar/{id}`
10. [Seção 8: Arquivamento de Vaga](#seção-8-arquivamento-de-vaga) - POST `/admin/vagas/arquivar/{id}`
11. [Seção 9: Exclusão de Vaga](#seção-9-exclusão-de-vaga) - POST `/admin/vagas/excluir/{id}`
12. [Integração com main.py](#integração-com-mainpy)
13. [Checklist de Implementação](#checklist-de-implementação)

---

## Visão Geral

Este documento define a implementação completa das rotas administrativas necessárias para atender aos **Casos de Uso do Administrador** conforme especificado em `Estagiou.pdf` (página 29).

### Casos de Uso

- **UC-ADM-01:** Gerenciar Usuários ✅ (Já implementado)
- **UC-ADM-02:** Gerenciar Áreas 🔨 (Seções 1-4)
- **UC-ADM-03:** Moderar Vagas 🔨 (Seções 5-9)
- **UC-ADM-04:** Configurar Plataforma ✅ (Já implementado)

### Requisitos Funcionais

| Requisito | Descrição | Seções |
|-----------|-----------|--------|
| RF-22 | Administrador pode criar, editar e excluir áreas | 1, 2, 3, 4 |
| RF-23 | Administrador pode aprovar/reprovar vagas | 6, 7 |
| RF-24 | Administrador pode arquivar/excluir vagas | 8, 9 |

---

## Padrões do Projeto Original

Todas as implementações devem seguir **rigorosamente** os padrões estabelecidos pelo projeto original DefaultWebApp.

### Estrutura de Imports (routes)

```python
from typing import Optional
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from dtos.[entidade]_dto import Criar[Entidade]DTO, Alterar[Entidade]DTO
from model.[entidade]_model import [Entidade]
from repo import [entidade]_repo
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.logger_config import logger
from util.perfis import Perfil
from util.exceptions import FormValidationError
```

### Inicialização do Router

```python
router = APIRouter(prefix="/admin/[entidades]")
templates = criar_templates("templates/admin/[entidades]")
```

### Decorador de Autenticação

```python
@router.get("/rota")
@requer_autenticacao([Perfil.ADMIN.value])
async def funcao(request: Request, usuario_logado: Optional[dict] = None):
    # Implementação
```

### Validação com DTOs

```python
try:
    dto = Criar[Entidade]DTO(campo1=valor1, campo2=valor2)
    # Processamento
except ValidationError as e:
    dados_formulario = {"campo1": valor1, "campo2": valor2}
    raise FormValidationError(
        validation_error=e,
        template_path="admin/[entidade]/formulario.html",
        dados_formulario=dados_formulario,
        campo_padrao="campo1",
    )
```

### Flash Messages e Redirecionamento

```python
informar_sucesso(request, "Operação realizada com sucesso!")
informar_erro(request, "Erro ao realizar operação")
return RedirectResponse("/admin/rota", status_code=status.HTTP_303_SEE_OTHER)
```

### Estrutura de Templates

```jinja2
{% extends "base_privada.html" %}
{% from "macros/form_fields.html" import field with context %}

{% block titulo %}Título da Página{% endblock %}

{% block content %}
<!-- Conteúdo -->
{% endblock %}

{% block scripts %}
<!-- Scripts específicos -->
{% endblock %}
```

### DTOs com Pydantic

```python
from pydantic import BaseModel, field_validator
from dtos.validators import validar_nome_generico, validar_id_positivo

class Criar[Entidade]DTO(BaseModel):
    """DTO para criação de [entidade]."""
    campo: str
    _validar_campo = field_validator("campo")(validar_nome_generico(min_length=3, max_length=100))

class Alterar[Entidade]DTO(BaseModel):
    """DTO para alteração de [entidade]."""
    id_[entidade]: int
    campo: str
    _validar_id = field_validator("id_[entidade]")(validar_id_positivo())
    _validar_campo = field_validator("campo")(validar_nome_generico(min_length=3, max_length=100))
```

---

## Seção 1: Listagem de Áreas

**Rota:** GET `/admin/areas/listar`
**Arquivo:** `routes/admin_areas_routes.py`
**Requisito:** RF-22 (visualização)

Esta rota lista todas as áreas cadastradas no sistema.

---

### 1.1 Rota GET

**Código:**

```python
@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as áreas cadastradas no sistema"""
    areas = area_repo.obter_todas()
    return templates.TemplateResponse(
        "admin/areas/listar.html",
        {"request": request, "areas": areas}
    )
```

---

### 1.2 Template

**Arquivo:** `templates/admin/areas/listar.html`

**Código:**

```jinja2
{% extends "base_privada.html" %}

{% block titulo %}Gerenciar Áreas{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="bi bi-grid-3x3-gap"></i> Gerenciar Áreas</h2>
            <a href="/admin/areas/cadastrar" class="btn btn-primary">
                <i class="bi bi-plus-circle"></i> Nova Área
            </a>
        </div>

        <div class="card shadow-sm">
            <div class="card-body">
                {% if areas %}
                <div class="table-responsive">
                    <table class="table table-hover align-middle">
                        <thead class="table-light">
                            <tr>
                                <th>ID</th>
                                <th>Nome</th>
                                <th>Descrição</th>
                                <th class="text-center">Vagas Vinculadas</th>
                                <th class="text-center">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for area in areas %}
                            <tr>
                                <td>{{ area.id_area }}</td>
                                <td>{{ area.nome }}</td>
                                <td>{{ area.descricao[:80] }}{% if area.descricao|length > 80 %}...{% endif %}</td>
                                <td class="text-center">
                                    <span class="badge bg-info">
                                        {{ area_repo.verificar_uso(area.id_area) }}
                                    </span>
                                </td>
                                <td class="text-center">
                                    <div class="btn-group btn-group-sm" role="group">
                                        <a href="/admin/areas/editar/{{ area.id_area }}"
                                            class="btn btn-outline-primary" title="Editar">
                                            <i class="bi bi-pencil"></i>
                                        </a>
                                        <button type="button" class="btn btn-outline-danger" title="Excluir"
                                            onclick="excluirArea({{ area.id_area }}, '{{ area.nome|replace("'", "\\'") }}')">
                                            <i class="bi bi-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% else %}
                <div class="alert alert-info text-center mb-0">
                    <i class="bi bi-info-circle"></i> Nenhuma área cadastrada.
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>

{% include "components/modal_confirmacao.html" %}
{% endblock %}

{% block scripts %}
<script>
    function excluirArea(areaId, areaNome) {
        const detalhes = `
        <div class="card bg-light">
            <div class="card-body">
                <table class="table table-sm table-borderless mb-0">
                    <tr>
                        <th width="30%">ID:</th>
                        <td>${areaId}</td>
                    </tr>
                    <tr>
                        <th>Nome:</th>
                        <td>${areaNome}</td>
                    </tr>
                </table>
            </div>
        </div>
        `;

        abrirModalConfirmacao({
            url: `/admin/areas/excluir/${areaId}`,
            mensagem: 'Tem certeza que deseja excluir esta área?',
            detalhes: detalhes
        });
    }
</script>
{% endblock %}
```

---

## Seção 2: Cadastro de Área

**Rota:** GET/POST `/admin/areas/cadastrar`
**Arquivo:** `routes/admin_areas_routes.py`
**Requisito:** RF-22 (criação)

Esta rota permite cadastrar novas áreas no sistema.

---

### 2.1 DTO

**Arquivo:** `dtos/area_dto.py` ✅ (já existe)

**Código:**

```python
from pydantic import BaseModel, field_validator
from dtos.validators import validar_nome_generico

class CriarAreaDTO(BaseModel):
    """DTO para criação de área."""
    nome: str
    descricao: str

    _validar_nome = field_validator("nome")(validar_nome_generico(min_length=3, max_length=100))
```

**Validações:**
- `nome`: Obrigatório, entre 3 e 100 caracteres
- `descricao`: Obrigatório (pode ser vazio)

---

### 2.2 Rota GET

**Código:**

```python
@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de área"""
    return templates.TemplateResponse(
        "admin/areas/cadastro.html",
        {"request": request}
    )
```

---

### 2.3 Rota POST

**Código:**

```python
@router.post("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(""),
    usuario_logado: Optional[dict] = None
):
    """Cadastra uma nova área"""
    assert usuario_logado is not None

    dados_formulario: dict = {"nome": nome, "descricao": descricao}

    try:
        # Validar com DTO
        dto = CriarAreaDTO(nome=nome, descricao=descricao)

        # Verificar se área com mesmo nome já existe
        area_existente = area_repo.obter_por_nome(dto.nome)
        if area_existente:
            informar_erro(request, "Já existe uma área cadastrada com este nome")
            return templates.TemplateResponse(
                "admin/areas/cadastro.html",
                {"request": request, "dados": dados_formulario}
            )

        # Criar área
        area = Area(id_area=0, nome=dto.nome, descricao=dto.descricao)
        area_repo.inserir(area)

        logger.info(f"Área '{dto.nome}' cadastrada por admin {usuario_logado['id']}")
        informar_sucesso(request, "Área cadastrada com sucesso!")

        return RedirectResponse("/admin/areas/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        raise FormValidationError(
            validation_error=e,
            template_path="admin/areas/cadastro.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )
```

**Validações:**
- DTO valida formato dos campos
- Verifica duplicação de nome
- Log de auditoria

---

### 2.4 Template

**Arquivo:** `templates/admin/areas/cadastro.html`

**Código:**

```jinja2
{% extends "base_privada.html" %}
{% from "macros/form_fields.html" import field with context %}

{% block titulo %}Cadastrar Área{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="d-flex align-items-center mb-4">
            <h2 class="mb-0"><i class="bi bi-grid-3x3-gap"></i> Cadastrar Nova Área</h2>
        </div>

        <div class="card shadow-sm">
            <form method="POST" action="/admin/areas/cadastrar">
                <div class="card-body p-4">
                    <div class="row">
                        <div class="col-12">
                            {% include "components/alert_erro_geral.html" %}
                        </div>

                        <div class="col-12 mb-3">
                            {{ field(name='nome', label='Nome da Área', type='text', required=true,
                                     placeholder='Ex: Tecnologia da Informação') }}
                        </div>

                        <div class="col-12 mb-3">
                            {{ field(name='descricao', label='Descrição', type='textarea', required=false,
                                     rows=4, placeholder='Descrição detalhada da área de atuação...') }}
                        </div>
                    </div>
                </div>
                <div class="card-footer p-4">
                    <div class="d-flex gap-3">
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-check-circle"></i> Cadastrar
                        </button>
                        <a href="/admin/areas/listar" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancelar
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Seção 3: Edição de Área

**Rota:** GET/POST `/admin/areas/editar/{id}`
**Arquivo:** `routes/admin_areas_routes.py`
**Requisito:** RF-22 (edição)

Esta rota permite editar áreas existentes.

---

### 3.1 DTO

**Arquivo:** `dtos/area_dto.py` ✅ (já existe)

**Código:**

```python
class AlterarAreaDTO(BaseModel):
    """DTO para alteração de área."""
    id_area: int
    nome: str
    descricao: str

    _validar_id = field_validator("id_area")(validar_id_positivo())
    _validar_nome = field_validator("nome")(validar_nome_generico(min_length=3, max_length=100))
```

**Validações:**
- `id_area`: Deve ser positivo
- `nome`: Entre 3 e 100 caracteres
- `descricao`: Obrigatório (pode ser vazio)

---

### 3.2 Rota GET

**Código:**

```python
@router.get("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_editar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exibe formulário de alteração de área"""
    area = area_repo.obter_por_id(id)

    if not area:
        informar_erro(request, "Área não encontrada")
        return RedirectResponse("/admin/areas/listar", status_code=status.HTTP_303_SEE_OTHER)

    dados_area = {
        "id_area": area.id_area,
        "nome": area.nome,
        "descricao": area.descricao
    }

    return templates.TemplateResponse(
        "admin/areas/editar.html",
        {"request": request, "area": area, "dados": dados_area}
    )
```

---

### 3.3 Rota POST

**Código:**

```python
@router.post("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_editar(
    request: Request,
    id: int,
    nome: str = Form(...),
    descricao: str = Form(""),
    usuario_logado: Optional[dict] = None
):
    """Altera dados de uma área"""
    assert usuario_logado is not None

    area_atual = area_repo.obter_por_id(id)
    if not area_atual:
        informar_erro(request, "Área não encontrada")
        return RedirectResponse("/admin/areas/listar", status_code=status.HTTP_303_SEE_OTHER)

    dados_formulario: dict = {"id_area": id, "nome": nome, "descricao": descricao}

    try:
        # Validar com DTO
        dto = AlterarAreaDTO(id_area=id, nome=nome, descricao=descricao)

        # Verificar se nome já existe em outra área
        area_nome = area_repo.obter_por_nome(dto.nome)
        if area_nome and area_nome.id_area != id:
            informar_erro(request, "Já existe outra área cadastrada com este nome")
            return templates.TemplateResponse(
                "admin/areas/editar.html",
                {"request": request, "area": area_atual, "dados": dados_formulario}
            )

        # Atualizar área
        area_atualizada = Area(id_area=id, nome=dto.nome, descricao=dto.descricao)
        area_repo.alterar(area_atualizada)

        logger.info(f"Área {id} ('{dto.nome}') alterada por admin {usuario_logado['id']}")
        informar_sucesso(request, "Área alterada com sucesso!")

        return RedirectResponse("/admin/areas/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["area"] = area_repo.obter_por_id(id)
        raise FormValidationError(
            validation_error=e,
            template_path="admin/areas/editar.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )
```

**Validações:**
- Verifica se área existe
- Valida com DTO
- Verifica duplicação de nome em outra área
- Log de auditoria

---

### 3.4 Template

**Arquivo:** `templates/admin/areas/editar.html`

**Código:**

```jinja2
{% extends "base_privada.html" %}
{% from "macros/form_fields.html" import field with context %}

{% block titulo %}Editar Área{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="d-flex align-items-center mb-4">
            <h2 class="mb-0"><i class="bi bi-pencil"></i> Editar Área</h2>
        </div>

        <div class="card shadow-sm">
            <form method="POST" action="/admin/areas/editar/{{ area.id_area }}">
                <div class="card-body p-4">
                    <div class="row">
                        <div class="col-12">
                            {% include "components/alert_erro_geral.html" %}
                        </div>

                        <div class="col-12 mb-3">
                            <label class="form-label fw-bold">ID da Área</label>
                            <input type="text" class="form-control" value="{{ area.id_area }}" disabled>
                        </div>

                        <div class="col-12 mb-3">
                            {{ field(name='nome', label='Nome da Área', type='text', required=true) }}
                        </div>

                        <div class="col-12 mb-3">
                            {{ field(name='descricao', label='Descrição', type='textarea', required=false, rows=4) }}
                        </div>
                    </div>
                </div>
                <div class="card-footer p-4">
                    <div class="d-flex gap-3">
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-check-circle"></i> Salvar Alterações
                        </button>
                        <a href="/admin/areas/listar" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancelar
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Seção 4: Exclusão de Área

**Rota:** POST `/admin/areas/excluir/{id}`
**Arquivo:** `routes/admin_areas_routes.py`
**Requisito:** RF-22 (exclusão)

Esta rota permite excluir áreas que não possuem vagas vinculadas.

---

### 4.1 Rota POST

**Código:**

```python
@router.post("/excluir/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui uma área"""
    assert usuario_logado is not None

    area = area_repo.obter_por_id(id)
    if not area:
        informar_erro(request, "Área não encontrada")
        return RedirectResponse("/admin/areas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se área está sendo usada por vagas
    quantidade_vagas = area_repo.verificar_uso(id)
    if quantidade_vagas > 0:
        informar_erro(
            request,
            f"Não é possível excluir esta área pois existem {quantidade_vagas} vaga(s) vinculada(s) a ela"
        )
        logger.warning(
            f"Admin {usuario_logado['id']} tentou excluir área {id} com {quantidade_vagas} vaga(s) vinculada(s)"
        )
        return RedirectResponse("/admin/areas/listar", status_code=status.HTTP_303_SEE_OTHER)

    area_repo.excluir(id)
    logger.info(f"Área {id} ('{area.nome}') excluída por admin {usuario_logado['id']}")
    informar_sucesso(request, "Área excluída com sucesso!")

    return RedirectResponse("/admin/areas/listar", status_code=status.HTTP_303_SEE_OTHER)
```

**Validações:**
- Verifica se área existe
- **IMPORTANTE:** Verifica se há vagas vinculadas (integridade referencial)
- Log de auditoria

**Observação:** O template com modal de confirmação já está na Seção 1 (listagem).

---

## Seção 5: Listagem de Vagas para Moderação

**Rota:** GET `/admin/vagas/listar`
**Arquivo:** `routes/admin_vagas_routes.py` (NOVO)
**Requisito:** RF-23, RF-24 (visualização)

Esta rota lista vagas para moderação, com filtro por status.

---

### 5.1 Rota GET

**Código:**

```python
from typing import Optional
from fastapi import APIRouter, Form, Request, Query, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from repo import vaga_repo, area_repo, empresa_repo
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.logger_config import logger
from util.perfis import Perfil

router = APIRouter(prefix="/admin/vagas")
templates = criar_templates("templates/admin/vagas")

@router.get("/")
@requer_autenticacao([Perfil.ADMIN.value])
async def index(request: Request, usuario_logado: Optional[dict] = None):
    """Redireciona para lista de vagas"""
    return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_307_TEMPORARY_REDIRECT)

@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def listar(
    request: Request,
    status_filtro: Optional[str] = Query("Pendente"),
    usuario_logado: Optional[dict] = None
):
    """Lista vagas para moderação com filtro de status"""

    # Buscar vagas por status
    if status_filtro:
        vagas = vaga_repo.obter_por_status(status_filtro)
    else:
        vagas = vaga_repo.obter_todas()

    # Enriquecer vagas com dados de área e empresa
    vagas_enriquecidas = []
    for vaga in vagas:
        area = area_repo.obter_por_id(vaga.id_area) if vaga.id_area else None
        empresa = empresa_repo.obter_por_id(vaga.id_empresa) if vaga.id_empresa else None

        vagas_enriquecidas.append({
            "vaga": vaga,
            "area_nome": area.nome if area else "N/A",
            "empresa_nome": empresa.nome if empresa else "N/A"
        })

    status_opcoes = ["Pendente", "Aprovada", "Reprovada", "Arquivada"]

    return templates.TemplateResponse(
        "admin/vagas/listar.html",
        {
            "request": request,
            "vagas": vagas_enriquecidas,
            "status_filtro": status_filtro,
            "status_opcoes": status_opcoes
        }
    )
```

**Descrição:**
- Filtra vagas por status (padrão: Pendente)
- Enriquece dados com nome da área e empresa
- Permite trocar filtro via query parameter

---

### 5.2 Template

**Arquivo:** `templates/admin/vagas/listar.html`

**Código:**

```jinja2
{% extends "base_privada.html" %}

{% block titulo %}Moderar Vagas{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="bi bi-clipboard-check"></i> Moderar Vagas</h2>
        </div>

        <!-- Filtro por Status -->
        <div class="card shadow-sm mb-3">
            <div class="card-body">
                <form method="GET" action="/admin/vagas/listar" class="row g-3 align-items-end">
                    <div class="col-md-4">
                        <label for="status_filtro" class="form-label fw-bold">Filtrar por Status</label>
                        <select name="status_filtro" id="status_filtro" class="form-select">
                            <option value="">Todos</option>
                            {% for opcao in status_opcoes %}
                            <option value="{{ opcao }}" {% if opcao == status_filtro %}selected{% endif %}>
                                {{ opcao }}
                            </option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="col-md-2">
                        <button type="submit" class="btn btn-primary w-100">
                            <i class="bi bi-funnel"></i> Filtrar
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Lista de Vagas -->
        <div class="card shadow-sm">
            <div class="card-body">
                {% if vagas %}
                <div class="table-responsive">
                    <table class="table table-hover align-middle">
                        <thead class="table-light">
                            <tr>
                                <th>ID</th>
                                <th>Título</th>
                                <th>Empresa</th>
                                <th>Área</th>
                                <th>Status</th>
                                <th>Data Cadastro</th>
                                <th class="text-center">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in vagas %}
                            {% set vaga = item.vaga %}
                            <tr>
                                <td>{{ vaga.id_vaga }}</td>
                                <td>
                                    <strong>{{ vaga.titulo }}</strong>
                                    {% if vaga.descricao %}
                                    <br><small class="text-muted">
                                        {{ vaga.descricao[:60] }}{% if vaga.descricao|length > 60 %}...{% endif %}
                                    </small>
                                    {% endif %}
                                </td>
                                <td>{{ item.empresa_nome }}</td>
                                <td>{{ item.area_nome }}</td>
                                <td>
                                    {% if vaga.status == "Pendente" %}
                                    <span class="badge bg-warning text-dark">Pendente</span>
                                    {% elif vaga.status == "Aprovada" %}
                                    <span class="badge bg-success">Aprovada</span>
                                    {% elif vaga.status == "Reprovada" %}
                                    <span class="badge bg-danger">Reprovada</span>
                                    {% elif vaga.status == "Arquivada" %}
                                    <span class="badge bg-secondary">Arquivada</span>
                                    {% endif %}
                                </td>
                                <td>{{ vaga.data_cadastro|data_br if vaga.data_cadastro else '-' }}</td>
                                <td class="text-center">
                                    <div class="btn-group btn-group-sm" role="group">
                                        {% if vaga.status == "Pendente" %}
                                        <button type="button" class="btn btn-outline-success" title="Aprovar"
                                            onclick="aprovarVaga({{ vaga.id_vaga }}, '{{ vaga.titulo|replace("'", "\\'") }}')">
                                            <i class="bi bi-check-circle"></i>
                                        </button>
                                        <button type="button" class="btn btn-outline-danger" title="Reprovar"
                                            onclick="reprovarVaga({{ vaga.id_vaga }}, '{{ vaga.titulo|replace("'", "\\'") }}')">
                                            <i class="bi bi-x-circle"></i>
                                        </button>
                                        {% endif %}

                                        {% if vaga.status in ["Aprovada", "Reprovada"] %}
                                        <button type="button" class="btn btn-outline-secondary" title="Arquivar"
                                            onclick="arquivarVaga({{ vaga.id_vaga }}, '{{ vaga.titulo|replace("'", "\\'") }}')">
                                            <i class="bi bi-archive"></i>
                                        </button>
                                        {% endif %}

                                        <button type="button" class="btn btn-outline-danger" title="Excluir"
                                            onclick="excluirVaga({{ vaga.id_vaga }}, '{{ vaga.titulo|replace("'", "\\'") }}')">
                                            <i class="bi bi-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% else %}
                <div class="alert alert-info text-center mb-0">
                    <i class="bi bi-info-circle"></i> Nenhuma vaga encontrada com o filtro selecionado.
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>

{% include "components/modal_confirmacao.html" %}

<!-- Modal para Reprovar Vaga -->
<div class="modal fade" id="modalReprovarVaga" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header bg-danger text-white">
                <h5 class="modal-title">
                    <i class="bi bi-x-circle"></i> Reprovar Vaga
                </h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <form id="formReprovarVaga" method="POST" action="">
                <div class="modal-body">
                    <p id="modalReprovarMensagem" class="mb-3"></p>
                    <div class="mb-3">
                        <label for="motivo_reprovacao" class="form-label fw-bold">Motivo da Reprovação *</label>
                        <textarea name="motivo" id="motivo_reprovacao" class="form-control" rows="3"
                                  required placeholder="Informe o motivo da reprovação..."></textarea>
                        <small class="text-muted">Este motivo será enviado ao recrutador.</small>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        <i class="bi bi-x-circle"></i> Cancelar
                    </button>
                    <button type="submit" class="btn btn-danger">
                        <i class="bi bi-x-circle"></i> Reprovar Vaga
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    function aprovarVaga(vagaId, vagaTitulo) {
        const detalhes = `
        <div class="card bg-light">
            <div class="card-body">
                <strong>Título:</strong> ${vagaTitulo}
            </div>
        </div>`;

        abrirModalConfirmacao({
            url: `/admin/vagas/aprovar/${vagaId}`,
            mensagem: 'Tem certeza que deseja aprovar esta vaga?',
            detalhes: detalhes
        });
    }

    function reprovarVaga(vagaId, vagaTitulo) {
        const modal = new bootstrap.Modal(document.getElementById('modalReprovarVaga'));
        const form = document.getElementById('formReprovarVaga');
        const mensagem = document.getElementById('modalReprovarMensagem');

        form.action = `/admin/vagas/reprovar/${vagaId}`;
        mensagem.textContent = `Reprovar vaga: "${vagaTitulo}"`;
        modal.show();
    }

    function arquivarVaga(vagaId, vagaTitulo) {
        const detalhes = `
        <div class="card bg-light">
            <div class="card-body">
                <strong>Título:</strong> ${vagaTitulo}
            </div>
        </div>`;

        abrirModalConfirmacao({
            url: `/admin/vagas/arquivar/${vagaId}`,
            mensagem: 'Tem certeza que deseja arquivar esta vaga?',
            detalhes: detalhes
        });
    }

    function excluirVaga(vagaId, vagaTitulo) {
        const detalhes = `
        <div class="card bg-light">
            <div class="card-body">
                <strong>Título:</strong> ${vagaTitulo}
            </div>
        </div>`;

        abrirModalConfirmacao({
            url: `/admin/vagas/excluir/${vagaId}`,
            mensagem: 'Tem certeza que deseja excluir esta vaga? Esta ação não pode ser desfeita.',
            detalhes: detalhes
        });
    }
</script>
{% endblock %}
```

---

## Seção 6: Aprovação de Vaga

**Rota:** POST `/admin/vagas/aprovar/{id}`
**Arquivo:** `routes/admin_vagas_routes.py`
**Requisito:** RF-23 (aprovação)

Esta rota permite aprovar vagas pendentes, tornando-as visíveis publicamente.

---

### 6.1 Rota POST

**Código:**

```python
@router.post("/aprovar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_aprovar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Aprova uma vaga pendente"""
    assert usuario_logado is not None

    vaga = vaga_repo.obter_por_id(id)
    if not vaga:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    if vaga.status != "Pendente":
        informar_erro(request, "Apenas vagas pendentes podem ser aprovadas")
        logger.warning(f"Admin {usuario_logado['id']} tentou aprovar vaga {id} com status '{vaga.status}'")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Atualizar status para Aprovada
    sucesso = vaga_repo.atualizar_status(id, "Aprovada")

    if sucesso:
        logger.info(f"Vaga {id} ('{vaga.titulo}') aprovada por admin {usuario_logado['id']}")
        informar_sucesso(request, "Vaga aprovada com sucesso! Agora ela está visível publicamente.")
    else:
        logger.error(f"Erro ao aprovar vaga {id}")
        informar_erro(request, "Erro ao aprovar vaga")

    return RedirectResponse("/admin/vagas/listar?status_filtro=Pendente", status_code=status.HTTP_303_SEE_OTHER)
```

**Validações:**
- Verifica se vaga existe
- Verifica se status é "Pendente"
- Log de auditoria

**Dependência:** Requer função `vaga_repo.atualizar_status(id, novo_status)` em `repo/vaga_repo.py`.

---

## Seção 7: Reprovação de Vaga

**Rota:** POST `/admin/vagas/reprovar/{id}`
**Arquivo:** `routes/admin_vagas_routes.py`
**Requisito:** RF-23 (reprovação)

Esta rota permite reprovar vagas pendentes com motivo obrigatório.

---

### 7.1 DTO

**Arquivo:** `dtos/vaga_dto.py` (ADICIONAR)

**Código:**

```python
from pydantic import BaseModel, field_validator
from dtos.validators import validar_texto_obrigatorio

class ReprovarVagaDTO(BaseModel):
    """DTO para reprovação de vaga pelo administrador."""
    motivo: str

    _validar_motivo = field_validator("motivo")(validar_texto_obrigatorio(min_length=10, max_length=500))
```

**Se `validar_texto_obrigatorio` não existir em `dtos/validators.py`, criar:**

```python
def validar_texto_obrigatorio(min_length: int = 1, max_length: int = 1000):
    """Validador para campos de texto obrigatórios."""
    def validador(v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Este campo é obrigatório")
        if len(v) < min_length:
            raise ValueError(f"Deve ter no mínimo {min_length} caracteres")
        if len(v) > max_length:
            raise ValueError(f"Deve ter no máximo {max_length} caracteres")
        return v.strip()
    return validador
```

**Validações:**
- `motivo`: Obrigatório, entre 10 e 500 caracteres

---

### 7.2 Rota POST

**Código:**

```python
from dtos.vaga_dto import ReprovarVagaDTO
from util.exceptions import FormValidationError

@router.post("/reprovar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_reprovar(
    request: Request,
    id: int,
    motivo: str = Form(...),
    usuario_logado: Optional[dict] = None
):
    """Reprova uma vaga pendente com motivo"""
    assert usuario_logado is not None

    vaga = vaga_repo.obter_por_id(id)
    if not vaga:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    if vaga.status != "Pendente":
        informar_erro(request, "Apenas vagas pendentes podem ser reprovadas")
        logger.warning(f"Admin {usuario_logado['id']} tentou reprovar vaga {id} com status '{vaga.status}'")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    try:
        # Validar motivo com DTO
        dto = ReprovarVagaDTO(motivo=motivo)

        # Atualizar status para Reprovada
        sucesso = vaga_repo.atualizar_status(id, "Reprovada")

        if sucesso:
            # Registrar motivo da reprovação
            vaga_repo.registrar_motivo_reprovacao(id, dto.motivo)

            logger.info(
                f"Vaga {id} ('{vaga.titulo}') reprovada por admin {usuario_logado['id']} - "
                f"Motivo: {dto.motivo[:50]}..."
            )
            informar_sucesso(request, "Vaga reprovada. O recrutador será notificado.")
        else:
            logger.error(f"Erro ao reprovar vaga {id}")
            informar_erro(request, "Erro ao reprovar vaga")

        return RedirectResponse("/admin/vagas/listar?status_filtro=Pendente", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        informar_erro(request, f"Motivo inválido: {e.errors()[0]['msg']}")
        return RedirectResponse("/admin/vagas/listar?status_filtro=Pendente", status_code=status.HTTP_303_SEE_OTHER)
```

**Validações:**
- Verifica se vaga existe
- Verifica se status é "Pendente"
- Valida motivo com DTO (10-500 caracteres)
- Registra motivo no banco
- Log de auditoria

**Dependências:**
- `vaga_repo.atualizar_status(id, status)`
- `vaga_repo.registrar_motivo_reprovacao(id, motivo)`

**Observação:** O modal de reprovação já está no template da Seção 5 (listagem).

---

## Seção 8: Arquivamento de Vaga

**Rota:** POST `/admin/vagas/arquivar/{id}`
**Arquivo:** `routes/admin_vagas_routes.py`
**Requisito:** RF-24 (arquivamento)

Esta rota permite arquivar vagas aprovadas ou reprovadas.

---

### 8.1 Rota POST

**Código:**

```python
@router.post("/arquivar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_arquivar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Arquiva uma vaga (aprovada ou reprovada)"""
    assert usuario_logado is not None

    vaga = vaga_repo.obter_por_id(id)
    if not vaga:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    if vaga.status not in ["Aprovada", "Reprovada"]:
        informar_erro(request, "Apenas vagas aprovadas ou reprovadas podem ser arquivadas")
        logger.warning(f"Admin {usuario_logado['id']} tentou arquivar vaga {id} com status '{vaga.status}'")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Atualizar status para Arquivada
    sucesso = vaga_repo.atualizar_status(id, "Arquivada")

    if sucesso:
        logger.info(f"Vaga {id} ('{vaga.titulo}') arquivada por admin {usuario_logado['id']}")
        informar_sucesso(request, "Vaga arquivada com sucesso!")
    else:
        logger.error(f"Erro ao arquivar vaga {id}")
        informar_erro(request, "Erro ao arquivar vaga")

    return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)
```

**Validações:**
- Verifica se vaga existe
- Verifica se status é "Aprovada" ou "Reprovada"
- Log de auditoria

**Dependência:** `vaga_repo.atualizar_status(id, status)`

---

## Seção 9: Exclusão de Vaga

**Rota:** POST `/admin/vagas/excluir/{id}`
**Arquivo:** `routes/admin_vagas_routes.py`
**Requisito:** RF-24 (exclusão)

Esta rota permite excluir vagas que não possuem candidaturas vinculadas.

---

### 9.1 Rota POST

**Código:**

```python
@router.post("/excluir/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui uma vaga (qualquer status)"""
    assert usuario_logado is not None

    vaga = vaga_repo.obter_por_id(id)
    if not vaga:
        informar_erro(request, "Vaga não encontrada")
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se há candidaturas vinculadas
    quantidade_candidaturas = vaga_repo.contar_candidaturas(id)
    if quantidade_candidaturas > 0:
        informar_erro(
            request,
            f"Não é possível excluir esta vaga pois existem {quantidade_candidaturas} candidatura(s) vinculada(s). "
            f"Considere arquivar a vaga ao invés de excluí-la."
        )
        logger.warning(
            f"Admin {usuario_logado['id']} tentou excluir vaga {id} com {quantidade_candidaturas} candidatura(s)"
        )
        return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)

    vaga_repo.excluir(id)
    logger.info(f"Vaga {id} ('{vaga.titulo}') excluída por admin {usuario_logado['id']}")
    informar_sucesso(request, "Vaga excluída com sucesso!")

    return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_303_SEE_OTHER)
```

**Validações:**
- Verifica se vaga existe
- **IMPORTANTE:** Verifica se há candidaturas vinculadas (integridade referencial)
- Sugere arquivamento se houver candidaturas
- Log de auditoria

**Dependência:** `vaga_repo.contar_candidaturas(id_vaga)`

---

## Integração com main.py

### Imports e Routers

**Arquivo:** `main.py`

**Adicionar imports:**

```python
from routes.admin_areas_routes import router as admin_areas_router
from routes.admin_vagas_routes import router as admin_vagas_router
```

**Incluir routers (após outros admin routers):**

```python
app.include_router(admin_areas_router, tags=["Admin - Áreas"])
logger.info("Router admin de áreas incluído")

app.include_router(admin_vagas_router, tags=["Admin - Vagas"])
logger.info("Router admin de vagas incluído")
```

---

### Estrutura Completa dos Arquivos de Rotas

#### `routes/admin_areas_routes.py` (COMPLETO)

```python
from typing import Optional
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from dtos.area_dto import CriarAreaDTO, AlterarAreaDTO
from model.area_model import Area
from repo import area_repo
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.logger_config import logger
from util.perfis import Perfil
from util.exceptions import FormValidationError

router = APIRouter(prefix="/admin/areas")
templates = criar_templates("templates/admin/areas")

@router.get("/")
@requer_autenticacao([Perfil.ADMIN.value])
async def index(request: Request, usuario_logado: Optional[dict] = None):
    """Redireciona para lista de áreas"""
    return RedirectResponse("/admin/areas/listar", status_code=status.HTTP_307_TEMPORARY_REDIRECT)

# Código das Seções 1, 2, 3 e 4 (ver seções acima)
```

#### `routes/admin_vagas_routes.py` (COMPLETO)

```python
from typing import Optional
from fastapi import APIRouter, Form, Request, Query, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from dtos.vaga_dto import ReprovarVagaDTO
from repo import vaga_repo, area_repo, empresa_repo
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.logger_config import logger
from util.perfis import Perfil
from util.exceptions import FormValidationError

router = APIRouter(prefix="/admin/vagas")
templates = criar_templates("templates/admin/vagas")

@router.get("/")
@requer_autenticacao([Perfil.ADMIN.value])
async def index(request: Request, usuario_logado: Optional[dict] = None):
    """Redireciona para lista de vagas"""
    return RedirectResponse("/admin/vagas/listar", status_code=status.HTTP_307_TEMPORARY_REDIRECT)

# Código das Seções 5, 6, 7, 8 e 9 (ver seções acima)
```

---

### Funções Necessárias em `repo/vaga_repo.py`

As seguintes funções devem existir (ou serem criadas):

```python
def obter_por_status(status: str) -> list[Vaga]:
    """Busca vagas por status."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM vaga WHERE status = ? ORDER BY data_cadastro DESC",
            (status,)
        )
        rows = cursor.fetchall()
        return [Vaga(**dict(row)) for row in rows]

def atualizar_status(id_vaga: int, novo_status: str) -> bool:
    """Atualiza o status de uma vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE vaga SET status = ? WHERE id_vaga = ?",
            (novo_status, id_vaga)
        )
        return cursor.rowcount > 0

def registrar_motivo_reprovacao(id_vaga: int, motivo: str) -> bool:
    """Registra motivo de reprovação de uma vaga."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE vaga SET motivo_reprovacao = ? WHERE id_vaga = ?",
            (motivo, id_vaga)
        )
        return cursor.rowcount > 0

def contar_candidaturas(id_vaga: int) -> int:
    """Conta quantas candidaturas existem para uma vaga."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) as quantidade FROM candidatura WHERE id_vaga = ?",
                (id_vaga,)
            )
            row = cursor.fetchone()
            return row["quantidade"] if row else 0
    except Exception:
        return 0
```

**IMPORTANTE:** Verificar se a tabela `vaga` possui as colunas `status` e `motivo_reprovacao`.

---

## Checklist de Implementação

### Seção 1: Listagem de Áreas

- [ ] Criar diretório `templates/admin/areas/`
- [ ] Criar rota GET `/admin/areas/listar` em `routes/admin_areas_routes.py`
- [ ] Criar template `templates/admin/areas/listar.html`
- [ ] Testar listagem de áreas

---

### Seção 2: Cadastro de Área

- [ ] Verificar DTOs em `dtos/area_dto.py` (já existem ✅)
- [ ] Criar rota GET `/admin/areas/cadastrar`
- [ ] Criar rota POST `/admin/areas/cadastrar`
- [ ] Criar template `templates/admin/areas/cadastro.html`
- [ ] Testar cadastro de área com validações

---

### Seção 3: Edição de Área

- [ ] Criar rota GET `/admin/areas/editar/{id}`
- [ ] Criar rota POST `/admin/areas/editar/{id}`
- [ ] Criar template `templates/admin/areas/editar.html`
- [ ] Testar edição de área

---

### Seção 4: Exclusão de Área

- [ ] Criar rota POST `/admin/areas/excluir/{id}`
- [ ] Testar exclusão com validação de integridade referencial

---

### Seção 5: Listagem de Vagas para Moderação

- [ ] Criar arquivo `routes/admin_vagas_routes.py`
- [ ] Criar diretório `templates/admin/vagas/`
- [ ] Criar rota GET `/admin/vagas/listar`
- [ ] Criar template `templates/admin/vagas/listar.html`
- [ ] Implementar filtro por status
- [ ] Testar listagem com diferentes filtros

---

### Seção 6: Aprovação de Vaga

- [ ] Criar rota POST `/admin/vagas/aprovar/{id}`
- [ ] Criar função `vaga_repo.atualizar_status()` se não existir
- [ ] Testar aprovação de vaga

---

### Seção 7: Reprovação de Vaga

- [ ] Criar DTO `ReprovarVagaDTO` em `dtos/vaga_dto.py`
- [ ] Criar validador `validar_texto_obrigatorio()` se não existir
- [ ] Criar rota POST `/admin/vagas/reprovar/{id}`
- [ ] Criar função `vaga_repo.registrar_motivo_reprovacao()` se não existir
- [ ] Testar reprovação com motivo

---

### Seção 8: Arquivamento de Vaga

- [ ] Criar rota POST `/admin/vagas/arquivar/{id}`
- [ ] Testar arquivamento de vaga

---

### Seção 9: Exclusão de Vaga

- [ ] Criar rota POST `/admin/vagas/excluir/{id}`
- [ ] Criar função `vaga_repo.contar_candidaturas()` se não existir
- [ ] Testar exclusão com validação de integridade

---

### Integração

- [ ] Adicionar imports em `main.py`
- [ ] Incluir routers em `main.py`
- [ ] Verificar colunas no banco (`status`, `motivo_reprovacao`)
- [ ] Testar todas as rotas integradas

---

### Testes

- [ ] Criar `tests/test_admin_areas_routes.py`
- [ ] Criar `tests/test_admin_vagas_routes.py`
- [ ] Testar DTOs de validação
- [ ] Testar fluxo completo de CRUD de áreas
- [ ] Testar fluxo completo de moderação de vagas
- [ ] Testar permissões (apenas ADMIN acessa)
- [ ] Testar integridade referencial
- [ ] Testar responsividade dos templates
- [ ] Testar modals de confirmação
- [ ] Testar flash messages

---

## Observações Finais

### Ordem Recomendada de Implementação

1. **Seções 1-4:** Gerenciamento de Áreas (implementar na ordem)
2. **Verificar/criar funções auxiliares em `vaga_repo.py`**
3. **Seções 5-9:** Moderação de Vagas (implementar na ordem)
4. **Testes abrangentes**

### Considerações de Segurança

- ✅ Todas as rotas protegidas com `@requer_autenticacao([Perfil.ADMIN.value])`
- ✅ Validação de entrada com DTOs
- ✅ Log de auditoria em todas as operações críticas
- ✅ Verificação de integridade referencial antes de exclusões
- ✅ Flash messages informativos para o usuário

### Padrões Mantidos

- ✅ Estrutura de arquivos igual ao projeto original
- ✅ Nomenclatura de variáveis e funções consistente
- ✅ DTOs com `field_validator` do Pydantic
- ✅ Templates estendendo `base_privada.html`
- ✅ Uso de macros para campos de formulário
- ✅ Modal de confirmação para exclusões
- ✅ Redirect com status `HTTP_303_SEE_OTHER` após POST
- ✅ Flash messages com `informar_sucesso` e `informar_erro`

---

**Fim do Plano de Implementação FASE 2**
