from ..components import Box, Column, Divider, Label, Row, Selection, Table
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


def sales_dates_datasource():
    m_sales = view_controller.database.venda.listar()
    m_dates: list[str] = []
    for sale in m_sales:
        m_date = sale["ocorreu_em"].split()[0]
        if m_date not in m_dates:
            m_dates.append(m_date)
    return m_dates


class View(ViewModel):
    def __init__(self) -> None:
        self.id = "reports"

    def update(self):
        self.select_sales_date = Selection(
            items=sales_dates_datasource(),
            style={"flex": 1},
            on_select=lambda _: self.on_select_sales_date(),
        )

        self.table_sales_in_date = Table(
            title="Vendas",
            headings=["preco_total", "metodo_pagamento", "nome_cliente"],
            data_source=self.sales_in_date_datasource,
            filter_source=self.sales_in_date_filtersource,
            style={"flex": 1},
        )

        # Custom on_select event
        self.table_sales_in_date.table().on_select = self.on_select_sale

        self.table_products_in_sale = Table(
            title="Produtos da Venda",
            headings=["Nome", "Marca", "Referencia", "Preco", "Quantidade"],
            data_source=self.products_in_sale_datasource,
            filter_source=self.products_in_sale_filtersource,
            style={"flex": 1},
        )

        view_controller.update_main(
            [
                Column(
                    [
                        Label("Relatorios"),
                        Divider(),
                        Row(
                            [
                                Box(style={"flex": 3}),
                                Row(
                                    [Label("Vendas por data"), self.select_sales_date],
                                    {"flex": 1},
                                ),
                            ]
                        ),
                        Divider(),
                        self.table_sales_in_date,
                        Divider(),
                        self.table_products_in_sale,
                    ],
                    {"flex": 1},
                )
            ]
        )

    def on_select_sales_date(self):
        self.table_sales_in_date.update()
        self.table_products_in_sale.update()

    def on_select_sale(self, table, row):
        self.table_sales_in_date.set_selected(row)
        self.table_products_in_sale.update()

    def sales_in_date_datasource(self):
        m_date = self.select_sales_date.value
        return view_controller.database.venda.buscar_por_atributo(m_date, "ocorreu_em")

    def sales_in_date_filtersource(self, search: str):
        data = self.sales_in_date_datasource()
        if data is None:
            return

        return search_handle(data, search)

    def products_in_sale_datasource(self):
        m_products = self.table_sales_in_date.selected()
        if m_products is None:
            return []

        return m_products["produtos"]

    def products_in_sale_filtersource(self, search: str):
        m_data = self.products_in_sale_datasource()
        if m_data is None:
            return []

        return search_handle(m_data, search)


reports_model = View()
