from re import IGNORECASE
from typing import Literal, Union

from tinydb import TinyDB, where
from tinydb.table import Document

from .database_files import produtos_db, vendas_db
from .database_models import MetodoPagamento, Produto, Venda


def verificar_se_existe_o_mesmo_documento(
    documento: Union[Produto, Venda], banco_dados: TinyDB
):
    if documento.__contains__("id"):
        del documento["id"]

    for item in banco_dados.all():
        resultado_existencia_atributos = []

        for atributo in documento.keys():
            if item[atributo] == documento[atributo]:
                resultado_existencia_atributos.append(True)
            else:
                resultado_existencia_atributos.append(False)

        if all(resultado_existencia_atributos):
            return True

    return False


def adicionar_id_ao_documento(documento: Document):
    return {"id": documento.doc_id, **documento}


class ProdutoAPI:
    def __init__(self, db) -> None:
        self.db = db

    def __dummy__(self):
        return Produto(
            id=0,
            nome="dummy",
            marca="dummy",
            referencia="dummy",
            preco=0.00,
            quantidade=0,
        )

    def listar(self):
        return [
            Produto(**adicionar_id_ao_documento(produto)) for produto in self.db.all()
        ]

    def criar(self, documento: Produto):
        if verificar_se_existe_o_mesmo_documento(documento, self.db):
            return False

        self.db.insert(documento)
        return True

    def excluir(self, id: int):
        self.db.remove(doc_ids=[id])
        return True

    def atualizar(self, id: int, documento: Produto):
        self.db.update(doc_ids=[id], fields=documento)
        return True

    def buscar(self, termos: str):
        m_produtos = self.listar()

        m_produtos_filtrados: list[Produto] = []
        for produto in m_produtos:
            m_produto = {**produto}
            del m_produto["id"]
            del m_produto["preco"]
            del m_produto["quantidade"]

            for termo in termos.split():
                if (
                    termo.lower() in " ".join(m_produto.values()).lower()
                    and produto not in m_produtos_filtrados
                ):
                    m_produtos_filtrados.append(produto)

        return m_produtos_filtrados

    def buscar_por_id(self, id: int):
        produto = self.db.get(doc_id=id)
        if produto is None:
            return None

        return Produto(**adicionar_id_ao_documento(produto))

    def buscar_por_atributo(self, termos: str, atributo: str):
        if atributo.lower() not in self.__dummy__().keys():
            return

        m_produtos_filtrados: list[Produto] = []
        for termo in termos.split():
            m_produtos = self.db.search(
                where(atributo.lower()).search(r"{}".format(termo), IGNORECASE)
            )

            for produto in m_produtos:
                if produto not in m_produtos_filtrados:
                    m_produtos_filtrados.append(
                        Produto(**adicionar_id_ao_documento(produto))
                    )

        return m_produtos_filtrados


class VendaAPI:
    def __init__(self, db) -> None:
        self.db = db

    def __dummy__(self):
        return Venda(
            id=0,
            metodo_pagamento=MetodoPagamento.PENDURADO,
            produtos=[],
            nome_cliente="dummy",
            ocorreu_em="dummy",
            preco_total=0.00,
        )

    def listar(self):
        return [Venda(**adicionar_id_ao_documento(venda)) for venda in self.db.all()]

    def criar(self, documento: Venda):
        if verificar_se_existe_o_mesmo_documento(documento, self.db):
            return False

        self.db.insert(documento)
        return True

    def excluir(self, id: int):
        self.db.remove(doc_ids=[id])
        return True

    def atualizar(self, id: int, documento: Venda):
        self.db.update(doc_ids=[id], fields=documento)
        return True

    def buscar(self, termos: str):
        m_vendas = self.listar()

        m_vendas_filtradas: list[Venda] = []
        for venda in m_vendas:
            m_venda = {**venda}
            del m_venda["id"]

            for termo in termos.split():
                if (
                    termo.lower() in " ".join(m_venda.values()).lower()
                    and venda not in m_vendas_filtradas
                ):
                    m_vendas_filtradas.append(venda)

        return m_vendas_filtradas

    def buscar_por_id(self, id: int):
        venda = self.db.get(doc_id=id)
        if venda is None:
            return None

        return Venda(**adicionar_id_ao_documento(venda))

    def buscar_por_atributo(self, termos: str, atributo: str):
        if atributo.lower() not in self.__dummy__().keys():
            return

        m_vendas_filtradas: list[Venda] = []
        for termo in termos.split():
            m_vendas = self.db.search(
                where(atributo.lower()).search(r"{}".format(termo), IGNORECASE)
            )

            for venda in m_vendas:
                if venda not in m_vendas_filtradas:
                    m_vendas_filtradas.append(Venda(**adicionar_id_ao_documento(venda)))

        return m_vendas_filtradas


class API:
    def __init__(self, storage: Literal["Memory", None] = None) -> None:
        self.produto = ProdutoAPI(produtos_db(storage))

        self.venda = VendaAPI(vendas_db(storage))
