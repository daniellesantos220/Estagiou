from fastapi import Request
from typing import Literal

TipoMensagem = Literal["sucesso", "erro", "aviso", "info"]

def adicionar_mensagem(
    request: Request,
    mensagem: str,
    tipo: TipoMensagem = "info"
):
    """Adiciona mensagem flash à sessão"""
    if "mensagens" not in request.session:
        request.session["mensagens"] = []

    request.session["mensagens"].append({
        "texto": mensagem,
        "tipo": tipo
    })

def informar_sucesso(request: Request, mensagem: str):
    adicionar_mensagem(request, mensagem, "sucesso")

def informar_erro(request: Request, mensagem: str):
    adicionar_mensagem(request, mensagem, "erro")

def informar_aviso(request: Request, mensagem: str):
    adicionar_mensagem(request, mensagem, "aviso")

def informar_info(request: Request, mensagem: str):
    adicionar_mensagem(request, mensagem, "info")

def obter_mensagens(request: Request) -> list:
    """Obtém e limpa mensagens da sessão"""
    mensagens = request.session.pop("mensagens", [])
    return mensagens
