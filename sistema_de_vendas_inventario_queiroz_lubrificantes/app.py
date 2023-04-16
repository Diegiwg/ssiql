import toga

from .components import Column


class App(toga.App):

    def startup(self):

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = Column()
        self.main_window.show()


def main():
    return App()
