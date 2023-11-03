from typing import Literal, TypedDict, Union

from toga import Widget


class StyleDocument(TypedDict):
    """
    Represents the style document of a widget.
    """

    width: int
    height: int

    direction: Literal["row", "column", None]
    alignment: Literal["top", "bottom", "left", "right", "center"]

    flex: int
    padding: int
    padding_top: int
    padding_bottom: int
    padding_left: int
    padding_right: int

    text_align: Literal["left", "center", "right", "justify"]
    text_direction: Literal["ltr", "rtl"]

    font_size: int
    font_weight: Literal["normal", "bold"]
    font_variant: Literal["normal", "small_caps"]


class Style:
    """
    Represents the style of a widget.
    """

    def __init__(
        self,
        widget: Widget,
        document: Union[StyleDocument, None] = None,
    ):
        """
        Initializes the class instance with the given widget and document.

        Parameters:
            widget (Widget): The widget to be initialized.

            document (Union[StyleDocument, None], optional): The document containing
            the style information. Defaults to None.

        Returns:
            None
        """
        # DEFAULTS
        widget.style["font_size"] = "10"

        if document is None:
            return

        if "padding" in document:
            widget.style["padding_top"] = document["padding"]
            widget.style["padding_bottom"] = document["padding"]
            widget.style["padding_left"] = document["padding"]
            widget.style["padding_right"] = document["padding"]
            del document["padding"]

        for attr, value in document.items():
            widget.style[attr] = value
