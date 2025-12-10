# Atividade Final: 5 Aprimoramentos para o Sistema Estagiou

## Visão Geral do Projeto
O **Estagiou** é uma plataforma de estágios construída com FastAPI + Bootstrap 5. Possui três perfis de usuário: Estudante, Recrutador e Administrador.

---

# Atividade 1 - Aluno 1: Adicionar Contador de Caracteres no Formulário de Cadastro de Vagas

**Objetivo:** Adicionar um contador de caracteres em tempo real nos campos de texto do formulário de cadastro de vagas do recrutador.

**Arquivo a modificar:** `templates/recrutador/vagas/cadastro.html`

**Tempo estimado:** 30-40 minutos

---

## Passo 0: Criar a branch de trabalho

Antes de começar a atividade, você deve criar uma branch com seu primeiro nome. Abra o terminal na pasta do projeto e execute:

```bash
git checkout -b aluno1
```

> **Importante:** Substitua `aluno1` pelo seu primeiro nome em minúsculas (ex: `joao`, `maria`, `pedro`).

---

## Passo 1: Abrir o arquivo do formulário
Abra o arquivo `templates/recrutador/vagas/cadastro.html` no seu editor de código.

---

## Passo 2: Adicionar o bloco de estilos CSS
O arquivo atual não possui um bloco `{% block styles %}`. Você precisa adicionar este bloco **antes** do `{% block content %}`.

Localize a linha 6 que contém `{% block content %}` e adicione **antes** dela:

```html
{% block styles %}
<style>
    .char-counter {
        font-size: 0.85rem;
        color: #6c757d;
        text-align: right;
        margin-top: 4px;
    }
    .char-counter.warning {
        color: #ffc107;
    }
    .char-counter.danger {
        color: #dc3545;
    }
</style>
{% endblock %}

```

---

## Passo 3: Adicionar o contador ao campo "Título"
Localize as linhas 26-29 que contêm o campo de título:

```html
<div class="col-md-8 mb-3">
    {{ field(name='titulo', label='Título da Vaga', type='text', required=true,
             placeholder='Ex: Estagiário em Desenvolvimento de Software') }}
</div>
```

Substitua por:

```html
<div class="col-md-8 mb-3">
    {{ field(name='titulo', label='Título da Vaga', type='text', required=true,
             placeholder='Ex: Estagiário em Desenvolvimento de Software') }}
    <div class="char-counter" id="contador-titulo">
        <span id="chars-titulo">0</span> / 100 caracteres
    </div>
</div>
```

---

## Passo 4: Adicionar o contador ao campo "Descrição"
Localize as linhas 45-48 que contêm o campo de descrição:

```html
<div class="col-12 mb-3">
    {{ field(name='descricao', label='Descrição da Vaga', type='textarea', required=true,
             rows=4, placeholder='Descreva as atividades e responsabilidades do estagiário...') }}
</div>
```

Substitua por:

```html
<div class="col-12 mb-3">
    {{ field(name='descricao', label='Descrição da Vaga', type='textarea', required=true,
             rows=4, placeholder='Descreva as atividades e responsabilidades do estagiário...') }}
    <div class="char-counter" id="contador-descricao">
        <span id="chars-descricao">0</span> / 2000 caracteres
    </div>
</div>
```

---

## Passo 5: Adicionar o bloco de scripts JavaScript
O arquivo atual não possui um bloco `{% block scripts %}`. Adicione este bloco **após** o `{% endblock %}` final (depois da linha 159).

No final do arquivo, adicione:

```html
{% block scripts %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Contador para o título
        const inputTitulo = document.querySelector('input[name="titulo"]');
        const contadorTitulo = document.getElementById('chars-titulo');
        const divContadorTitulo = document.getElementById('contador-titulo');

        if (inputTitulo) {
            inputTitulo.addEventListener('input', function() {
                const length = this.value.length;
                contadorTitulo.textContent = length;

                divContadorTitulo.classList.remove('warning', 'danger');
                if (length >= 90) {
                    divContadorTitulo.classList.add('danger');
                } else if (length >= 70) {
                    divContadorTitulo.classList.add('warning');
                }
            });
            // Atualiza contador ao carregar (para quando há dados pré-preenchidos)
            contadorTitulo.textContent = inputTitulo.value.length;
        }

        // Contador para a descrição
        const textareaDescricao = document.querySelector('textarea[name="descricao"]');
        const contadorDescricao = document.getElementById('chars-descricao');
        const divContadorDescricao = document.getElementById('contador-descricao');

        if (textareaDescricao) {
            textareaDescricao.addEventListener('input', function() {
                const length = this.value.length;
                contadorDescricao.textContent = length;

                divContadorDescricao.classList.remove('warning', 'danger');
                if (length >= 1800) {
                    divContadorDescricao.classList.add('danger');
                } else if (length >= 1500) {
                    divContadorDescricao.classList.add('warning');
                }
            });
            // Atualiza contador ao carregar
            contadorDescricao.textContent = textareaDescricao.value.length;
        }
    });
</script>
{% endblock %}
```

---

## Como testar:
1. Inicie o servidor: `python main.py`
2. Acesse http://localhost:8000/login
3. Faça login como Recrutador
4. Acesse o menu "Cadastrar Vaga" ou vá para http://localhost:8000/recrutador/vagas/cadastrar
5. Digite texto nos campos "Título da Vaga" e "Descrição da Vaga"
6. Observe o contador atualizando em tempo real abaixo de cada campo
7. Verifique que a cor muda para amarelo (warning) e vermelho (danger) quando se aproxima do limite

---

## Passo Final: Fazer o commit da atividade

Após concluir e testar a atividade, você deve salvar suas alterações no Git. Execute os seguintes comandos no terminal:

```bash
git add .
git commit -m "Adiciona contador de caracteres no formulário de cadastro de vagas"
```

---

---

---

# Atividade 2 - Aluno 2: Adicionar Filtro por Status nas Candidaturas do Estudante

**Objetivo:** Permitir que o estudante filtre suas candidaturas por status (Pendente, Aprovado, Rejeitado, etc.)

**Arquivo a modificar:** `templates/candidaturas/minhas.html`

**Tempo estimado:** 40-50 minutos

---

## Passo 0: Criar a branch de trabalho

Antes de começar a atividade, você deve criar uma branch com seu primeiro nome. Abra o terminal na pasta do projeto e execute:

```bash
git checkout -b aluno2
```

> **Importante:** Substitua `aluno2` pelo seu primeiro nome em minúsculas (ex: `joao`, `maria`, `pedro`).

---

## Passo 1: Abrir o arquivo
Abra o arquivo `templates/candidaturas/minhas.html` no seu editor de código.

---

## Passo 2: Adicionar o bloco de estilos CSS
O arquivo atual não possui um bloco `{% block styles %}`. Adicione este bloco **antes** do `{% block content %}` (antes da linha 5).

Localize a linha 4 que contém `{% block titulo %}Minhas Candidaturas{% endblock %}` e adicione **após** ela:

```html
{% block styles %}
<style>
    .filtro-status {
        margin-bottom: 1.5rem;
    }
    .btn-filtro {
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .btn-filtro.active {
        box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.25);
    }
    .linha-candidatura.hidden {
        display: none;
    }
    .contador-resultados {
        font-size: 0.9rem;
        color: #6c757d;
        margin-top: 0.5rem;
    }
</style>
{% endblock %}

```

---

## Passo 3: Adicionar os botões de filtro
Localize as linhas 24-25 que fecham o page-header:

```html
    </div>
</div>
```

Adicione **logo após** (antes da linha 26 `<div class="row">`):

```html
<!-- Filtros de Status -->
<div class="filtro-status">
    <div class="d-flex flex-wrap align-items-center gap-2">
        <span class="text-muted me-2">Filtrar por status:</span>
        <button type="button" class="btn btn-outline-secondary btn-sm btn-filtro active" data-status="todos">
            Todos
        </button>
        <button type="button" class="btn btn-outline-warning btn-sm btn-filtro" data-status="pendente">
            Pendente
        </button>
        <button type="button" class="btn btn-outline-info btn-sm btn-filtro" data-status="em_analise">
            Em Análise
        </button>
        <button type="button" class="btn btn-outline-success btn-sm btn-filtro" data-status="aprovado">
            Aprovado
        </button>
        <button type="button" class="btn btn-outline-danger btn-sm btn-filtro" data-status="rejeitado">
            Rejeitado
        </button>
        <button type="button" class="btn btn-outline-dark btn-sm btn-filtro" data-status="cancelado">
            Cancelado
        </button>
    </div>
    <div class="contador-resultados">
        Exibindo <span id="qtd-exibida">0</span> de <span id="qtd-total">0</span> candidaturas
    </div>
</div>

```

---

## Passo 4: Adicionar atributo data-status nas linhas da tabela
O template usa uma tabela para listar as candidaturas. Localize a linha 44-45 que contém o loop:

```html
{% for item in candidaturas %}
<tr>
```

Substitua por:

```html
{% for item in candidaturas %}
<tr class="linha-candidatura" data-status="{{ item.candidatura.status }}">
```

---

## Passo 5: Modificar o JavaScript existente
O arquivo já possui um bloco `{% block scripts %}` (linhas 122-149). Você precisa adicionar o código de filtro **dentro** desse bloco.

Localize a linha 123 que contém `<script>` e substitua todo o bloco de script (linhas 123-148) por:

```html
<script>
    // Função existente para cancelar candidatura
    function cancelarCandidatura(candidaturaId, vagaTitulo) {
        const detalhes = `
        <div class="card bg-light">
            <div class="card-body">
                <table class="table table-sm table-borderless mb-0">
                    <tr>
                        <th width="30%">Vaga:</th>
                        <td>${vagaTitulo}</td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="alert alert-warning mt-3 mb-0">
            <i class="bi bi-exclamation-triangle"></i>
            Esta ação não pode ser desfeita.
        </div>
        `;

        abrirModalConfirmacao({
            url: `/candidaturas/cancelar/${candidaturaId}`,
            mensagem: 'Tem certeza que deseja cancelar esta candidatura?',
            detalhes: detalhes
        });
    }

    // Novo código para filtro de status
    document.addEventListener('DOMContentLoaded', function() {
        const btnsFiltro = document.querySelectorAll('.btn-filtro');
        const linhas = document.querySelectorAll('.linha-candidatura');
        const qtdExibida = document.getElementById('qtd-exibida');
        const qtdTotal = document.getElementById('qtd-total');

        // Define os valores iniciais
        if (qtdTotal && qtdExibida) {
            qtdTotal.textContent = linhas.length;
            qtdExibida.textContent = linhas.length;
        }

        btnsFiltro.forEach(btn => {
            btn.addEventListener('click', function() {
                // Remove active de todos os botões
                btnsFiltro.forEach(b => b.classList.remove('active'));
                // Adiciona active no botão clicado
                this.classList.add('active');

                const statusSelecionado = this.dataset.status;
                let visiveisCount = 0;

                linhas.forEach(linha => {
                    if (statusSelecionado === 'todos' || linha.dataset.status === statusSelecionado) {
                        linha.classList.remove('hidden');
                        visiveisCount++;
                    } else {
                        linha.classList.add('hidden');
                    }
                });

                if (qtdExibida) {
                    qtdExibida.textContent = visiveisCount;
                }
            });
        });
    });
</script>
```

---

## Como testar:
1. Inicie o servidor: `python main.py`
2. Acesse http://localhost:8000/login
3. Faça login como Estudante
4. Acesse o menu "Minhas Candidaturas" ou vá para http://localhost:8000/candidaturas/minhas
5. Observe os botões de filtro abaixo do título da página
6. Clique em cada botão de filtro (Todos, Pendente, Em Análise, etc.)
7. Verifique que apenas as candidaturas do status selecionado aparecem na tabela
8. Observe o contador atualizando (ex: "Exibindo 2 de 5 candidaturas")

---

## Passo Final: Fazer o commit da atividade

Após concluir e testar a atividade, você deve salvar suas alterações no Git. Execute os seguintes comandos no terminal:

```bash
git add .
git commit -m "Adiciona filtro por status nas candidaturas do estudante"
```

---

---

---

# Atividade 3 - Aluno 3: Adicionar Botão "Copiar Link" na Página de Detalhes da Vaga

**Objetivo:** Permitir que o usuário copie o link da vaga para compartilhar facilmente.

**Arquivo a modificar:** `templates/vagas/detalhes.html`

**Tempo estimado:** 25-35 minutos

---

## Passo 0: Criar a branch de trabalho

Antes de começar a atividade, você deve criar uma branch com seu primeiro nome. Abra o terminal na pasta do projeto e execute:

```bash
git checkout -b aluno3
```

> **Importante:** Substitua `aluno3` pelo seu primeiro nome em minúsculas (ex: `joao`, `maria`, `pedro`).

---

## Passo 1: Abrir o arquivo
Abra o arquivo `templates/vagas/detalhes.html` no seu editor de código.

---

## Passo 2: Adicionar o bloco de estilos CSS
O arquivo atual não possui um bloco `{% block styles %}`. Adicione este bloco **antes** do `{% block content %}` (antes da linha 5).

Localize a linha 3 que contém `{% block titulo %}{{ vaga.titulo }}{% endblock %}` e adicione **após** ela:

```html
{% block styles %}
<style>
    .btn-compartilhar {
        position: relative;
        display: inline-block;
    }
    .tooltip-copiado {
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background-color: #198754;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        white-space: nowrap;
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.3s, visibility 0.3s;
        margin-bottom: 0.5rem;
    }
    .tooltip-copiado.show {
        opacity: 1;
        visibility: visible;
    }
    .tooltip-copiado::after {
        content: '';
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        border: 6px solid transparent;
        border-top-color: #198754;
    }
</style>
{% endblock %}

```

---

## Passo 3: Adicionar o botão de compartilhar
Localize as linhas 9-13 que contêm o botão "Voltar para Vagas":

```html
<!-- Navegação -->
<div class="mb-4">
    <a href="/vagas" class="btn btn-outline-primary btn-sm">
        <i class="bi bi-arrow-left me-1"></i>Voltar para Vagas
    </a>
</div>
```

Substitua por:

```html
<!-- Navegação -->
<div class="mb-4 d-flex justify-content-between align-items-center">
    <a href="/vagas" class="btn btn-outline-primary btn-sm">
        <i class="bi bi-arrow-left me-1"></i>Voltar para Vagas
    </a>
    <div class="btn-compartilhar">
        <button type="button" class="btn btn-outline-secondary btn-sm" id="btn-copiar-link">
            <i class="bi bi-share me-1"></i>Compartilhar Vaga
        </button>
        <div class="tooltip-copiado" id="tooltip-copiado">
            Link copiado!
        </div>
    </div>
</div>
```

---

## Passo 4: Adicionar o bloco de scripts JavaScript
O arquivo atual não possui um bloco `{% block scripts %}`. Adicione este bloco **no final do arquivo**, após o último `{% endblock %}` (após a linha 239).

No final do arquivo, adicione:

```html
{% block scripts %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const btnCopiar = document.getElementById('btn-copiar-link');
        const tooltip = document.getElementById('tooltip-copiado');

        if (btnCopiar) {
            btnCopiar.addEventListener('click', function() {
                // Pega a URL atual da página
                const url = window.location.href;

                // Copia para a área de transferência
                navigator.clipboard.writeText(url).then(function() {
                    // Mostra o tooltip de sucesso
                    tooltip.classList.add('show');

                    // Muda o texto do botão temporariamente
                    const textoOriginal = btnCopiar.innerHTML;
                    btnCopiar.innerHTML = '<i class="bi bi-check me-1"></i>Copiado!';
                    btnCopiar.classList.remove('btn-outline-secondary');
                    btnCopiar.classList.add('btn-success');

                    // Volta ao estado original após 2 segundos
                    setTimeout(function() {
                        tooltip.classList.remove('show');
                        btnCopiar.innerHTML = textoOriginal;
                        btnCopiar.classList.remove('btn-success');
                        btnCopiar.classList.add('btn-outline-secondary');
                    }, 2000);
                }).catch(function(err) {
                    console.error('Erro ao copiar:', err);
                    alert('Não foi possível copiar o link. Copie manualmente: ' + url);
                });
            });
        }
    });
</script>
{% endblock %}
```

---

## Como testar:
1. Inicie o servidor: `python main.py`
2. Acesse http://localhost:8000/vagas
3. Clique em qualquer vaga para ver seus detalhes
4. Observe o botão "Compartilhar Vaga" no canto superior direito (ao lado do botão "Voltar")
5. Clique no botão "Compartilhar Vaga"
6. Verifique que:
   - O tooltip verde "Link copiado!" aparece acima do botão
   - O botão muda para verde com o texto "Copiado!"
   - Após 2 segundos, volta ao estado original
7. Cole o link em algum lugar (Ctrl+V ou Cmd+V) para confirmar que foi copiado corretamente

---

## Passo Final: Fazer o commit da atividade

Após concluir e testar a atividade, você deve salvar suas alterações no Git. Execute os seguintes comandos no terminal:

```bash
git add .
git commit -m "Adiciona botão de compartilhar na página de detalhes da vaga"
```

---

---

---

# Atividade 4 - Aluno 4: Adicionar Indicador de "Vaga Vista Recentemente" com LocalStorage

**Objetivo:** Marcar visualmente as vagas que o usuário já visualizou, usando LocalStorage do navegador.

**Arquivos a modificar:**
- `templates/vagas/listar.html`
- `templates/vagas/detalhes.html`

**Tempo estimado:** 40-50 minutos

---

## Passo 0: Criar a branch de trabalho

Antes de começar a atividade, você deve criar uma branch com seu primeiro nome. Abra o terminal na pasta do projeto e execute:

```bash
git checkout -b aluno4
```

> **Importante:** Substitua `aluno4` pelo seu primeiro nome em minúsculas (ex: `joao`, `maria`, `pedro`).

---

## Parte A: Modificar a página de listagem

---

## Passo 1: Abrir o arquivo de listagem
Abra o arquivo `templates/vagas/listar.html` no seu editor de código.

---

## Passo 2: Adicionar o bloco de estilos CSS
O arquivo atual não possui um bloco `{% block styles %}`. Adicione este bloco **antes** do `{% block content %}` (antes da linha 5).

Localize a linha 3 que contém `{% block titulo %}Vagas de Estágio{% endblock %}` e adicione **após** ela:

```html
{% block styles %}
<style>
    .badge-visto {
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 0.7rem;
    }
    .job-card {
        position: relative;
    }
    .job-card.ja-vista {
        border-left: 4px solid #6c757d !important;
    }
    .job-card.ja-vista .card-title {
        color: #6c757d !important;
    }
</style>
{% endblock %}

```

---

## Passo 3: Adicionar atributo data-id nos cards de vaga
Localize a linha 88 que contém o card da vaga:

```html
<div class="card job-card h-100">
```

Substitua por:

```html
<div class="card job-card h-100" data-id="{{ item.vaga.id_vaga }}">
```

---

## Passo 4: Adicionar o bloco de scripts JavaScript
O arquivo atual não possui um bloco `{% block scripts %}`. Adicione este bloco **no final do arquivo**, após o último `{% endblock %}` (após a linha 166).

No final do arquivo, adicione:

```html
{% block scripts %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Recupera as vagas vistas do localStorage
        const vagasVistas = JSON.parse(localStorage.getItem('vagasVistas') || '[]');

        // Marca os cards das vagas já vistas
        document.querySelectorAll('.job-card').forEach(function(card) {
            const idVaga = card.dataset.id;
            if (idVaga && vagasVistas.includes(idVaga)) {
                card.classList.add('ja-vista');

                // Adiciona o badge "Vista"
                const badge = document.createElement('span');
                badge.className = 'badge bg-secondary badge-visto';
                badge.innerHTML = '<i class="bi bi-eye me-1"></i>Vista';
                card.querySelector('.card-body').appendChild(badge);
            }
        });
    });
</script>
{% endblock %}
```

---

## Parte B: Modificar a página de detalhes

---

## Passo 5: Abrir o arquivo de detalhes
Abra o arquivo `templates/vagas/detalhes.html` no seu editor de código.

**Nota:** Se você já fez a Atividade 3 (Botão Compartilhar), o arquivo já terá um bloco `{% block scripts %}`. Neste caso, você só precisa adicionar o código dentro do script existente.

---

## Passo 6: Adicionar o código para salvar a vaga vista

**Se o arquivo NÃO tem `{% block scripts %}`** (se a Atividade 3 não foi feita), adicione no final do arquivo:

```html
{% block scripts %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Pega o ID da vaga atual
        const idVaga = '{{ vaga.id_vaga }}';

        // Recupera as vagas vistas do localStorage
        let vagasVistas = JSON.parse(localStorage.getItem('vagasVistas') || '[]');

        // Adiciona esta vaga se ainda não estiver na lista
        if (!vagasVistas.includes(idVaga)) {
            vagasVistas.push(idVaga);

            // Limita a 50 vagas para não crescer demais o localStorage
            if (vagasVistas.length > 50) {
                vagasVistas = vagasVistas.slice(-50);
            }

            localStorage.setItem('vagasVistas', JSON.stringify(vagasVistas));
        }
    });
</script>
{% endblock %}
```

**Se o arquivo JÁ tem `{% block scripts %}`** (se a Atividade 3 foi feita), adicione o código **dentro** do `document.addEventListener('DOMContentLoaded', function() { ... })` existente, antes do fechamento `});`:

```javascript
        // ========== CÓDIGO PARA MARCAR VAGA COMO VISTA ==========
        // Pega o ID da vaga atual
        const idVaga = '{{ vaga.id_vaga }}';

        // Recupera as vagas vistas do localStorage
        let vagasVistas = JSON.parse(localStorage.getItem('vagasVistas') || '[]');

        // Adiciona esta vaga se ainda não estiver na lista
        if (!vagasVistas.includes(idVaga)) {
            vagasVistas.push(idVaga);

            // Limita a 50 vagas para não crescer demais o localStorage
            if (vagasVistas.length > 50) {
                vagasVistas = vagasVistas.slice(-50);
            }

            localStorage.setItem('vagasVistas', JSON.stringify(vagasVistas));
        }
```

---

## Como testar:
1. Inicie o servidor: `python main.py`
2. Acesse http://localhost:8000/vagas
3. Observe que nenhuma vaga tem marcação especial (primeira visita)
4. Clique em qualquer vaga para ver seus detalhes
5. Clique no botão "Voltar para Vagas" para retornar à listagem
6. Observe que a vaga que você visualizou agora tem:
   - Uma borda cinza à esquerda
   - Um badge "Vista" no canto superior direito do card
   - O título em cor mais suave
7. Clique em outra vaga e repita o processo
8. Feche o navegador, abra novamente e acesse a listagem - as vagas vistas devem continuar marcadas (dados salvos no LocalStorage)

---

## Passo Final: Fazer o commit da atividade

Após concluir e testar a atividade, você deve salvar suas alterações no Git. Execute os seguintes comandos no terminal:

```bash
git add .
git commit -m "Adiciona indicador de vaga vista recentemente com LocalStorage"
```

---

---

---

# Atividade 5 - Aluno 5: Adicionar Estatísticas Rápidas no Dashboard do Recrutador

**Objetivo:** Mostrar cards com estatísticas das vagas do recrutador (total de vagas, vagas abertas, fechadas e total de candidaturas).

**Arquivos a modificar:**
- `routes/recrutador_vagas_routes.py`
- `templates/recrutador/vagas/listar.html`

**Tempo estimado:** 50-60 minutos

---

## Passo 0: Criar a branch de trabalho

Antes de começar a atividade, você deve criar uma branch com seu primeiro nome. Abra o terminal na pasta do projeto e execute:

```bash
git checkout -b aluno5
```

> **Importante:** Substitua `aluno5` pelo seu primeiro nome em minúsculas (ex: `joao`, `maria`, `pedro`).

---

## Parte A: Modificar a rota (backend)

---

## Passo 1: Abrir o arquivo de rotas
Abra o arquivo `routes/recrutador_vagas_routes.py` no seu editor de código.

---

## Passo 2: Localizar a função `listar`
Localize a função `listar` que começa na linha 30:

```python
@router.get("/listar")
@requer_autenticacao([Perfil.RECRUTADOR.value])
async def listar(request: Request, usuario_logado: Optional[dict] = None):
```

---

## Passo 3: Adicionar o cálculo das estatísticas
Localize as linhas 48-52 que contêm o retorno do template:

```python
    return templates.TemplateResponse(
        "recrutador/vagas/listar.html",
        {"request": request, "vagas": vagas_enriquecidas, "usuario_logado": usuario_logado}
    )
```

Substitua por (adicionando o cálculo de estatísticas antes do return):

```python
    # Calcula estatísticas das vagas
    total_vagas = len(vagas)
    vagas_abertas = sum(1 for v in vagas if v.status_vaga == 'aberta')
    vagas_fechadas = sum(1 for v in vagas if v.status_vaga == 'fechada')
    vagas_suspensas = sum(1 for v in vagas if v.status_vaga == 'suspensa')
    total_candidaturas = sum(item['qtd_candidaturas'] for item in vagas_enriquecidas)

    estatisticas = {
        'total_vagas': total_vagas,
        'vagas_abertas': vagas_abertas,
        'vagas_fechadas': vagas_fechadas,
        'vagas_suspensas': vagas_suspensas,
        'total_candidaturas': total_candidaturas
    }

    return templates.TemplateResponse(
        "recrutador/vagas/listar.html",
        {
            "request": request,
            "vagas": vagas_enriquecidas,
            "estatisticas": estatisticas,
            "usuario_logado": usuario_logado
        }
    )
```

---

## Parte B: Modificar o template (frontend)

---

## Passo 4: Abrir o arquivo do template
Abra o arquivo `templates/recrutador/vagas/listar.html` no seu editor de código.

---

## Passo 5: Adicionar o bloco de estilos CSS
O arquivo atual não possui um bloco `{% block styles %}`. Adicione este bloco **antes** do `{% block content %}` (antes da linha 5).

Localize a linha 3 que contém `{% block titulo %}Minhas Vagas{% endblock %}` e adicione **após** ela:

```html
{% block styles %}
<style>
    .stats-container {
        margin-bottom: 2rem;
    }
    .stat-card {
        text-align: center;
        padding: 1.5rem;
        border-radius: 0.75rem;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    .stat-card .stat-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .stat-card .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        display: block;
        line-height: 1;
    }
    .stat-card .stat-label {
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    .stat-card.total {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .stat-card.abertas {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
    }
    .stat-card.fechadas {
        background: linear-gradient(135deg, #636363 0%, #a2a2a2 100%);
        color: white;
    }
    .stat-card.candidaturas {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
</style>
{% endblock %}

```

---

## Passo 6: Adicionar os cards de estatística no HTML
Localize as linhas 24-25 que fecham o page-header:

```html
    </div>
</div>
```

Adicione **logo após** (antes da linha 26 `<div class="row">`):

```html
<!-- Cards de Estatísticas -->
<div class="stats-container">
    <div class="row g-3">
        <div class="col-6 col-lg-3">
            <div class="stat-card total">
                <div class="stat-icon"><i class="bi bi-briefcase"></i></div>
                <span class="stat-number">{{ estatisticas.total_vagas }}</span>
                <span class="stat-label">Total de Vagas</span>
            </div>
        </div>
        <div class="col-6 col-lg-3">
            <div class="stat-card abertas">
                <div class="stat-icon"><i class="bi bi-check-circle"></i></div>
                <span class="stat-number">{{ estatisticas.vagas_abertas }}</span>
                <span class="stat-label">Vagas Abertas</span>
            </div>
        </div>
        <div class="col-6 col-lg-3">
            <div class="stat-card fechadas">
                <div class="stat-icon"><i class="bi bi-x-circle"></i></div>
                <span class="stat-number">{{ estatisticas.vagas_fechadas }}</span>
                <span class="stat-label">Vagas Fechadas</span>
            </div>
        </div>
        <div class="col-6 col-lg-3">
            <div class="stat-card candidaturas">
                <div class="stat-icon"><i class="bi bi-people"></i></div>
                <span class="stat-number">{{ estatisticas.total_candidaturas }}</span>
                <span class="stat-label">Total Candidaturas</span>
            </div>
        </div>
    </div>
</div>

```

---

## Como testar:
1. Inicie o servidor: `python main.py`
2. Acesse http://localhost:8000/login
3. Faça login como Recrutador
4. Acesse o menu "Minhas Vagas" ou vá para http://localhost:8000/recrutador/vagas/listar
5. Observe os 4 cards coloridos de estatísticas no topo da página:
   - **Total de Vagas** (roxo): quantidade total de vagas cadastradas
   - **Vagas Abertas** (verde): vagas com status "aberta"
   - **Vagas Fechadas** (cinza): vagas com status "fechada"
   - **Total Candidaturas** (rosa): soma de todas as candidaturas recebidas
6. Passe o mouse sobre os cards e observe o efeito de elevação (hover)
7. Cadastre uma nova vaga e retorne à listagem - os números devem atualizar automaticamente

---

## Passo Final: Fazer o commit da atividade

Após concluir e testar a atividade, você deve salvar suas alterações no Git. Execute os seguintes comandos no terminal:

```bash
git add .
git commit -m "Adiciona cards de estatísticas no dashboard do recrutador"
```

---

---

---

# Resumo das Atividades

| Aluno | Atividade | Tempo | Dificuldade | Arquivos |
|-------|-----------|-------|-------------|----------|
| Aluno 1 | Contador de caracteres no formulário | 30-40 min | Fácil | `templates/recrutador/vagas/cadastro.html` |
| Aluno 2 | Filtro por status nas candidaturas | 40-50 min | Fácil | `templates/candidaturas/minhas.html` |
| Aluno 3 | Botão "Copiar Link" da vaga | 25-35 min | Fácil | `templates/vagas/detalhes.html` |
| Aluno 4 | Indicador "Vaga Vista" | 40-50 min | Fácil | `templates/vagas/listar.html`, `templates/vagas/detalhes.html` |
| Aluno 5 | Cards de estatísticas | 50-60 min | Fácil | `routes/recrutador_vagas_routes.py`, `templates/recrutador/vagas/listar.html` |

## Características das Atividades:
- Todas são **independentes** e podem ser realizadas simultaneamente
- Todas têm **duração máxima de 60 minutos**
- Todas são de **nível fácil** com instruções passo a passo
- Todos os **códigos necessários** estão disponibilizados
- Nenhuma requer conhecimento avançado de Python ou JavaScript

## Fluxo de Trabalho Git:
1. **Antes de iniciar:** Criar branch com seu primeiro nome (`git checkout -b seunome`)
2. **Durante:** Salvar os arquivos normalmente
3. **Ao finalizar:** Fazer commit das alterações (`git add .` e `git commit -m "mensagem"`)
