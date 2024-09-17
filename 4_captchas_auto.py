from selenium import webdriver
from time import sleep
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

# Configurações do Selenium WebDriver
opts = Options()
opts.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
opts.add_argument("--window-size=400,800")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

url = 'https://www.google.com/recaptcha/api2/demo'
driver.get(url)

try:
    # Obtém o identificador único do captcha
    captcha_key = driver.find_element(By.ID, 'recaptcha-demo').get_attribute('data-sitekey')

    # Substitua pela sua chave de API do 2Captcha
    api_key = "SUA_CHAVE_DE_API_AQUI"
    
    # Monta a requisição para o 2captcha
    url = f"https://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={captcha_key}&pageurl={url}&json=0"

    print(url)  # Visualiza a URL

    # Faz uma requisição GET com o requests para a URL da API do 2captcha
    resposta_requerimento = requests.get(url)
    captcha_service_key = resposta_requerimento.text

    print(captcha_service_key)
    # Faz o parse da resposta para obter o ID que nosso captcha tem no sistema do 2CAPTCHA
    if "OK|" in captcha_service_key:
        captcha_service_key = captcha_service_key.split('|')[-1]
    else:
        raise Exception("Erro ao obter o ID do captcha: " + captcha_service_key)

    # Monta a requisição para consultar se o captcha já foi resolvido
    url_resp = f"https://2captcha.com/res.php?key={api_key}&action=get&id={captcha_service_key}&json=0"

    print(url_resp)

    # Espera 10 segundos, conforme instruções
    sleep(10)

    # Entra em um loop para consultar o status do captcha até que esteja resolvido
    while True:
        resposta_solver = requests.get(url_resp)
        resposta_solver = resposta_solver.text
        print(resposta_solver)
        # Se o captcha não estiver pronto, espera 5 segundos, itera novamente no loop e pergunta novamente
        if resposta_solver == "CAPCHA_NOT_READY":
            sleep(5)
        # Caso contrário, o captcha está resolvido e pode sair do loop
        else:
            break

    # Obtém a solução do captcha que o 2CAPTCHA API retornou
    if "OK|" in resposta_solver:
        resposta_solver = resposta_solver.split('|')[-1]
    else:
        raise Exception("Erro ao resolver o captcha: " + resposta_solver)

    # Usa o script da documentação deles para inserir a solução na página da web
    insertar_solucion = f'document.getElementById("g-recaptcha-response").innerHTML="{resposta_solver}";'
    print(insertar_solucion)

    # Executa o script com o selenium
    driver.execute_script(insertar_solucion)

    # Clica no botão de submit e deve avançar
    submit_button = driver.find_element(By.XPATH, '//input[@id="recaptcha-demo-submit"]')
    submit_button.click()
except NoSuchElementException as e:
    print(f"Erro ao encontrar elemento: {e}")
except Exception as e:
    print(e)
finally:
    # Lógica após resolver o captcha ou se o captcha não existir
    print("Devo estar na página onde estão as informações...")

    try:
        # Extrai as informações após o captcha
        conteudo = driver.find_element(By.CLASS_NAME, 'recaptcha-success')
        print(conteudo.text)
    except NoSuchElementException:
        print("Elemento 'recaptcha-success' não encontrado.")
    finally:
        driver.quit()