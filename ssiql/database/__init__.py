from typing import Literal

from .database_api import DatabaseManager
from .database_models import PaymentMethod, Product, Sale  # noqa: F401


def db_manager(storage: Literal["Memory", None] = None) -> DatabaseManager:
    """
    Initializes a new instance of the database manager.

    Parameters:
        storage (Literal['Memory', None], optional): The type of storage to use for the database.
        Defaults to None.

    Returns:
        API: An instance of the database manager.
    """
    return DatabaseManager(storage)
