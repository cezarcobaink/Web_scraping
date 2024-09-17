from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class LoginSpider(Spider):
    name = 'GitHubLogin'
    start_urls = ['https://github.com/login']

    def __init__(self, *args, **kwargs):
        super(LoginSpider, self).__init__(*args, **kwargs)
        # Configura o Selenium WebDriver para usar o Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=400,800')
        self.driver = webdriver.Chrome(options=options)

    def parse(self, response):
        # Abre a página de login do GitHub
        self.driver.get('https://github.com/login')
        time.sleep(10)  # Espera 10 segundos para carregar a página

        # Insere o nome de usuário
        username_input = self.driver.find_element(By.ID, 'login_field')
        username_input.send_keys('cezarcobaink')
        time.sleep(10)  # Espera 10 segundos

        # Insere a senha
        password_input = self.driver.find_element(By.ID, 'password')
        password_input.send_keys(open('./password.txt').readline().strip())
        time.sleep(10)  # Espera 10 segundos

        # Submete o formulário de login
        password_input.send_keys(Keys.RETURN)
        time.sleep(10)  # Espera 10 segundos para o login ser processado

        # Navega para a página de repositórios do usuário
        self.driver.get('https://github.com/cezarcobaink?tab=repositories')
        time.sleep(10)  # Espera 10 segundos para carregar a página

        # Obtém o HTML da página e passa para o Scrapy
        response = Selector(text=self.driver.page_source)
        self.parse_repositorios(response)

    def parse_repositorios(self, response):
        # Seleciona os repositórios na página e imprime seus nomes
        repositorios = response.xpath('//h3[@class="wb-break-all"]/a/text()')
        for repositorio in repositorios:
            print(repositorio.get())

# Configura o processo de crawling
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'DOWNLOAD_DELAY': 1,
    'ROBOTSTXT_OBEY': True,
})

# Inicia o processo de crawling
process.crawl(LoginSpider)
process.start()