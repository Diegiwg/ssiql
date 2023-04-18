"""
Ainda precisa refatorar antes de lançar o Modulo
"""

from typing import Callable

import toga

from .common import Box, Column, Label, Row, TextInput
from .style import Style, StyleDocument


class Table(Box):
    def __init__(
        self,
        headings: list,
        data_source: Callable,
        filter_source: Callable,
        title="",
        style=StyleDocument(),
    ):
        super().__init__(style=style)

        self.__selected = None
        self.__data_source = data_source
        self.__filter_source = filter_source

        self.__table = toga.Table(
            headings=headings,
            data=data_source(),
            missing_value="",
            on_select=self.__on_select_handler,
        )
        Style(self.__table, {"flex": 1})

        self.__search_input = TextInput(
            value="", on_change=self.__on_search_handler, style={"flex": 1}
        )

        self.add(
            Column(
                style={"flex": 1},
                children=[
                    Row(
                        children=[
                            Label(style={"flex": 3}, text=title),
                            Row(
                                style={"flex": 1},
                                children=[Label("Buscar"), self.__search_input],
                            ),
                        ]
                    ),
                    self.__table,
                ],
            )
        )

    def __on_select_handler(self, table, row):
        self.__selected = row

    def __on_search_handler(self, _):
        if self.__search_input.value == "":
            self.__table.data = self.__data_source()
            return

        m_search: str = self.__search_input.value.lower()
        self.__table.data = self.__filter_source(m_search)

    def update(self):
        self.__selected = None
        self.__table.data = []

        # Aplicado para mesmo depois de atualizar, manter o termo de busca
        self.__on_search_handler(None)

    def selected(self):
        if self.__selected is None:
            return None

        m_item: dict = self.__selected.__dict__

        try:
            del m_item["_attrs"]
            del m_item["_source"]
        except:  # noqa: E722
            pass  # Não tem atributos

        return m_item

    def table(self):
        return self.__table

    def set_selected(self, row):
        self.__selected = row
