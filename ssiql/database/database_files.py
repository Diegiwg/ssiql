import os
from typing import Literal

from tinydb import TinyDB
from tinydb.storages import MemoryStorage

# Create a directory if it doesn't exist
if not os.path.exists(os.path.expanduser("~/data")):
    os.mkdir(os.path.expanduser("~/data"))


def products_db(storage: Literal["Memory", None] = None) -> TinyDB:
    """
    Initializes a TinyDB instance for the products database.

    Args:
        storage (Literal["Memory", None], optional): The storage type for the database.
        Defaults to None.

    Returns:
        TinyDB: The initialized TinyDB instance.

    Raises:
        None
    """
    if storage is None:
        return TinyDB(os.path.expanduser("~/data/products.json"))
    return TinyDB(storage=MemoryStorage)


def sales_db(storage: Literal["Memory", None] = None) -> TinyDB:
    """
    Initializes and returns a TinyDB instance for the sales database.

    Args:
        storage (Literal["Memory", None], optional): The storage option for the database.
            Defaults to None, which indicates a file-based storage.

    Returns:
        TinyDB: A TinyDB instance for the sales database.
    """
    if storage is None:
        return TinyDB(os.path.expanduser("~/data/sales.json"))
    return TinyDB(storage=MemoryStorage)
