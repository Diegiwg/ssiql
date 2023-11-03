import toga

from .views import view_controller


class App(toga.App):
    """
    Main application class.
    """
    def startup(self):
        """
        Initializes the application and sets up the main view model, 
        the main window, and the full screen mode.
        """
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
    """
    Initializes and returns an instance of the `App` class.
    """
    return App()
