from typing import Literal

from .database_api import API
from .database_models import MetodoPagamento, Produto, Venda  # noqa: F401


def database_api(storage: Literal['Memory', None] = None):
    return API(storage)
