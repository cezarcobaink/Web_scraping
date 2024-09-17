import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep

options = Options()
# options.add_argument('headless')
options.add_argument('window-size=400,800')

navegador = webdriver.Chrome(options=options)

navegador.get('https://www.airbnb.com')

# Espera até que o elemento "Qualquer lugar" esteja presente no DOM e clique nele
qualquer_lugar = WebDriverWait(navegador, 30).until(
    EC.element_to_be_clickable((By.XPATH, '//span[text()="Qualquer lugar"]'))
)
qualquer_lugar.click()

# Espera 20 segundos para garantir que a página carregue completamente
sleep(20)

# Espera até que o campo de entrada de busca esteja presente no DOM e esteja clicável
input_place = WebDriverWait(navegador, 30).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[data-testid="search_query_input"]'))
)

# Envia o texto "São Paulo" para o campo de entrada e pressiona Enter imediatamente
input_place.send_keys('São Paulo' + Keys.ENTER)

# Espera 20 segundos para garantir que a página carregue completamente
sleep(20)

# Espera até que o botão "Próximo" esteja presente e clicável
proximo_botao = WebDriverWait(navegador, 30).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="dates-footer-primary-btn"]'))
)
proximo_botao.click()

# Espera 20 segundos para garantir que a página carregue completamente
sleep(20)

# Espera até que o botão "Buscar" esteja presente e clicável
buscar_botao = WebDriverWait(navegador, 30).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="explore-footer-primary-btn"]'))
)
buscar_botao.click()

# Espera 20 segundos para garantir que a página carregue completamente
sleep(20)

# Obtém o conteúdo da página
page_content = navegador.page_source

# Analisa o conteúdo da página com BeautifulSoup
site = BeautifulSoup(page_content, 'html.parser')

# Encontra todos os elementos de hospedagem
hospedagens = site.find_all('div', attrs={'itemprop': 'itemListElement'})

# Lista para armazenar os dados
dados_hospedagens = []

# Verifica se encontrou hospedagens
if not hospedagens:
    print("Nenhuma hospedagem encontrada.")
else:
    # Itera sobre cada hospedagem e extrai os dados
    for hospedagem in hospedagens:

        # Encontra os elementos de descrição, URL e preço da hospedagem        
        hospedagem_descricao = hospedagem.find('meta', attrs={'itemprop': 'name'})
        hospedagem_url = hospedagem.find('meta', attrs={'itemprop': 'url'})
        hospedagem_preco = hospedagem.find('span', attrs={'class': '_11jcbg2'})

        descricao_texto = hospedagem_descricao['content'] if hospedagem_descricao else 'Descrição não encontrada'
        url_texto = hospedagem_url['content'] if hospedagem_url else 'URL não encontrada'
        preco_texto = hospedagem_preco.get_text().strip() if hospedagem_preco else 'Preço não encontrado'

        # Adiciona os dados à lista
        dados_hospedagens.append({
            'Descrição': descricao_texto,
            'Preço': preco_texto,
            'URL': url_texto
        })

        print('Descrição:', descricao_texto)
        print('Preço:', preco_texto)
        print('URL:', url_texto)
        print('-' * 40)  # Adiciona uma linha separadora entre as hospedagens

# Cria um DataFrame a partir dos dados
df = pd.DataFrame(dados_hospedagens)

# Salva o DataFrame em um arquivo Excel
df.to_excel('seleniun/hospedagens.xlsx', index=False)

print("Dados salvos em hospedagens.xlsx")

# Espera por uma entrada do usuário antes de fechar o navegador
input("Pressione Enter para fechar o navegador...")

# Fecha o navegador
navegador.quit()