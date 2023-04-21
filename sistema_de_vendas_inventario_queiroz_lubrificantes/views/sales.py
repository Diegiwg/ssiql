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
from ..database import Produto, Venda
from ..views import ViewModel, view_controller


def search_handle(data: list, search: str):
    m_filtered_data: list = []
    for m_data in data:
        m_temp = {**m_data}
        del m_temp["id"]

        for m_search in search.split():
            if (
                m_search.lower() in m_temp.__str__().lower()
                and m_data not in m_filtered_data
            ):
                m_filtered_data.append(m_data)
    return m_filtered_data


class View(ViewModel):
    def __init__(self) -> None:
        self.id = "sales"

    def update(self):
        self.shopping_cart: list[Produto] = []

        self.table_available_products = Table(
            title="Produtos Disponíveis",
            headings=["Nome", "Marca", "Referencia", "Preco", "Quantidade"],
            data_source=self.available_products_datasource,
            filter_source=self.available_products_filtersource,
            style={"flex": 2},
        )

        self.input_quantity_product_add_cart = NumberInput(
            1, {"flex": 1, "padding_right": 10}
        )

        self.table_products_in_shopping_cart = Table(
            title="Produtos no Carrinho",
            headings=["Nome", "Marca", "Referencia", "Preco", "Quantidade"],
            data_source=self.products_in_shopping_cart_datasource,
            filter_source=self.products_in_shopping_cart_filtersource,
            style={"flex": 2},
        )

        self.input_client_name = TextInput(style={"flex": 1, "padding_right": 10})

        self.select_payment_method = Selection(
            ["DINHEIRO", "CARTAO", "PIX", "PENDURADO"],
            style={"flex": 1, "padding_right": 10},
        )

        self.label_total_value_in_shopping_cart = Label(
            "Valor total da compra: R$ 0.00", style={"flex": 1}
        )

        view_controller.update_main(
            [
                Column(
                    [
                        Label("Vendas"),
                        Divider(),
                        Column(
                            [
                                self.table_available_products,
                                Row(
                                    [
                                        Box(style={"flex": 1}),
                                        Row(
                                            [
                                                Label("Quantidade"),
                                                self.input_quantity_product_add_cart,
                                            ],
                                            {"flex": 1},
                                        ),
                                        Button(
                                            "Adicionar ao Carrinho",
                                            lambda _: self.add_product_to_shopping_cart_handler(),
                                            {"flex": 1},
                                        ),
                                    ],
                                    {"padding_top": 10},
                                ),
                            ],
                            {"flex": 1},
                        ),
                        Divider(),
                        Column(
                            [
                                self.table_products_in_shopping_cart,
                                Row(
                                    [
                                        self.label_total_value_in_shopping_cart,
                                        Button(
                                            "Remover Produto",
                                            lambda _: self.remove_product_from_shopping_cart_handler(),
                                            {"flex": 1, "padding_right": 10},
                                        ),
                                        Button(
                                            "Limpar Carrinho",
                                            lambda _: self.clear_shopping_cart_handler(),
                                            {"flex": 1},
                                        ),
                                    ],
                                    {"padding_top": 10},
                                ),
                                Row(
                                    [
                                        Row(
                                            [
                                                Label("Nome do Cliente"),
                                                self.input_client_name,
                                            ],
                                            {"flex": 1},
                                        ),
                                        Row(
                                            [
                                                Label("Método de Pagamento"),
                                                self.select_payment_method,
                                            ],
                                            {"flex": 1},
                                        ),
                                        Button(
                                            "Finalizar Compra",
                                            lambda _: self.finalize_sale_handler(),
                                            {"flex": 1},
                                        ),
                                    ],
                                    {"padding_top": 10},
                                ),
                            ],
                            {"flex": 1},
                        ),
                    ],
                    {"flex": 1},
                )
            ]
        )

    def tables_update(self):
        self.table_available_products.update()
        self.table_products_in_shopping_cart.update()

        # Atualizar o valor total da compra
        if self.shopping_cart:
            m_total_value = float(
                sum(
                    [
                        product["preco"] * product["quantidade"]
                        for product in self.shopping_cart
                    ]
                )
            )
        else:
            m_total_value = 0.00
        self.label_total_value_in_shopping_cart.text = (
            f"Valor total da compra: R$ {m_total_value:.2f}"
        )

    def available_products_datasource(self):
        m_products = view_controller.database.produto.listar()
        return [
            product
            for product in m_products
            if product["quantidade"] > 0
            and "id" in product
            and f"'id': {product['id']}" not in self.shopping_cart.__str__()
        ]

    def available_products_filtersource(self, search: str):
        m_products: list[Produto] = search_handle(
            self.available_products_datasource(), search
        )
        return m_products

    def products_in_shopping_cart_datasource(self):
        return self.shopping_cart

    def products_in_shopping_cart_filtersource(self, search: str):
        m_products: list[Produto] = search_handle(self.shopping_cart, search)
        return m_products

    def clear_shopping_cart_handler(self):
        self.shopping_cart = []
        self.tables_update()

    def add_product_to_shopping_cart_handler(self):
        m_product = self.table_available_products.selected()
        m_quantity = self.input_quantity_product_add_cart.value
        if (
            not m_product
            or m_quantity is None
            or m_quantity <= 0
            or m_quantity > m_product["quantidade"]
        ):
            return

        m_product["quantidade"] = int(m_quantity)

        self.shopping_cart.append(Produto(**m_product))
        self.input_quantity_product_add_cart.value = 1
        self.tables_update()

    def remove_product_from_shopping_cart_handler(self):
        m_product = self.table_products_in_shopping_cart.selected()
        if not m_product:
            return

        self.shopping_cart.remove(Produto(**m_product))
        self.tables_update()

    def finalize_sale_handler(self):
        if not self.shopping_cart:
            return

        for product in self.shopping_cart:
            if "id" not in product:
                continue

            m_product = view_controller.database.produto.buscar_por_id(product["id"])
            if not m_product:
                continue

            m_product["quantidade"] -= product["quantidade"]

            view_controller.database.produto.atualizar(product["id"], m_product)

        m_total_price = [
            product["preco"] * product["quantidade"] for product in self.shopping_cart
        ]

        m_sale: Venda = {
            "metodo_pagamento": self.select_payment_method.value,
            "ocorreu_em": str(datetime.now()),
            "preco_total": float(sum(m_total_price)),
            "nome_cliente": self.input_client_name.value,
            "produtos": self.shopping_cart,
        }
        view_controller.database.venda.criar(m_sale)

        self.input_client_name.value = ""
        self.shopping_cart = []
        self.tables_update()


sales_model = View()
