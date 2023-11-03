from typing import TypedDict

from ..components import Button, Column, Divider, Label, Row, TextInput
from ..database import Product
from ..views import ViewModel, view_controller


class ProductForm(TypedDict):
    """
    Represents the form for creating a new product.
    """

    name: TextInput
    brand: TextInput
    reference: TextInput
    price: TextInput
    quantity: TextInput


def create_handle(form: ProductForm):
    """
    Create a new product in the database.
    """
    if (
        form["name"].value == ""
        or form["brand"].value == ""
        or form["reference"].value == ""
        or form["price"].value == ""
        or form["quantity"].value == ""
    ):
        return

    # Try to convert the price
    price: float
    try:
        price = float(form["price"].value.replace(",", "."))
    except ValueError:
        return

    # Try to convert the quantity
    quantity: int
    try:
        quantity = int(form["quantity"].value)
    except ValueError:
        return

    # Create and add the new product to the database
    new_product = Product(
        name=form["name"].value,
        brand=form["brand"].value,
        reference=form["reference"].value,
        price=price,
        quantity=quantity,
    )

    view_controller.database.product.create(new_product)
    view_controller.redirect_to_previous()


class Model(ViewModel):
    """
    Represents the model for the product create view.
    """

    def __init__(self) -> None:
        self.id = "product_create"

    def update(self):
        """
        Update the View
        """

        form = ProductForm(
            name=TextInput(style={"flex": 2}),
            brand=TextInput(style={"flex": 2}),
            reference=TextInput(style={"flex": 2}),
            price=TextInput(style={"flex": 2}),
            quantity=TextInput(style={"flex": 2}),
        )

        label_name = Label("Name", {"flex": 1})
        label_brand = Label("Brand", {"flex": 1})
        label_reference = Label("Reference", {"flex": 1})
        label_price = Label("Price", {"flex": 1})
        label_quantity = Label("Quantity", {"flex": 1})

        create_product_btn = Button(
            "Create Product",
            lambda _: create_handle(form),
            {"flex": 1},
        )

        cancel_action_btn = Button(
            "Cancel",
            lambda _: view_controller.redirect_to_previous(),
            {"flex": 1},
        )

        view_controller.update_main(
            [
                Column(
                    [
                        Label("Create Product"),
                        Divider(),
                        Row([label_name, form["name"]], {"flex": 1}),
                        Row([label_brand, form["brand"]], {"flex": 1}),
                        Row([label_reference, form["reference"]], {"flex": 1}),
                        Row([label_price, form["price"]], {"flex": 1}),
                        Row([label_quantity, form["quantity"]], {"flex": 1}),
                        Divider(),
                        Row([create_product_btn, cancel_action_btn], {"flex": 1}),
                    ],
                    {"flex": 1},
                )
            ]
        )


view_controller.register_model(Model())
