Ótimo! Segue abaixo o README atualizado:

# Sistema de Vendas e Inventario - Loja Queiroz Lubrificantes e Auto Peças

## Demonstração do Projeto

<https://user-images.githubusercontent.com/15692310/232661172-8889bc01-2f12-4213-a360-2d2225b23ed8.mp4>

## Descrição do Projeto

O projeto é um sistema com interface simplificada, que abrange o controle de Produtos e Estoque, com as operações de cadastro, listagem, alteração e exclusão de produtos. Faz parte também do projeto, o sistema de vendas, no qual existe a opção de Nomear o Cliente, selecionar o método de pagamento e finalizar a compra. Por fim, existe a opção de visualizar as vendas que ocorreram em uma determinada data.

## Como Usar

> Observação: No momento, a release só está disponível para Windows, mas é possível executar em Linux com o clone do projeto.

O método de uso mais simples é baixar a release mais recente, em [releases](https://github.com/Diegiwg/sistema-de-vendas-inventario-queiroz-lubrificantes/releases).

Caso queira executar a versão de desenvolvimento, basta seguir os seguintes passos:

1. Clonar o repositório: `git clone https://github.com/Diegiwg/sistema-de-vendas-inventario-queiroz-lubrificantes.git`
2. Navegar até o diretório: `cd sistema-de-vendas-inventario-queiroz-lubrificantes`
3. Executar o comando: `pip install -r requirements-dev.txt`
4. Executar o comando: `briefcase dev`

### Banco de Dados

O banco de dados é gerado automaticamente e utiliza dois arquivos [JSON](https://www.json.org/json-pt.html) como armazenamento, que podem ser encontrados em: `~/data/`.

No momento, temos apenas releases para Windows, mas na versão de desenvolvimento, é possível executar em Linux.

### Funções Disponíveis

- Cadastro de produtos
- Listagem de produtos
- Alteração de produtos
- Exclusão de produtos
- Modificação da quantidade em estoque
- Cadastro de vendas
- Listagem de vendas

## Licença

Este projeto é licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Desenvolvedor

- Diego Queiroz - [@Diegiwg](https://github.com/Diegiwg)

## Contribuições

Contribuições são bem-vindas! Para contribuir, faça um fork do repositório, crie um novo branch e envie um pull request com suas alterações.
