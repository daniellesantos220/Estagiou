# Casos de Uso - Sistema Estagiou

Este documento descreve todos os casos de uso (requisitos funcionais) do sistema Estagiou, organizados por módulo e indicando os perfis de usuário que podem executar cada funcionalidade.

---

## Perfis de Usuário

| Perfil | Descrição |
|--------|-----------|
| **Visitante** | Usuário não autenticado |
| **Estudante** | Usuário que busca vagas de estágio |
| **Recrutador** | Representante de empresa que publica vagas |
| **Administrador** | Usuário com controle total do sistema |

---

## 1. Autenticação e Controle de Acesso

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-AUTH-01 | Realizar login no sistema | X | - | - | - |
| UC-AUTH-02 | Realizar cadastro de conta | X | - | - | - |
| UC-AUTH-03 | Solicitar recuperação de senha | X | - | - | - |
| UC-AUTH-04 | Redefinir senha via token | X | - | - | - |
| UC-AUTH-05 | Realizar logout | - | X | X | X |

---

## 2. Gerenciamento de Perfil

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-PERF-01 | Visualizar próprio perfil | - | X | X | X |
| UC-PERF-02 | Editar dados do perfil | - | X | X | X |
| UC-PERF-03 | Alterar senha da conta | - | X | X | X |
| UC-PERF-04 | Atualizar foto de perfil | - | X | X | X |
| UC-PERF-05 | Visualizar dashboard pessoal | - | X | X | X |

---

## 3. Navegação de Vagas (Público)

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-VAGA-01 | Listar vagas abertas | X | X | - | X |
| UC-VAGA-02 | Filtrar vagas por termo de busca | X | X | - | X |
| UC-VAGA-03 | Filtrar vagas por área | X | X | - | X |
| UC-VAGA-04 | Visualizar detalhes de uma vaga | X | X | - | X |

---

## 4. Candidaturas (Estudante)

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-CAND-01 | Candidatar-se a uma vaga | - | X | - | - |
| UC-CAND-02 | Listar minhas candidaturas | - | X | - | - |
| UC-CAND-03 | Cancelar candidatura pendente | - | X | - | - |
| UC-CAND-04 | Visualizar status da candidatura | - | X | - | - |

---

## 5. Curtidas/Favoritos (Estudante)

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-CURT-01 | Curtir/favoritar uma vaga | - | X | - | - |
| UC-CURT-02 | Remover curtida de uma vaga | - | X | - | - |
| UC-CURT-03 | Listar vagas favoritadas | - | X | - | - |

---

## 6. Gerenciamento de Vagas (Recrutador)

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-RECR-01 | Listar minhas vagas publicadas | - | - | X | - |
| UC-RECR-02 | Cadastrar nova vaga de estágio | - | - | X | - |
| UC-RECR-03 | Editar dados de uma vaga | - | - | X | - |
| UC-RECR-04 | Alterar status da vaga (abrir/fechar/suspender) | - | - | X | - |
| UC-RECR-05 | Visualizar candidatos de uma vaga | - | - | X | - |
| UC-RECR-06 | Avaliar candidatura (aprovar/rejeitar) | - | - | X | - |

---

## 7. Chamados de Suporte

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-CHAM-01 | Listar meus chamados | - | X | X | - |
| UC-CHAM-02 | Abrir novo chamado de suporte | - | X | X | - |
| UC-CHAM-03 | Visualizar detalhes do chamado | - | X | X | X |
| UC-CHAM-04 | Responder a um chamado | - | X | X | X |
| UC-CHAM-05 | Excluir chamado (sem resposta) | - | X | X | - |
| UC-CHAM-06 | Listar todos os chamados do sistema | - | - | - | X |
| UC-CHAM-07 | Fechar chamado | - | - | - | X |
| UC-CHAM-08 | Reabrir chamado fechado | - | - | - | X |

---

## 8. Chat/Mensagens

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-CHAT-01 | Listar conversas | - | X | X | X |
| UC-CHAT-02 | Visualizar histórico de mensagens | - | X | X | X |
| UC-CHAT-03 | Enviar mensagem | - | X | X | X |
| UC-CHAT-04 | Buscar usuários para iniciar conversa | - | X | X | X |
| UC-CHAT-05 | Visualizar contador de mensagens não lidas | - | X | X | X |

---

## 9. Administração de Usuários

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-ADMU-01 | Listar todos os usuários | - | - | - | X |
| UC-ADMU-02 | Cadastrar novo usuário | - | - | - | X |
| UC-ADMU-03 | Editar dados de um usuário | - | - | - | X |
| UC-ADMU-04 | Excluir usuário | - | - | - | X |
| UC-ADMU-05 | Alterar perfil/papel de um usuário | - | - | - | X |

---

## 10. Moderação de Vagas (Admin)

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-ADMV-01 | Listar todas as vagas do sistema | - | - | - | X |
| UC-ADMV-02 | Filtrar vagas por status | - | - | - | X |
| UC-ADMV-03 | Aprovar vaga para publicação | - | - | - | X |
| UC-ADMV-04 | Suspender vaga | - | - | - | X |
| UC-ADMV-05 | Excluir vaga (sem candidaturas) | - | - | - | X |

---

## 11. Gerenciamento de Áreas

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-AREA-01 | Listar áreas de atuação | - | - | - | X |
| UC-AREA-02 | Cadastrar nova área | - | - | - | X |
| UC-AREA-03 | Editar área existente | - | - | - | X |
| UC-AREA-04 | Excluir área (sem vagas vinculadas) | - | - | - | X |

---

## 12. Gerenciamento de Curtidas (Admin)

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-ADMC-01 | Listar todas as curtidas do sistema | - | - | - | X |
| UC-ADMC-02 | Cadastrar curtida para usuário | - | - | - | X |
| UC-ADMC-03 | Editar curtida | - | - | - | X |
| UC-ADMC-04 | Remover curtida | - | - | - | X |

---

## 13. Configurações do Sistema

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-CONF-01 | Visualizar configurações do sistema | - | - | - | X |
| UC-CONF-02 | Alterar limites de taxa (rate limiting) | - | - | - | X |
| UC-CONF-03 | Gerenciar cache do sistema | - | - | - | X |
| UC-CONF-04 | Selecionar tema visual do sistema | - | - | - | X |

---

## 14. Backup e Restauração

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-BACK-01 | Listar backups disponíveis | - | - | - | X |
| UC-BACK-02 | Criar backup manual | - | - | - | X |
| UC-BACK-03 | Restaurar backup | - | - | - | X |
| UC-BACK-04 | Baixar arquivo de backup | - | - | - | X |
| UC-BACK-05 | Excluir backup | - | - | - | X |

---

## 15. Auditoria e Logs

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-AUDI-01 | Visualizar logs do sistema | - | - | - | X |
| UC-AUDI-02 | Filtrar logs por data | - | - | - | X |
| UC-AUDI-03 | Filtrar logs por nível (INFO, WARNING, ERROR) | - | - | - | X |

---

## 16. Páginas Públicas

| ID | Caso de Uso | Visitante | Estudante | Recrutador | Administrador |
|----|-------------|:---------:|:---------:|:----------:|:-------------:|
| UC-PUB-01 | Acessar página inicial | X | X | X | X |
| UC-PUB-02 | Acessar página "Sobre" | X | X | X | X |

---

## Resumo por Perfil

### Visitante (4 casos de uso exclusivos + 6 compartilhados)
- Autenticação (login, cadastro, recuperação de senha)
- Navegação pública de vagas
- Páginas institucionais

### Estudante (12 casos de uso exclusivos + compartilhados)
- Gerenciamento de perfil
- Candidaturas a vagas
- Curtidas/favoritos
- Chamados de suporte
- Chat/mensagens

### Recrutador (6 casos de uso exclusivos + compartilhados)
- Gerenciamento de vagas próprias
- Visualização e avaliação de candidatos
- Chamados de suporte
- Chat/mensagens

### Administrador (27 casos de uso exclusivos + compartilhados)
- Gerenciamento completo de usuários
- Moderação de vagas
- Gerenciamento de áreas
- Gerenciamento de curtidas
- Configurações do sistema
- Backup e restauração
- Auditoria e logs
- Chamados de suporte (gestão completa)

---

## Total de Casos de Uso: 67

| Categoria | Quantidade |
|-----------|:----------:|
| Autenticação | 5 |
| Perfil | 5 |
| Vagas Públicas | 4 |
| Candidaturas | 4 |
| Curtidas (Estudante) | 3 |
| Vagas (Recrutador) | 6 |
| Chamados | 8 |
| Chat | 5 |
| Admin - Usuários | 5 |
| Admin - Vagas | 5 |
| Admin - Áreas | 4 |
| Admin - Curtidas | 4 |
| Configurações | 4 |
| Backup | 5 |
| Auditoria | 3 |
| Páginas Públicas | 2 |
| **Total** | **67** |
