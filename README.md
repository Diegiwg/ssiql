# Sistema de Vendas e Inventario - Loja Queiroz Lubrificantes e Auto Peças

## Demonstração do Projeto

<https://user-images.githubusercontent.com/15692310/232661172-8889bc01-2f12-4213-a360-2d2225b23ed8.mp4>

## Descrição do Projeto

O projeto é um sistema com interface simplificada, que abrange o controle de Produtos e Estoque, com as operações de cadastro, listagem, alteração e exclusão de produtos.

Faz parte também do projeto, o sistema de vendas, no qual existe a opção de Nomear o Cliente, seleciona o metodo de pagamento e finalizar a compra.

Por fim, existe a opção de visualizar as vendas que ocorreram em uma determinada data.

### Regras de Uso

O projeto é de origem voluntaria, e está aberto para qualquer um utilizar, modificar, e vender.

## Como Usar

O metodo de uso mais simples é baixar a release mais recente, em [releases](https://github.com/Diegiwg/sistema-de-vendas-inventario-queiroz-lubrificantes/releases).

Caso queira executar a versão de desenvolvimento, basta seguir os seguintes passos:

1. Clonar o repositório: `git clone https://github.com/Diegiwg/sistema-de-vendas-inventario-queiroz-lubrificantes.git`
2. Navegar até o diretorio: `cd sistema-de-vendas-inventario-queiroz-lubrificantes`
3. Executar o comando: `pip install -r requirements-dev.txt`
4. Executar o comando: `briefcase dev`

### Banco de Dados

O Banco de Dados também é simplificado, e utiliza como armazenamento dois arquivos [JSON](https://www.json.org/json-pt.html).

Os arquivos podem ser encontrados em: `~/data/`.

No caso, o `~` representa o diretório do usuario, no windows sendo algo como `C:\Users\User`.

Existem dois arquivos:

- produtos.json -> Armazena os produtos, com suas quantidades em estoque.
- vendas.json -> Armazena as vendas realizadas.

## Requesitos do Projeto

- Sistema para cadastrar e gerenciar produtos
  - Cadastrar produtos
  - Listar produtos
  - Alterar produtos
  - Excluir produtos
  - Modificar a quantidade em estoque

- Sistema para efetuar vendas
  - Cadastrar vendas
  - Listar vendas
