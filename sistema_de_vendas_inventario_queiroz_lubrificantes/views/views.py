from typing import Callable

from ..components import Box, Button, Column, Divider, Row
from ..database import API


class ViewModel:
    id: str
    update: Callable


class ViewController:
    def __init__(self, database: API) -> None:
        self.database = database

        self.__models: dict[str, ViewModel] = {}
        self.__navegation: list[ViewModel] = []

        self.__main_part1 = Column(
            [
                Button("Vendas", lambda _: self.redirect_to("sales")),
                Button("Produtos", lambda _: self.redirect_to("products")),
                Button("Relatórios", lambda _: self.redirect_to("reports")),
            ],
            style={"flex": 1},
        )
        self.__main_part2 = Box()
        self.__main = Row(
            [
                self.__main_part1,
                Divider("v", {"padding_left": 10, "padding_right": 10}),
                self.__main_part2,
            ],
            {"flex": 1, "padding": 10},
        )

    def main(self):
        return self.__main

    def update_main(self, widgets: list):
        self.__main.remove(self.__main_part2)
        self.__main_part2 = Column(widgets, {"flex": 6})
        self.__main.add(self.__main_part2)

    def register_model(self, model: ViewModel):
        self.__models[model.id] = model

    def update_model(self, custom_data=None):
        if not self.__navegation:
            return

        m_model = self.__navegation[-1]

        if custom_data:
            m_model.update(custom_data)
        else:
            m_model.update()

    def redirect_to(self, model_id: str, custom_data=None):
        if model_id not in self.__models:
            return

        if self.__navegation and model_id == self.__navegation[-1].id:
            return

        if len(self.__navegation) > 50:
            self.__navegation = self.__navegation[25:]

        self.__navegation.append(self.__models[model_id])
        self.update_model(custom_data)

    def redirect_to_previous(self):
        if not self.__navegation:
            return

        self.__navegation.pop()
        self.update_model()
