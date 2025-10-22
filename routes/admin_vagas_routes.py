#Aprovação de Vaga

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

#Arqui