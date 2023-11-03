from datetime import datetime

from tinydb import TinyDB

from ssiql.database import (
    DatabaseManager,
    PaymentMethod,
    Product,
    Sale,
    database_files,
    db_manager,
)


def dummy_product(
    name="dummy", brand="dummy", reference="dummy", price=0.00, quantity=0
):
    """
    Create a dummy product with the given parameters.
    """
    return Product(
        name=name,
        brand=brand,
        reference=reference,
        price=price,
        quantity=quantity,
    )


def dummy_product_registration(api: DatabaseManager):
    """
    Registers dummy products in the database.
    """
    api.product.create(dummy_product(name="Fine Wood"))
    api.product.create(dummy_product(brand="Wood"))
    api.product.create(dummy_product(reference="Coarse Wood"))
    api.product.create(dummy_product(price=10.00))
    api.product.create(dummy_product(quantity=10))


def dummy_sale(product_difference: int = 0):
    """
    Create a dummy sale transaction.
    """
    return Sale(
        payment_method=PaymentMethod.ON_CREDIT,
        total_price=10.00,
        occurred_at=str(datetime.now()),
        customer_name="dummy",
        products=[
            dummy_product(quantity=product_difference),
        ],
    )


def test_if_db_files_were_created():
    """
    Check if the database files for products and sales were created.
    """
    assert isinstance(database_files.products_db("Memory"), TinyDB)
    assert isinstance(database_files.sales_db("Memory"), TinyDB)


def test_if_product_can_be_created():
    """
    Check if a product can be created.
    """
    api = db_manager("Memory")
    assert api.product.create(dummy_product()) is True


def test_if_duplicate_product_cannot_be_created():
    """
    Test to check if a duplicate product cannot be created.
    """
    api = db_manager("Memory")

    product = dummy_product()
    api.product.create(product)  # Create the first product
    assert api.product.create(product) is False


def test_if_product_can_be_updated():
    """
    Check if a product can be updated successfully.
    """
    api = db_manager("Memory")

    api.product.create(dummy_product())
    api.product.update(1, dummy_product(name="New Name"))
    assert api.product.search_by_id(1) == {"id": 1, **dummy_product(name="New Name")}


def test_if_product_can_be_deleted():
    """
    Test if a product can be deleted.
    """
    api = db_manager("Memory")

    dummy_product_registration(api)
    assert api.product.delete(1) is True


def test_if_products_can_be_listed():
    """
    Test if products can be listed.
    """
    api = db_manager("Memory")

    for index in range(10):
        api.product.create(dummy_product(quantity=index))
    assert len(api.product.list()) == 10


def test_if_getting_product_by_id_works():
    """
    Test if getting a product by ID works.
    """
    api = db_manager("Memory")

    for index in range(10):
        api.product.create(dummy_product(quantity=index))
    assert api.product.search_by_id(3) is not None


def test_if_searching_products_by_all_attributes_works():
    """
    Test if searching products by all attributes works.
    """
    api = db_manager("Memory")

    dummy_product_registration(api)
    assert len(api.product.search("Wood")) == 3


def test_if_searching_products_by_nonexistent_attribute_fails():
    """
    Test if searching products by a nonexistent attribute fails.
    """
    api = db_manager("Memory")

    api.product.create(dummy_product())
    assert api.product.search_by_attribute(attribute="dummy", terms="dummy") is None


def test_if_searching_products_by_name_works():
    """
    Tests if searching products by name works.
    """
    api = db_manager("Memory")

    dummy_product_registration(api)
    products = api.product.search_by_attribute(attribute="name", terms="Wood")
    assert products is not None and len(products) == 1


def test_if_searching_products_by_brand_works():
    """
    Test if searching products by brand works.
    """
    api = db_manager("Memory")

    dummy_product_registration(api)
    products = api.product.search_by_attribute(attribute="brand", terms="Wood")
    assert products is not None and len(products) == 1


def test_if_searching_products_by_reference_works():
    """
    Tests if searching products by reference works.
    """
    api = db_manager("Memory")

    dummy_product_registration(api)
    products = api.product.search_by_attribute(attribute="reference", terms="Wood")
    assert products is not None and len(products) == 1


def test_if_searching_products_by_price_works():
    """
    Test if searching products by price works.
    """
    api = db_manager("Memory")

    dummy_product_registration(api)
    products = api.product.search_by_attribute(attribute="price", terms="10.00")
    assert products is not None and len(products) == 0


def test_if_searching_products_by_quantity_works():
    """
    Test if searching products by quantity works.
    """
    api = db_manager("Memory")

    dummy_product_registration(api)
    products = api.product.search_by_attribute(attribute="quantity", terms="10")
    assert products is not None and len(products) == 0


def test_if_sale_can_be_created():
    """
    Test if a sale can be created.
    """
    api = db_manager("Memory")

    assert api.sale.create(dummy_sale()) is True


def test_if_duplicate_sale_cannot_be_created():
    """
    Tests if a duplicate sale cannot be created.
    """
    api = db_manager("Memory")

    sale = dummy_sale()
    api.sale.create(sale)  # Create the first sale
    assert api.sale.create(sale) is False


def test_if_sales_can_be_listed():
    """
    Test if sales can be listed.
    """
    api = db_manager("Memory")

    for index in range(10):
        api.sale.create(dummy_sale(index))
    assert len(api.sale.list()) == 10
