from enum import Enum
from typing import TypedDict


class PaymentMethod(Enum):
    """
    Enum representing the available payment methods.
    """

    CASH = "CASH"
    CARD = "CARD"
    PIX = "PIX"
    ON_CREDIT = "ON_CREDIT"


class Product(TypedDict):
    """
    Represents a product in the database.
    """

    id: int
    name: str
    brand: str
    reference: str
    price: float
    quantity: int


class Sale(TypedDict):
    """
    Represents a sale in the database.
    """

    id: int
    occurred_at: str
    total_price: float
    payment_method: PaymentMethod
    products: list[Product]
    customer_name: str
