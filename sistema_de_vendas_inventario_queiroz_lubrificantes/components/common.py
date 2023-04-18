from typing import Callable, Literal, Optional, Union

import toga

from .style import Style, StyleDocument


class Box(toga.Box):
    def __init__(
        self, children: list[toga.Widget] = [], style: StyleDocument = StyleDocument()
    ):
        super().__init__(children=children)
        Style(self, style)


class Column(Box):
    def __init__(
        self, children: list[toga.Widget] = [], style: StyleDocument = StyleDocument()
    ):
        style["direction"] = "column"
        super().__init__(children=children, style=style)


class Row(Box):
    def __init__(
        self, children: list[toga.Widget] = [], style: StyleDocument = StyleDocument()
    ):
        style["direction"] = "row"
        super().__init__(children=children, style=style)


class Divider(toga.Divider):
    def __init__(
        self,
        direction: Literal["h", "v"] = "h",
        style: StyleDocument = StyleDocument(padding_top=10, padding_bottom=10),
    ):
        m_direction = 0 if direction == "h" else 1
        super().__init__(direction=m_direction)
        Style(self, style)


class Label(toga.Label):
    def __init__(self, text: str, style: StyleDocument = StyleDocument()):
        super().__init__(text=text)
        Style(self, style)


class NumberInput(toga.NumberInput):
    def __init__(
        self, value: Union[int, None] = None, style: StyleDocument = StyleDocument()
    ):
        super().__init__(value=value)
        Style(self, style)


class TextInput(toga.TextInput):
    def __init__(
        self,
        value: Union[str, None] = None,
        on_change=None,
        style: StyleDocument = StyleDocument(),
    ):
        super().__init__(value=value, on_change=on_change)
        Style(self, style)


class Button(toga.Button):
    def __init__(
        self, text: str, on_press=None, style: StyleDocument = StyleDocument()
    ):
        super().__init__(text=text, on_press=on_press)
        Style(self, style)


class Selection(toga.Selection):
    def __init__(
        self,
        items: list[str] = [],
        style: StyleDocument = StyleDocument(),
        on_select: Optional[Callable] = None,
    ):
        super().__init__(items=items, on_select=on_select)
        Style(self, style)


class MultilineTextInput(toga.MultilineTextInput):
    def __init__(
        self,
        value: Optional[str] = None,
        on_change=None,
        style: StyleDocument = StyleDocument(),
    ):
        super().__init__(value=value, on_change=on_change)
        Style(self, style)
