from re import IGNORECASE
from typing import Literal, Union

from tinydb import TinyDB, where
from tinydb.table import Document

from .database_files import products_db, sales_db
from .database_models import PaymentMethod, Product, Sale


def check_if_document_exists(
    document: Union[Product, Sale],
    database: TinyDB,
):
    """
    Checks if a document exists in the specified database.

    Parameters:
        document (Union[Product, Sale]): The document to check for existence.

        database (TinyDB): The database to search in.

    Returns:
        bool: True if the document exists in the database, False otherwise.
    """
    if "id" in document:
        del document["id"]

    for item in database.all():
        attribute_existence_result = []

        for attribute in document.keys():
            if item[attribute] == document[attribute]:
                attribute_existence_result.append(True)
            else:
                attribute_existence_result.append(False)

        if all(attribute_existence_result):
            return True

    return False


def add_id_to_document(document: Document):
    """
    Adds an "id" field to the given document and returns the modified document.

    Args:
        document (Document): The document object to which the "id" field will be added.

    Returns:
        dict: The modified document with the "id" field added.
    """
    return {"id": document.doc_id, **document}


class ProductManager:
    """
    The ProductManager class provides methods for managing products in a database.
    """

    def __init__(self, db) -> None:
        self.db = db

    def __dummy__(self):
        return Product(
            id=0,
            name="dummy",
            brand="dummy",
            reference="dummy",
            price=0.00,
            quantity=0,
        )

    def list(self) -> list[Product]:
        """
        Returns a list of `Product` objects.

        :return: A list of `Product` objects.
        :type: list[Product]
        """
        return [Product(**add_id_to_document(product)) for product in self.db.all()]

    def create(self, document: Product) -> bool:
        """
        Create a new document in the database.

        Args:
            document (Product): The document to be created.

        Returns:
            bool: True if the document was successfully created, False otherwise.
        """
        if check_if_document_exists(document, self.db):
            return False
        self.db.insert(document)
        return True

    def delete(self, id: int) -> Literal[True]:
        """
        Delete a record from the database.

        Args:
            id (int): The ID of the record to be deleted.

        Returns:
            Literal[True]: Returns True if the record was successfully deleted.
        """
        self.db.remove(doc_ids=[id])
        return True

    def update(self, id: int, document: Product) -> Literal[True]:
        """
        Update a document in the database.

        Args:
            id (int): The ID of the document to be updated.
            document (Product): The updated document.

        Returns:
            Literal[True]: True if the update was successful.
        """
        self.db.update(doc_ids=[id], fields=document)
        return True

    def search(self, terms: str):
        """
        Search for products based on the given terms.

        Args:
            terms (str): The terms used to filter the products.

        Returns:
            list: A list of filtered products.
        """
        products = self.list()
        filtered_products = []

        for product in products:
            product_info = {**product}
            del product_info["id"]
            del product_info["price"]
            del product_info["quantity"]

            for term in terms.split():
                if (
                    term.lower() in " ".join(product_info.values()).lower()
                    and product not in filtered_products
                ):
                    filtered_products.append(product)

        return filtered_products

    def search_by_id(self, product_id: int):
        """
        Retrieves a product from the database based on its ID.

        Args:
            product_id (int): The ID of the product to search for.

        Returns:
            Product or None: The retrieved product as a `Product` instance if found, or `None` if not found.
        """
        product = self.db.get(doc_id=product_id)
        if product is None:
            return None

        return Product(**add_id_to_document(product))

    def search_by_attribute(self, terms: str, attribute: str):
        """
        Search for products in the database by a given attribute.

        Args:
            terms (str): The search terms to be used.
            attribute (str): The attribute to search by.

        Returns:
            list: A list of filtered products matching the search criteria.
        """
        if attribute.lower() not in self.__dummy__().keys():
            return

        filtered_products = []
        for term in terms.split():
            products = self.db.search(
                where(attribute.lower()).search(r"{}".format(term), IGNORECASE)
            )

            for product in products:
                if product not in filtered_products:
                    filtered_products.append(Product(**add_id_to_document(product)))

        return filtered_products


class SaleManager:
    """
    The SaleManager class provides methods for managing sales in a database.
    """

    def __init__(self, db):
        self.db = db

    def __dummy__(self):
        return Sale(
            id=0,
            payment_method=PaymentMethod.ON_CREDIT,
            products=[],
            customer_name="dummy",
            occurred_at="dummy",
            total_price=0.00,
        )

    def list(self) -> list[Sale]:
        """
        Returns a list of Sale objects.

        :return: A list of Sale objects.
        :rtype: list[Sale]
        """
        return [Sale(**add_id_to_document(sale)) for sale in self.db.all()]

    def create(self, document: Sale):
        """
        Creates a new sale document in the database.

        Parameters:
            document (Sale): The sale document to be created.

        Returns:
            bool: True if the document was successfully created, False otherwise.
        """
        if check_if_document_exists(document, self.db):
            return False

        self.db.insert(document)
        return True

    def delete(self, id: int):
        """
        Deletes a record from the database with the given ID.

        Args:
            id (int): The ID of the record to be deleted.

        Returns:
            bool: True if the record was successfully deleted, False otherwise.
        """
        self.db.remove(doc_ids=[id])
        return True

    def update(self, id: int, document: Sale):
        self.db.update(doc_ids=[id], fields=document)
        return True

    def search(self, terms: str):
        sales = self.list()

        filtered_sales = []
        for sale in sales:
            sale_info = {**sale}
            del sale_info["id"]

            for term in terms.split():
                if (
                    term.lower() in " ".join(sale_info.values()).lower()
                    and sale not in filtered_sales
                ):
                    filtered_sales.append(sale)

        return filtered_sales

    def search_by_id(self, id: int):
        """
        Search the database for a document with the given id and return the corresponding Sale object.

        Args:
            id (int): The id of the document to search for.

        Returns:
            Sale or None: The Sale object corresponding to the document if found, None otherwise.
        """
        sale = self.db.get(doc_id=id)
        if sale is None:
            return None

        return Sale(**add_id_to_document(sale))

    def search_by_attribute(self, terms: str, attribute: str):
        """
        Search for sales by a given attribute and terms.

        Args:
            terms (str): The search terms to look for.
            attribute (str): The attribute to search for.

        Returns:
            List[dict]: A list of filtered sales.

        """
        if attribute.lower() not in self.__dummy__().keys():
            return

        filtered_sales = []
        for term in terms.split():
            sales = self.db.search(
                where(attribute.lower()).search(r"{}".format(term), IGNORECASE)
            )

            for sale in sales:
                if sale not in filtered_sales:
                    filtered_sales.append(Sale(**add_id_to_document(sale)))

        return filtered_sales


class DatabaseManager:
    def __init__(self, storage: Literal["Memory", None] = None) -> None:
        self.product = ProductManager(products_db(storage))
        self.sale = SaleManager(sales_db(storage))
