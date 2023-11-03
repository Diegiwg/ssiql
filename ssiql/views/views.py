from typing import Callable

from ..components import Box, Button, Column, Divider, Row
from ..database import DatabaseManager


class ViewModel:
    id: str
    update: Callable


class ViewController:
    def __init__(self, database: DatabaseManager) -> None:
        self.database = database

        self.models: dict[str, ViewModel] = {}
        self.navigation: list[ViewModel] = []

        self.main_part1 = Column(
            [
                Button("Sales", lambda _: self.redirect_to("sales")),
                Button("Products", lambda _: self.redirect_to("products")),
                Button("Reports", lambda _: self.redirect_to("reports")),
            ],
            style={"flex": 1},
        )

        self.main_part2 = Box()

        self.main_part0 = Row(
            [
                self.main_part1,
                Divider("v", {"padding_left": 10, "padding_right": 10}),
                self.main_part2,
            ],
            {"flex": 1, "padding": 10},
        )

    def main(self):
        return self.main_part0

    def update_main(self, widgets: list):
        self.main_part0.remove(self.main_part2)
        self.main_part2 = Column(widgets, {"flex": 6})
        self.main_part0.add(self.main_part2)

    def register_model(self, model: ViewModel):
        self.models[model.id] = model

    def update_model(self, custom_data=None):
        if not self.navigation:
            return

        current_model = self.navigation[-1]

        if custom_data:
            current_model.update(custom_data)
        else:
            current_model.update()

    def redirect_to(self, model_id: str, custom_data=None):
        if model_id not in self.models:
            return

        if self.navigation and model_id == self.navigation[-1].id:
            return

        if len(self.navigation) > 50:
            self.navigation = self.navigation[25:]

        self.navigation.append(self.models[model_id])
        self.update_model(custom_data)

    def redirect_to_previous(self):
        if not self.navigation:
            return

        self.navigation.pop()
        self.update_model()
