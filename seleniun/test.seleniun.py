from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

navegador = webdriver.Chrome()

navegador.get('https://www.mercadolivre.com.br/')

sleep(5)

# Encontra o elemento <input> pelo ID usando By
elemento = navegador.find_element(By.ID, 'cb1-edit')

elemento.send_keys('Celular')

print(elemento)

# Espera por uma entrada do usuário antes de fechar o navegador
input("Pressione Enter para fechar o navegador...")

# Fecha o navegador
navegador.quit()