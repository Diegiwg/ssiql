from ..components import Button, Column, Divider, Label, Row, Table
from ..views import ViewModel, view_controller


class ProductViewModel(ViewModel):
    """
    Represents the model for the products view.
    """

    def __init__(self) -> None:
        self.id = "products"

        self.product_table: Table

    def update(self):
        """
        Update the View
        """

        table_headings = ["Name", "Brand", "Reference", "Price", "Quantity"]

        self.product_table = Table(
            headings=table_headings,
            data_source=view_controller.database.product.list,
            filter_source=view_controller.database.product.search,
            style={"flex": 1},
        )

        create_product_btn = Button(
            "Create Product",
            lambda _: view_controller.redirect_to("product_create"),
            {"flex": 1, "padding_right": 10},
        )

        update_product_btn = Button(
            "Update Product",
            lambda _: self.product_update_handle(),
            {"flex": 1, "padding_right": 10},
        )

        delete_product_btn = Button(
            "Delete Product",
            lambda _: self.product_delete_handle(),
            {"flex": 1},
        )

        view_controller.update_main(
            [
                Column(
                    [
                        Label("Products"),
                        Divider(),
                        self.product_table,
                        Divider(),
                        Row(
                            [create_product_btn, update_product_btn, delete_product_btn]
                        ),
                    ],
                    {"flex": 1},
                )
            ]
        )

    def product_delete_handle(self):
        """
        Delete a product from the database.

        This function deletes a selected product from the database. It first checks if a product is selected and if it has an "id" field. If not, it returns without performing any action. If a valid product is selected, it calls the delete method from the product table in the database, passing the "id" of the selected product. After deleting the product, it updates the product table.
        """
        selected_product = self.product_table.selected()
        if not selected_product or "id" not in selected_product:
            return

        view_controller.database.product.delete(selected_product["id"])
        self.product_table.update()

    def product_update_handle(self):
        """
        Updates the product in the database based on the selected product.
        """
        selected_product = self.product_table.selected()
        if not selected_product:
            return

        view_controller.redirect_to("product_update", selected_product)


view_controller.register_model(ProductViewModel())
