"""
Ainda precisa refatorar antes de lançar o Modulo
"""

from typing import Union

import toga

from ..database.database_api import ProdutoAPI, VendaAPI
from .common import Box, Column, Label, Row, TextInput
from .style import Style, StyleDocument


class Table(Box):
    def __init__(self,
                 headings: list,
                 model,
                 database: Union[VendaAPI, ProdutoAPI],
                 title='',
                 style=StyleDocument()):

        super().__init__(style=style)

        self.__selected = None
        self.__model = model
        self.__database = database

        self.__table = toga.Table(
            headings=headings, data=database.listar(),
            missing_value="", on_select=self.__on_select_handler
        )
        Style(self.__table, {'flex': 1})

        self.__search_input = TextInput(
            value='',
            on_change=self.__on_search_handler,
            style={'flex': 1}
        )

        self.add(
            Column(style={'flex': 1}, children=[
                Row(children=[
                    Label(style={'flex': 3}, text=title),
                    Row(style={'flex': 1}, children=[
                        Label('Buscar'),
                        self.__search_input
                    ])
                ]),
                self.__table
            ])
        )

    def __on_select_handler(self, table, row):
        self.__selected = row

    def __on_search_handler(self, _):
        if self.__search_input.value == '':
            self.__table.data = self.__database.listar()
            return

        m_search = self.__search_input.value.lower()
        self.__table.data = self.__database.buscar(m_search)

    def update(self):
        self.__selected = None
        self.__table.data = []

        # Aplicado para mesmo depois de atualizar, manter o termo de busca
        self.__on_search_handler(None)

    def selected(self):
        if self.__selected is None:
            return None

        m_item: dict = self.__selected.__dict__

        del m_item['_attrs']
        del m_item['_source']

        return self.__model(**m_item)
