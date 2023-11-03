from typing import Callable

import toga

from .common import Box, Column, Label, Row, TextInput
from .style import Style, StyleDocument


class Table(Box):
    """
    Represents a table widget.
    """

    def __init__(
        self,
        headings: list,
        data_source: Callable,
        filter_source: Callable,
        title="",
        style=StyleDocument(),
    ):
        """
        Initializes an instance of the class.

        Parameters:
            headings (list): A list of column headings for the table.

            data_source (Callable): A callable that returns the data for the table.

            filter_source (Callable): A callable that filters the data for the table.

            title (str, optional): The title of the table. Defaults to an empty string.

            style (StyleDocument, optional): The style document for the table.
            Defaults to StyleDocument().

        Returns:
            None
        """
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

        search_input_row = Row(
            style={"flex": 1}, children=[Label("Search"), self.__search_input]
        )

        table_and_search_row = Row(
            children=[Label(style={"flex": 3}, text=title), search_input_row]
        )

        self.add(
            Column(style={"flex": 1}, children=[table_and_search_row, self.__table])
        )

    def __on_select_handler(self, _, row):
        """
        Set the value of the __selected attribute to the given row.
        """
        self.__selected = row

    def __on_search_handler(self, _):
        """
        Handles the search event.
        """
        if self.__search_input.value == "":
            self.__table.data = self.__data_source()
            return

        m_search: str = self.__search_input.value.lower()
        self.__table.data = self.__filter_source(m_search)

    def update(self):
        """
        Update the state of the object.

        This function resets the selected item and clears the data in the table.
        It also triggers the search handler to maintain the search term after the update.
        """
        self.__selected = None
        self.__table.data = []

        self.__on_search_handler(None)

    def selected(self):
        """
        Returns the selected item as a dictionary, excluding the "_attrs" and "_source" attributes.
        """
        if self.__selected is None:
            return None

        m_item: dict = self.__selected.__dict__

        try:
            del m_item["_attrs"]
            del m_item["_source"]
        except KeyError:
            pass

        return m_item

    def table(self):
        """
        Returns the value of the private attribute __table.
        """
        return self.__table

    def set_selected(self, row):
        """
        Set the selected row.
        """
        self.__selected = row
