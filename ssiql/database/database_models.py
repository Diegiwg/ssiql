from enum import Enum
from typing import List, NotRequired, TypedDict


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

    id: NotRequired[int]
    name: str
    brand: str
    reference: NotRequired[str]
    price: float
    quantity: int


class Sale(TypedDict):
    """
    Represents a sale in the database.
    """

    id: NotRequired[int]
    occurred_at: str
    total_price: float
    payment_method: PaymentMethod
    products: List[Product]
    customer_name: str
