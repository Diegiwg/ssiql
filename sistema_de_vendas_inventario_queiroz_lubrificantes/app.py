import toga

from .database import database_api

api = database_api()


class SistemadeVendasInventarioQueirozLubrificantes(toga.App):

    def startup(self):
        main_box = toga.Box()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return SistemadeVendasInventarioQueirozLubrificantes()
