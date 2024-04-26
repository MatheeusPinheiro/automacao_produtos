# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

# Importação das opções do navegador
from botcity.web.browsers.chrome import default_options

# Atualizar o chromedriver automaticamente
from webdriver_manager.chrome import ChromeDriverManager


import pandas as pd

class Bot(WebBot):

    produtos = pd.read_excel('buscas.xlsx')

    def procurar_google_shopping(self, produto, termos_banidos, preco_minimo, preco_maximo):
        # Tratar os valores que vieram da tabela
        produto = produto.lower()
        termos_banidos = termos_banidos.lower()
        lista_termos_banidos = termos_banidos.split(" ")
        lista_termos_produto = produto.split(" ")
        preco_maximo = float(preco_maximo)
        preco_minimo = float(preco_minimo)

        # Pesquisar o produto no google
        self.find_element('//*[@id="APjFqb"]', By.XPATH).send_keys(str(produto)) 
        self.wait(1000)
        self.enter()

        # Clicar na aba shopping
        menus_google = self.find_element('crJ18e', By.CLASS_NAME)        
        if menus_google: 
            shopping_link = menus_google.find_element(By.LINK_TEXT, 'Shopping')
            if shopping_link:
                shopping_link.click()

        self.wait(2000)

        #Armazena a lista de ofertas 
        lista_ofertas = []

        # Pegar a lista de resultados da busca no google shopping
        lista_resultados = self.find_elements('i0X6df', By.CLASS_NAME)
        for product in lista_resultados:

            nome = product.find_element(By.CLASS_NAME, 'tAxDx').text
            nome = nome.lower()

            # verificacao do nome - se no nome tem algum termo banido
            tem_termos_banidos = False
            for palavra in lista_termos_banidos:
                if palavra in nome:
                    tem_termos_banidos = True

       
            # verificar se no nome tem todos os termos do nome do produto
            tem_todos_termos_produto = True
            for palavra in lista_termos_produto:
                if palavra not in nome:
                    tem_todos_termos_produto = False

            if not tem_termos_banidos and tem_todos_termos_produto: # verificando o nome
                try:   
                    preco =  product.find_element(By.CLASS_NAME, 'a8Pemb').text
                    preco = preco.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
                    preco = float(preco)

                    if preco_minimo <= preco <= preco_maximo:
                        #Pegar o Link
                        elemento_link = product.find_element(By.CLASS_NAME, 'bONr3b')
                        elemento_pai = elemento_link.find_element(By.XPATH, '..')
                        link = elemento_pai.get_attribute('href')

                        # Adicionando uma tubpla de produtos na lista de ofertas 
                        lista_ofertas.append((nome,preco,link))

                except:
                    continue
            
        return lista_ofertas
 
    
    def procurar_buscape_shopping(self):
        pass

    def enviar_email():
        pass



    def action(self, execution):
        # Runner passes the server url, the id of the task being executed,
        # the access token and the parameters that this task receives (when applicable).
        maestro = BotMaestroSDK.from_sys_args()
        ## Fetch the BotExecution with details from the task, including parameters
        execution = maestro.get_execution()

        print(f"Task ID is: {execution.task_id}")
        print(f"Task Parameters are: {execution.parameters}")


        # Configure whether or not to run on headless mode
        self.headless = False

        # Uncomment to change the default Browser to Firefox
        self.browser = Browser.CHROME

        # Uncomment to set the WebDriver path
        self.driver_path = ChromeDriverManager().install()

        # Opens the BotCity website.
        self.browse("https://google.com.br")

        # Maximize Window
        self.maximize_window()

        # Implement here your logic...
        
        lista_ofertas_google_shopping = self.procurar_google_shopping('iphone 12 64 gb', 'watch min', 3000, 3500)

        print(lista_ofertas_google_shopping)

        # Wait 3 seconds before closing
        self.wait(3000)

        # Finish and clean up the Web Browser
        # You MUST invoke the stop_browser to avoid
        # leaving instances of the webdriver open
        self.stop_browser()

        # Uncomment to mark this task as finished on BotMaestro
        maestro.finish_task(
            task_id=execution.task_id,
            status=AutomationTaskFinishStatus.SUCCESS,
            message="Task Finished OK."
        )


    def not_found(label):
        print(f"Element not found: {label}")


if __name__ == '__main__':
    Bot.main()
