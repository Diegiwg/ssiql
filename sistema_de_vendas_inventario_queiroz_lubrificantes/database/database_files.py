import os
from typing import Literal

from tinydb import TinyDB
from tinydb.storages import MemoryStorage

# Criar diretorio caso não exista
if not os.path.exists(os.path.expanduser("~/datas")):
    os.mkdir(os.path.expanduser("~/datas"))


def produtos_db(storage: Literal["Memory", None] = None):
    if storage is None:
        return TinyDB(os.path.expanduser("~/data/produtos.json"))

    return TinyDB(storage=MemoryStorage)


def vendas_db(storage: Literal["Memory", None] = None):
    if storage is None:
        return TinyDB(os.path.expanduser("~/data/vendas.json"))

    return TinyDB(storage=MemoryStorage)
