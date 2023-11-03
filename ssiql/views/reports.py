from datetime import datetime

from ..components import Box, Column, Divider, Label, Row, Selection, Table
from ..views import ViewModel, view_controller


def search_handler(data, search):
    """
    This function takes in a list of data and a search term, and
    filters the data based on the search term.

    Parameters:
        - data (list): A list of dictionaries representing the data to be filtered.
        - search (str): A string representing the search term.

    Returns:
        - filtered_data (list): A list of dictionaries representing the filtered data.
    """
    filtered_data = []
    for item in data:
        temp = {**item}
        del temp["id"]
        for search_term in search.split():
            if (
                search_term.lower() in " ".join(temp.values()).lower()
                and item not in filtered_data
            ):
                filtered_data.append(item)
    return filtered_data


def sales_dates_datasource():
    """
    Retrieve a list of dates from the sales data source.

    Returns:
        list: A list of dates in descending order.

    Raises:
        None
    """
    sales = view_controller.database.sale.list()
    dates = [str(datetime.now()).split()[0]]
    for sale in sales:
        sale_date = sale["occurred_at"].split()[0]
        if sale_date not in dates:
            dates.append(sale_date)
    dates.sort(reverse=True)
    return dates


class ReportsViewModel(ViewModel):
    """
    Represents the view model for the Reports view.
    """

    def __init__(self) -> None:
        self.id = "reports"

        self.select_sales_date: Selection
        self.table_sales_in_date: Table
        self.table_products_in_sale: Table

    def update(self):
        """
        Update the view.
        """

        self.select_sales_date = Selection(
            items=sales_dates_datasource(),
            style={"flex": 1},
            on_select=lambda _: self.on_select_sales_date(),
        )

        self.table_sales_in_date = Table(
            title="Sales",
            headings=["Total Price", "Payment Method", "Customer Name"],
            data_source=self.sales_in_date_datasource,
            filter_source=self.sales_in_date_filter_source,
            style={"flex": 1},
        )

        # Custom on_select event
        self.table_sales_in_date.table().on_select = self.on_select_sale

        self.table_products_in_sale = Table(
            title="Products in Sale",
            headings=["Name", "Brand", "Reference", "Price", "Quantity"],
            data_source=self.products_in_sale_datasource,
            filter_source=self.products_in_sale_filter_source,
            style={"flex": 1},
        )

        sales_by_date_node = Row(
            [
                Box(style={"flex": 3}),
                Row(
                    [Label("Sales by Date"), self.select_sales_date],
                    {"flex": 1},
                ),
            ]
        )

        view_controller.update_main(
            [
                Column(
                    [
                        Label("Reports"),
                        Divider(),
                        sales_by_date_node,
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
        """
        Updates the sales and products tables based on the selected sales date.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        self.table_sales_in_date.update()
        self.table_products_in_sale.update()

    def on_select_sale(self, _, row):
        """
        Sets the selected row in the sales table and updates the products in the sale table.

        Parameters:
            _ (Table): The table object representing the sales table.
            row (int): The index of the selected row.

        Returns:
            None
        """
        self.table_sales_in_date.set_selected(row)
        self.table_products_in_sale.update()

    def sales_in_date_datasource(self):
        """
        Retrieves the sales data from the database for a given date.

        :return: A list of sales data for the selected date.
        """
        selected_date = self.select_sales_date.value
        return view_controller.database.sale.search_by_attribute(
            selected_date, "occurred_at"
        )

    def sales_in_date_filter_source(self, search):
        """
        Retrieves the sales data from the date filter data source and applies a search filter.

        Parameters:
            search (str): The search term to filter the sales data.

        Returns:
            list: A list of sales data matching the search term.
        """
        data = self.sales_in_date_datasource()
        if data is None:
            return []
        return search_handler(data, search)

    def products_in_sale_datasource(self):
        """
        Retrieves the products in the selected sale from the data source.

        Returns:
            A list of products in the selected sale.
        """
        selected_sale = self.table_sales_in_date.selected()
        if selected_sale is None:
            return []
        return selected_sale["products"]

    def products_in_sale_filter_source(self, search):
        """
        Generates a filtered list of products based on the given search string.

        Parameters:
            search (str): The search string to filter the products.

        Returns:
            list: A list of products that match the search string.
        """
        data = self.products_in_sale_datasource()
        if data is None:
            return []
        return search_handler(data, search)


view_controller.register_model(ReportsViewModel())
