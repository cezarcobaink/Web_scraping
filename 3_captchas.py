from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
# Adicione em todos os seus scripts do selenium para evitar que a janela de seleção do navegador padrão apareça: (a partir de agosto de 2024)
opts.add_argument("--disable-search-engine-choice-screen")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

url = 'https://www.google.com/recaptcha/api2/demo'
driver.get(url)

sleep(1)  # Aguarde a página carregar

try:
    # Para interagir com os elementos dentro de um iframe, é necessário mudar para o contexto do iframe
    driver.switch_to.frame(driver.find_element('xpath', '//iframe'))
    sleep(1)  # Aguarde o iframe carregar

    # Agora é possível procurar elementos dentro do iframe e interagir com eles
    captcha = driver.find_element('xpath', '//div[@class="recaptcha-checkbox-border"]')
    captcha.click()
    sleep(1)  # Aguarde o usuário resolver o CAPTCHA

    # O script é pausado para aguardar o usuário pressionar ENTER após resolver o CAPTCHA
    input()

    # Após resolver o CAPTCHA, retornamos o driver para o contexto da página principal
    # Ou seja, saímos do iframe
    driver.switch_to.default_content()
    sleep(1)  # Aguarde antes de clicar no botão de envio

    # Clique no botão de envio
    submit_button = driver.find_element('xpath', '//input[@id="recaptcha-demo-submit"]')
    submit_button.click()
    sleep(1)  # Aguarde o envio ser processado

except Exception as e:
    print(e)

# Se chegar aqui, significa que o CAPTCHA foi resolvido
print("Já estou na página com as informações...")

# Extraia as informações que estavam atrás do CAPTCHA
conteudo = driver.find_element(By.CLASS_NAME, 'recaptcha-success')
print(conteudo.text)
