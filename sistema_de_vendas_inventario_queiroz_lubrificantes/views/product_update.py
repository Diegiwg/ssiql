from typing import TypedDict

from ..components import Button, Column, Divider, Label, Row, TextInput
from ..database import Produto
from ..views import ViewModel, view_controller


class ProductForm(TypedDict):
    nome: TextInput
    marca: TextInput
    referencia: TextInput
    preco: TextInput
    quantidade: TextInput


def update_handle(product_id: int, form: ProductForm):
    if (
        form["nome"].value == ""
        or form["marca"].value == ""
        or form["referencia"].value == ""
        or form["preco"].value == ""
        or form["quantidade"].value == ""
    ):
        return

    # Tentar converter preco
    m_preco = form["preco"].value.replace(",", ".")
    try:
        m_preco = float(m_preco)
    except ValueError:
        return

    # Tentar converter quantidade
    m_quantidade = form["quantidade"].value
    if not m_quantidade.isdigit():
        return
    else:
        m_quantidade = int(m_quantidade)

    view_controller.database.produto.atualizar(
        product_id,
        Produto(
            nome=form["nome"].value,
            marca=form["marca"].value,
            referencia=form["referencia"].value,
            preco=m_preco,
            quantidade=m_quantidade,
        ),
    )

    view_controller.redirect_to_previous()


class Model(ViewModel):
    def __init__(self) -> None:
        self.id = "product_update"

    def update(self, product: Produto):
        if "id" not in product:
            product["id"] = 0
            view_controller.redirect_to_previous()

        m_form = ProductForm(
            nome=TextInput(style={"flex": 2}),
            marca=TextInput(style={"flex": 2}),
            referencia=TextInput(style={"flex": 2}),
            preco=TextInput(style={"flex": 2}),
            quantidade=TextInput(style={"flex": 2}),
        )

        m_form["nome"].value = product["nome"]
        m_form["marca"].value = product["marca"]
        m_form["preco"].value = str(product["preco"])
        m_form["quantidade"].value = str(product["quantidade"])
        if "referencia" in product:
            m_form["referencia"].value = product["referencia"]

        m_lnome = Label("Nome", {"flex": 1})
        m_lmarca = Label("Marca", {"flex": 1})
        m_lreferencia = Label("Referencia", {"flex": 1})
        m_lpreco = Label("Preco", {"flex": 1})
        m_lquantidade = Label("Quantidade", {"flex": 1})

        view_controller.update_main(
            [
                Column(
                    [
                        Label("Criar Produto"),
                        Divider(),
                        Row([m_lnome, m_form["nome"]], {"flex": 1}),
                        Row([m_lmarca, m_form["marca"]], {"flex": 1}),
                        Row([m_lreferencia, m_form["referencia"]], {"flex": 1}),
                        Row([m_lpreco, m_form["preco"]], {"flex": 1}),
                        Row([m_lquantidade, m_form["quantidade"]], {"flex": 1}),
                        Divider(),
                        Row(
                            [
                                Button(
                                    "Atualizar Produto",
                                    lambda _: update_handle(product["id"], m_form),
                                    {"flex": 1},
                                ),
                                Button(
                                    "Cancelar",
                                    lambda _: view_controller.redirect_to_previous(),
                                    {"flex": 1},
                                ),
                            ],
                            {"flex": 1},
                        ),
                    ],
                    {"flex": 1},
                )
            ]
        )


view_controller.register_model(Model())
