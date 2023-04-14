
from enum import Enum
from typing import NotRequired, TypedDict


class MetodoPagamento(Enum):
    DINHEIRO = "DINHEIRO"
    CARTAO = "CARTAO"
    PIX = "PIX"
    PENDURADO = "PENDURADO"


class Produto(TypedDict):
    id: NotRequired[int]
    nome: str
    marca: str
    referencia: NotRequired[str]
    preco: float
    quantidade: int


class Venda(TypedDict):
    id: NotRequired[int]
    ocorreu_em: str
    preco_total: float
    metodo_pagamento: MetodoPagamento
    produtos: list[Produto]
    nome_cliente: NotRequired[str]
