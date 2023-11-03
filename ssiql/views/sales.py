from datetime import datetime

from ..components import (
    Box,
    Button,
    Column,
    Divider,
    Label,
    NumberInput,
    Row,
    Selection,
    Table,
    TextInput,
)
from ..database import Product, Sale
from ..views import ViewModel, view_controller


def search_handler(data, search, *del_keys):
    """
    Search through the given data based on the provided search
    terms and filter out any unwanted keys.
    """
    filtered_data = []
    for item in data:
        temp = {**item}
        del temp["id"]

        for key in del_keys:
            del temp[key]

        for search_term in search.split():
            if (
                search_term.lower() in " ".join(temp.values()).lower()
                and item not in filtered_data
            ):
                filtered_data.append(item)
    return filtered_data


class SalesViewModel(ViewModel):
    """
    Represents the view model for the sales view.
    """

    def __init__(self) -> None:
        self.id = "sales"

        self.shopping_cart: list[Product]
        self.table_available_products: Table
        self.input_quantity_product_add_cart: NumberInput
        self.table_products_in_shopping_cart: Table
        self.select_payment_method: Selection
        self.input_client_name: TextInput
        self.button_add_to_cart: Button
        self.label_total_value_in_shopping_cart: Label

    def update(self):
        """
        Update the View
        """

        self.shopping_cart: list[Product] = []

        self.table_available_products = Table(
            title="Available Products",
            headings=["Name", "Brand", "Reference", "Price", "Quantity"],
            data_source=self.available_products_datasource,
            filter_source=self.available_products_filter_source,
            style={"flex": 2},
        )

        self.input_quantity_product_add_cart = NumberInput(
            1, {"flex": 1, "padding_right": 10}
        )

        self.table_products_in_shopping_cart = Table(
            title="Products in Shopping Cart",
            headings=["Name", "Brand", "Reference", "Price", "Quantity"],
            data_source=self.products_in_shopping_cart_datasource,
            filter_source=self.products_in_shopping_cart_filter_source,
            style={"flex": 2},
        )

        self.input_client_name = TextInput(style={"flex": 1, "padding_right": 10})

        self.select_payment_method = Selection(
            ["CASH", "CARD", "PIX", "CREDIT"],
            style={"flex": 1, "padding_right": 10},
        )

        self.label_total_value_in_shopping_cart = Label(
            "Total Purchase Value: $0.00", style={"flex": 1}
        )

        row_add_to_cart = Row(
            [
                Box(style={"flex": 1}),
                Row(
                    [
                        Label("Quantity"),
                        self.input_quantity_product_add_cart,
                    ],
                    {"flex": 1},
                ),
                Button(
                    "Add to Cart",
                    lambda _: self.add_product_to_shopping_cart_handler(),
                    {"flex": 1},
                ),
            ],
            {"padding_top": 10},
        )

        row_1 = Row(
            [
                self.label_total_value_in_shopping_cart,
                Button(
                    "Remove Product",
                    lambda _: self.remove_product_from_shopping_cart_handler(),
                    {"flex": 1, "padding_right": 10},
                ),
                Button(
                    "Clear Cart",
                    lambda _: self.clear_shopping_cart_handler(),
                    {"flex": 1},
                ),
            ],
            {"padding_top": 10},
        )

        row_2 = Row(
            [
                Row(
                    [
                        Label("Customer Name"),
                        self.input_client_name,
                    ],
                    {"flex": 1},
                ),
                Row(
                    [
                        Label("Payment Method"),
                        self.select_payment_method,
                    ],
                    {"flex": 1},
                ),
                Button(
                    "Complete Sale",
                    lambda _: self.finalize_sale_handler(),
                    {"flex": 1},
                ),
            ],
            {"padding_top": 10},
        )

        view_controller.update_main(
            [
                Column(
                    [
                        Label("Sales"),
                        Divider(),
                        Column(
                            [self.table_available_products, row_add_to_cart],
                            {"flex": 1},
                        ),
                        Divider(),
                        Column(
                            [self.table_products_in_shopping_cart, row_1, row_2],
                            {"flex": 1},
                        ),
                    ],
                    {"flex": 1},
                )
            ]
        )

    def tables_update(self):
        """
        Updates the tables for available products and products in the shopping cart.
        """
        self.table_available_products.update()
        self.table_products_in_shopping_cart.update()

        # Update the total purchase value
        if self.shopping_cart:
            total_value = float(
                sum(
                    [
                        product["price"] * product["quantity"]
                        for product in self.shopping_cart
                    ]
                )
            )
        else:
            total_value = 0.00
        self.label_total_value_in_shopping_cart.text = (
            f"Total Purchase Value: ${total_value:.2f}"
        )

    def available_products_datasource(self):
        """
        Returns a list of available products from the datasource.
        """
        products = view_controller.database.product.list()
        return [
            product
            for product in products
            if product["quantity"] > 0
            and "id" in product
            and f"'id': {product['id']}" not in str(self.shopping_cart)
        ]

    def available_products_filter_source(self, search: str):
        """
        Filter the available products based on the search query.
        """
        products = search_handler(
            self.available_products_datasource(),
            search,
            "reference",
            "price",
            "quantity",
        )
        return products

    def products_in_shopping_cart_datasource(self):
        """
        Returns the shopping cart datasource.
        """
        return self.shopping_cart

    def products_in_shopping_cart_filter_source(self, search: str):
        """
        Filters the products in the shopping cart based on the provided search term.
        """
        products = search_handler(
            self.shopping_cart, search, "reference", "price", "quantity"
        )
        return products

    def clear_shopping_cart_handler(self):
        """
        Clears the shopping cart by resetting the self.shopping_cart attribute to an empty list.
        """
        self.shopping_cart = []
        self.tables_update()

    def add_product_to_shopping_cart_handler(self):
        """
        Adds a selected product to the shopping cart.
        """
        product = self.table_available_products.selected()
        quantity = self.input_quantity_product_add_cart.value
        if (
            not product
            or quantity is None
            or quantity <= 0
            or quantity > product["quantity"]
        ):
            return

        product["quantity"] = int(quantity)

        self.shopping_cart.append(Product(**product))
        self.input_quantity_product_add_cart.value = 1
        self.tables_update()

    def remove_product_from_shopping_cart_handler(self):
        """
        Removes a product from the shopping cart.
        """
        product = self.table_products_in_shopping_cart.selected()
        if not product:
            return

        self.shopping_cart.remove(Product(**product))
        self.tables_update()

    def finalize_sale_handler(self):
        """
        Finalizes a sale by updating the product quantities, creating a sale record,
        and resetting the shopping cart.
        """
        if not self.shopping_cart:
            return

        for product in self.shopping_cart:
            if "id" not in product:
                continue

            stored_product = view_controller.database.product.search_by_id(
                product["id"]
            )
            if not stored_product:
                continue

            stored_product["quantity"] -= product["quantity"]

            view_controller.database.product.update(product["id"], stored_product)

        total_price = [
            product["price"] * product["quantity"] for product in self.shopping_cart
        ]

        sale = Sale(
            payment_method=self.select_payment_method.value,
            occurred_at=str(datetime.now()),
            total_price=float(sum(total_price)),
            customer_name=self.input_client_name.value,
            products=self.shopping_cart,
        )
        view_controller.database.sale.create(sale)

        self.input_client_name.value = ""
        self.shopping_cart = []
        self.tables_update()


view_controller.register_model(SalesViewModel())
