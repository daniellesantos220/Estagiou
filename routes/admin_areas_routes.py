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