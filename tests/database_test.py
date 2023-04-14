from datetime import datetime

from tinydb import TinyDB

from sistema_de_vendas_inventario_queiroz_lubrificantes.database import (
    API,
    MetodoPagamento,
    Produto,
    Venda,
    database_api,
    database_files,
)


def dummy_produto(nome: str = "dummy", marca: str = "dummy",
                  referencia: str = "dummy", preco: float = 0.00, quantidade: int = 0):
    return Produto(
        nome=nome,
        marca=marca,
        referencia=referencia,
        preco=preco,
        quantidade=quantidade
    )


def dummy_cadastro_produto(api: API):
    api.produto.criar(dummy_produto(nome="Madeira Fina"))
    api.produto.criar(dummy_produto(marca="Madeira"))
    api.produto.criar(dummy_produto(referencia="Madeira Grossa"))
    api.produto.criar(dummy_produto(preco=10.00))
    api.produto.criar(dummy_produto(quantidade=10))


def dummy_venda(product_difference: int = 0):
    return Venda(
        produtos=[dummy_produto(quantidade=product_difference)],
        metodo_pagamento=MetodoPagamento.PENDURADO,
        ocorreu_em=str(datetime.now()),
        preco_total=0.0,
    )


def testar_se_os_arquivos_de_db_foram_criados():
    assert isinstance(database_files.produtos_db('Memory'), TinyDB)
    assert isinstance(database_files.vendas_db('Memory'), TinyDB)


def testar_se_e_possivel_criar_um_produto():
    api = database_api('Memory')

    assert api.produto.criar(dummy_produto()) is True


def testar_se_e_possivel_criar_um_produto_duplicado():
    api = database_api('Memory')

    m_produto = dummy_produto()

    api.produto.criar(m_produto)  # Criando o primeiro Produto
    assert api.produto.criar(m_produto) is False


def testar_se_e_possivel_atualizar_produto():
    api = database_api('Memory')

    api.produto.criar(dummy_produto())
    api.produto.atualizar(1, dummy_produto(nome="Novo Nome"))
    assert api.produto.buscar_por_id(1) == {
        'id': 1, **dummy_produto(nome="Novo Nome")
    }


def testar_se_e_possivel_excluir_produto():
    api = database_api('Memory')

    dummy_cadastro_produto(api)
    assert api.produto.excluir(1) is True


def testar_se_e_possivel_listar_produtos():
    api = database_api('Memory')

    for index in range(10):
        api.produto.criar(dummy_produto(quantidade=index))

    assert len(api.produto.listar()) == 10


def testar_se_funciona_buscar_produtos_por_id():
    api = database_api('Memory')

    for index in range(10):
        api.produto.criar(dummy_produto(quantidade=index))

    assert api.produto.buscar_por_id(3) is not None


def testar_se_funciona_buscar_produtos_por_todos_os_atributos():
    api = database_api('Memory')

    dummy_cadastro_produto(api)
    assert len(api.produto.buscar("Madeira")) == 3


def testar_se_funciona_buscar_produtos_por_atributo_inexistente():
    api = database_api('Memory')

    api.produto.criar(dummy_produto())

    assert api.produto.buscar_por_atributo(
        atributo="dummy", termos="dummy"
    ) is None


def testar_se_funciona_buscar_produtos_por_nome():
    api = database_api('Memory')

    dummy_cadastro_produto(api)
    m_produtos = api.produto.buscar_por_atributo(
        atributo="nome", termos="madeira"
    )
    assert m_produtos is not None and len(m_produtos) == 1


def testar_se_funciona_buscar_produtos_por_marca():
    api = database_api('Memory')

    dummy_cadastro_produto(api)
    m_produtos = api.produto.buscar_por_atributo(
        atributo="Marca", termos="madeira"
    )
    assert m_produtos is not None and len(m_produtos) == 1


def testar_se_funciona_buscar_produtos_por_referencia():
    api = database_api('Memory')

    dummy_cadastro_produto(api)
    m_produtos = api.produto.buscar_por_atributo(
        atributo="Referencia", termos="madeira"
    )
    assert m_produtos is not None and len(m_produtos) == 1


def testar_se_funciona_buscar_produtos_por_preco():
    api = database_api('Memory')

    dummy_cadastro_produto(api)
    m_produtos = api.produto.buscar_por_atributo(
        atributo="Preco", termos="10.00"
    )
    assert m_produtos is not None and len(m_produtos) == 0


def testar_se_funciona_buscar_produtos_por_quantidade():
    api = database_api('Memory')

    dummy_cadastro_produto(api)
    m_produtos = api.produto.buscar_por_atributo(
        atributo="Quantidade", termos="10"
    )
    assert m_produtos is not None and len(m_produtos) == 0


def testar_se_e_possivel_criar_venda():
    api = database_api('Memory')

    assert api.venda.criar(dummy_venda()) is True


def testar_se_e_possivel_criar_venda_duplicada():
    api = database_api('Memory')

    m_venda = dummy_venda()

    api.venda.criar(m_venda)  # Criando o primeiro Produto
    assert api.venda.criar(m_venda) is False


def testar_se_e_possivel_listar_vendas():
    api = database_api('Memory')

    for index in range(10):
        api.venda.criar(dummy_venda(index))

    assert len(api.venda.listar()) == 10
