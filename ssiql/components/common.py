from typing import Callable, Literal, Optional, Union

import toga

from .style import Style, StyleDocument


class Box(toga.Box):
    """
    A box widget.
    """

    def __init__(
        self,
        children: list[toga.Widget] = [],
        style: StyleDocument = StyleDocument(),
    ):
        """
        Initializes the class with the given parameters.

        Args:
            children (list[toga.Widget], optional): The list of child widgets.
            Defaults to an empty list.

            style (StyleDocument, optional): The style document to apply to
            the widget. Defaults to an empty StyleDocument object.

        Returns:
            None
        """
        super().__init__(children=children)
        Style(self, style)


class Column(Box):
    """
    A column widget.
    """

    def __init__(
        self, children: list[toga.Widget] = [], style: StyleDocument = StyleDocument()
    ):
        """
        Initializes a new instance of the class.

        Parameters:
            children (list[toga.Widget], optional): A list of child widgets.
            Defaults to an empty list.

            style (StyleDocument, optional): The style document for the widget.
            Defaults to an empty StyleDocument object.

        Returns:
            None
        """
        style["direction"] = "column"
        super().__init__(children=children, style=style)


class Row(Box):
    """
    A row widget.
    """

    def __init__(
        self,
        children: list[toga.Widget] = [],
        style: StyleDocument = StyleDocument(),
    ):
        """
        Initializes an instance of the class.

        Args:
            children (list[toga.Widget], optional): A list of child widgets.
            Defaults to [].

            style (StyleDocument, optional): The style document for the widget.
            Defaults to StyleDocument().

        Returns:
            None
        """
        style["direction"] = "row"
        super().__init__(children=children, style=style)


class Divider(toga.Divider):
    """
    A divider widget.
    """

    def __init__(
        self,
        direction: Literal["h", "v"] = "h",
        style: StyleDocument = StyleDocument(padding_top=10, padding_bottom=10),
    ):
        """
        Initializes a new instance of the class.

        Args:
            direction (Literal["h", "v"], optional): The direction of the instance.
            Defaults to "h".

            style (StyleDocument, optional): The style document of the instance.
            Defaults to StyleDocument(padding_top=10, padding_bottom=10).
        """
        m_direction = 0 if direction == "h" else 1
        super().__init__(direction=m_direction)
        Style(self, style)


class Label(toga.Label):
    """
    A label widget.
    """

    def __init__(
        self,
        text: str,
        style: StyleDocument = StyleDocument(),
    ):
        """
        Initializes a new instance of the class.

        Args:
            text (str): The text to be initialized with.

            style (StyleDocument, optional): The style document to be applied.
            Defaults to an instance of StyleDocument.

        Returns:
            None
        """
        super().__init__(text=text)
        Style(self, style)


class NumberInput(toga.NumberInput):
    """
    A number input widget.
    """

    def __init__(
        self,
        value: Union[int, None] = None,
        style: StyleDocument = StyleDocument(),
    ):
        """
        Initializes a new instance of the class.

        Parameters:
            value (Union[int, None], optional): The initial value. Defaults to None.

            style (StyleDocument, optional): The style document. Defaults to StyleDocument().

        Returns:
            None
        """
        super().__init__(value=value)
        Style(self, style)


class TextInput(toga.TextInput):
    """
    A text input widget.
    """

    def __init__(
        self,
        value: Union[str, None] = None,
        on_change=None,
        style: StyleDocument = StyleDocument(),
    ):
        """
        Initializes an instance of the class.

        Args:
            value (Union[str, None], optional): The initial value of the instance.
            Defaults to None.

            on_change (callable, optional): A callback function to be called when the
            value changes. Defaults to None.

            style (StyleDocument, optional): The style document to be applied to the
            instance. Defaults to StyleDocument().

        Returns:
            None
        """
        super().__init__(value=value, on_change=on_change)
        Style(self, style)


class Button(toga.Button):
    """
    A class representing a button widget.
    """

    def __init__(
        self, text: str, on_press=None, style: StyleDocument = StyleDocument()
    ):
        """
        Initializes a new instance of the class.

        Parameters:
            text (str): The text to display on the button.

            on_press (function, optional): A callback function to execute when the button
            is pressed. Defaults to None.

            style (StyleDocument, optional): An instance of the StyleDocument class to customize
            the button's appearance. Defaults to an empty StyleDocument.

        Returns:
            None
        """
        super().__init__(text=text, on_press=on_press)
        Style(self, style)


class Selection(toga.Selection):
    """
    A class representing a selection widget.
    """

    def __init__(
        self,
        items: list[str] = [],
        style: StyleDocument = StyleDocument(),
        on_select: Optional[Callable] = None,
    ):
        """
        Initializes a new instance of the class.

        Args:
            items (list[str], optional): The list of items. Defaults to [].

            style (StyleDocument, optional): The style of the document. Defaults to StyleDocument().

            on_select (Optional[Callable], optional): The callback function to be executed when
            an item is selected. Defaults to None.
        """
        super().__init__(items=items, on_select=on_select)
        Style(self, style)


class MultilineTextInput(toga.MultilineTextInput):
    """
    A class representing a multiline text input widget.
    """

    def __init__(
        self,
        value: Optional[str] = None,
        on_change=None,
        style: StyleDocument = StyleDocument(),
    ):
        """
        Initializes a new instance of the class.

        Parameters:
            value (Optional[str]): The initial value for the instance.
            Defaults to None.

            on_change (Optional[Callable]): A callback function to be called when the value changes.

            style (StyleDocument): The style document to be applied to the instance.
            Defaults to an empty StyleDocument.

        Returns:
            None
        """
        super().__init__(value=value, on_change=on_change)
        Style(self, style)
