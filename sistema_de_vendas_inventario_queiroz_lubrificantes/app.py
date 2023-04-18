import toga

from .views import view_controller
from .views.product_create import product_create_model
from .views.product_update import product_update_model
from .views.products import products_model
from .views.reports import reports_model
from .views.sales import sales_model


class App(toga.App):
    def startup(self):
        # Register View Models
        view_controller.register_model(products_model)
        view_controller.register_model(product_create_model)
        view_controller.register_model(product_update_model)
        view_controller.register_model(sales_model)
        view_controller.register_model(reports_model)

        # Main View Model
        view_controller.redirect_to("sales")
        view_controller.update_model()

        # Main Window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = view_controller.main()
        self.main_window.show()

        # Set Full Screen Mode
        self.set_full_screen(self.main_window)


def main():
    return App()
