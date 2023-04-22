import toga

from .views import (
    product_create,
    product_update,
    products,
    reports,
    sales,
    view_controller,
)


class App(toga.App):
    def startup(self):
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
