from typing import Literal, NotRequired, TypedDict, Union

from toga import Widget


class StyleDocument(TypedDict):
    width: NotRequired[int]
    height: NotRequired[int]

    direction: NotRequired[Literal['row', 'column', None]]
    alignment: NotRequired[Literal['top', 'bottom', 'left', 'right', 'center']]

    flex: NotRequired[int]
    padding: NotRequired[int]
    padding_top: NotRequired[int]
    padding_bottom: NotRequired[int]
    padding_left: NotRequired[int]
    padding_right: NotRequired[int]

    text_align: NotRequired[Literal['left', 'center', 'right', 'justify']]
    text_direction: NotRequired[Literal['ltr', 'rtl']]

    font_size: NotRequired[int]
    font_weight: NotRequired[Literal['normal', 'bold']]
    font_variant: NotRequired[Literal['normal', 'small_caps']]


class Style:
    def __init__(self, widget: Widget, document: Union[StyleDocument, None] = None):
        # DEFAULTS
        widget.style['font_size'] = '10'

        if document is None:
            return

        if 'padding' in document:
            widget.style['padding_top'] = document['padding']
            widget.style['padding_bottom'] = document['padding']
            widget.style['padding_left'] = document['padding']
            widget.style['padding_right'] = document['padding']
            del document['padding']

        for atributo, valor in document.items():
            widget.style[atributo] = valor
