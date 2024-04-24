# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

#Importação das opções do navegador
from botcity.web.browsers.chrome import default_options

#atualizar o chromedriver automaticamente
from webdriver_manager.chrome import ChromeDriverManager


import pandas as pd

class Bot(WebBot):

    produtos = pd.read_excel('buscas.xlsx')
    list_products = []

    def search_google_shopping(self, product, name_banid, min_price, max_price):

        product = product.lower()
        list_term_product = product.split(' ')

        name_banid = name_banid.lower()
        list_name_banid = name_banid.split(' ')

        self.find_element('//*[@id="APjFqb"]', By.XPATH).send_keys(str(product)) 
        self.wait(1000)
        self.enter()

        menus_google = self.find_element('crJ18e', By.CLASS_NAME)
        
        if menus_google: 
            shopping_link = menus_google.find_element(By.LINK_TEXT, 'Shopping')
            if shopping_link:
                shopping_link.click()

        self.wait(2000)


        result_list = self.find_elements('i0X6df', By.CLASS_NAME)

        for product in result_list:

            name = product.find_element(By.CLASS_NAME, 'tAxDx').text
            name = name.lower()
         
            # Analisa se tem algum nome banido
            is_a_term_banid = False
            for letter in list_name_banid:
                if letter in name:
                    is_a_term_banid = True

            # Analisar se ele tem todos os termos do produto
            is_all_term_product = True
            for letter in list_term_product:
                if letter in name:
                    is_all_term_product = False

            if not is_a_term_banid  and is_all_term_product:   
                price =  product.find_element(By.CLASS_NAME, 'a8Pemb').text
                price = price.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
                price = float(price)

                min_price = float(min_price)
                max_price = float(max_price)

                if min_price <= price  <= max_price:
                    #Get Link
                    element_referenc = product.find_element(By.CLASS_NAME, 'bONr3b')
                    element_dad = element_referenc.find_element(By.XPATH, '..')
                    link = element_dad.get_attribute('href')

                    print(name, price , link)

    
    
    
    def search_buscape_shopping(self):
        pass

    def send_email():
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
        
        self.search_google_shopping('iphone 12 64 gb', 'mini watch', 3000, 3500)

        print('Tamanho da lista ',len(self.list_products))

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
