# - Objetivo:  Encontrar produtos do Mercado Livre a partir de uma busca realizada pelo usuário
# - Objetivo: Encontrar productos de Mercado Libre a partir de una búsqueda realizada por el usuario    
# - Objective: Find Mercado Livre products from a search made by the user
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://lista.mercadolivre.com.br/'

# Solicita ao usuário o produto para pesquisa
produto_nome = input('Qual produto para pesquisa?')

# Faz a requisição HTTP para a página de busca do Mercado Livre
response = requests.get(url + produto_nome)

# Cria um objeto BeautifulSoup para analisar o conteúdo HTML da página
site = BeautifulSoup(response.text, 'html.parser')

# Encontra todos os elementos div que possuem a classe específica dos produtos
produtos = site.findAll('div', attrs={'class' : 'andes-card ui-search-result ui-search-result--core andes-card--flat andes-card--padding-16'})

# Inicializa uma lista para armazenar os dados dos produtos
lista_produtos = []

# Itera sobre cada produto encontrado
for produto in produtos:
    # Encontra o título do produto
    titulo = produto.find('h2', attrs={'class' : 'ui-search-item__title'})
    # Encontra o link do produto
    link = produto.find('a', attrs={'class' : 'ui-search-item__group__element ui-search-link__title-card ui-search-link'})
    # Encontra o preço em reais do produto
    real = produto.find('span', attrs={'class' : 'andes-money-amount__fraction'})
    # Encontra o preço em centavos do produto
    centavo = produto.find('span', attrs={'class' : 'andes-money-amount__cents andes-money-amount__cents--superscript-16'})

    # Verifica se todos os elementos foram encontrados antes de tentar acessá-los
    if titulo and link and real:
        titulo_text = titulo.text if titulo else 'N/A'
        link_href = link['href'] if link else 'N/A'
        preco_real = real.text if real else 'N/A'
        preco_centavo = centavo.text if centavo else '00'

        # Adiciona as informações do produto à lista
        lista_produtos.append({
            'Titulo': titulo_text,
            'Preço': 'R$' + preco_real + ',' + preco_centavo,
            'Link': link_href
        })

# Cria um DataFrame a partir da lista de produtos
df = pd.DataFrame(lista_produtos)

# Salva o DataFrame em um arquivo Excel
df.to_excel('Obtendo_busca_usuario.xlsx', index=False)

print('Dados salvos em Obtendo_busca_usuario.xlsx')