from os import mkdir, path
from typing import Literal

from tinydb import TinyDB
from tinydb.storages import MemoryStorage

# Criar diretorio caso não exista
if not path.exists("data"):
    mkdir("data")


def produtos_db(storage: Literal["Memory", None] = None):
    if storage is None:
        return TinyDB("data/produtos.json")

    return TinyDB(storage=MemoryStorage)


def vendas_db(storage: Literal["Memory", None] = None):
    if storage is None:
        return TinyDB("data/vendas.json")

    return TinyDB(storage=MemoryStorage)
