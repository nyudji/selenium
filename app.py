from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Abre o navegador
nav = webdriver.Firefox()
url = 'https://www.farfetch.com/br/shopping/men/items.aspx'

# Acessar o site
nav.get(url)
print('Acessando o link:', url)
time.sleep(3)

# Maximiza a janela do navegador
nav.maximize_window()

# Espera até que o menu "Sale" esteja visível
wait = WebDriverWait(nav, 15)
sale_menu = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@data-nav='Sale']")))

# Cria uma ação para passar o mouse sobre o menu "Sale"
actions = ActionChains(nav)
actions.move_to_element(sale_menu).perform()
time.sleep(2)

# Carrega o submenu Jaquetas
try:
    jackets_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ewmv8150') and text()='Jackets']")))
    jackets_link.click()
    print("Clicou em Jaquetas com sucesso!")
except Exception as e:
    print("Erro ao clicar em Jaquetas:", e)
    nav.quit()  # Fecha o navegador se o clique falhar

# Espera para garantir que a página de Jaquetas carregue
time.sleep(5)

# Lista para armazenar dados de produtos
produtos_lista = []

# Encontra todos os elementos de marcas (com a classe 'ltr-10idii7-Body-BodyBold')
marcas = nav.find_elements(By.CLASS_NAME, 'ltr-10idii7-Body-BodyBold')
# Para cada marca, extrai os produtos e outras informações
marcas = nav.find_elements(By.CLASS_NAME, 'ltr-10idii7-Body-BodyBold')
# Para cada marca, extrai os produtos e outras informações
for marca in marcas:
    try:
        # Captura a marca
        marca_nome = marca.text
        print(marca_nome)
        
        # Encontra os elementos de nome do produto com o atributo 'data-component="ProductCardDescription"'
        produtos = nav.find_elements(By.XPATH, '//p[@data-component="ProductCardDescription"]')
        
        # Encontra os elementos de preço com o atributo 'data-component="PriceFinal"'
        precos = nav.find_elements(By.XPATH, '//p[@data-component="PriceFinal"]')
        
        nome_produto = produtos.text  # Extrai o texto do nome do produto
        preco = precos.text  # Extrai o texto do preço
        print(f"Produto: {nome_produto}, Preço: {preco}")
            
    except Exception as e:
        print(f"Erro ao processar o produto: {e}")

# Converte a lista de dicionários para um DataFrame
df_produtos = pd.DataFrame(produtos_lista)
print(produtos_lista)
# Exibe o DataFrame
print(df_produtos)

# Fecha o navegador
nav.quit()
