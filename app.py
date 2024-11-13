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

# Encontra todos os elementos de marcas
produtos = nav.find_elements(By.XPATH, '//p[@data-component="ProductCardDescription"]')

for produto in produtos:
    try:
        # Captura o nome da marca atual
        produtos = produto.text
        print(f"Produto: {produtos}")
        
        # Rola até a marca para garantir que esteja visível
        nav.execute_script("arguments[0].scrollIntoView();", produto)
        time.sleep(1)  # Pequena pausa para garantir que a rolagem tenha sido concluída

        # Move-se para o elemento da marca atual para garantir que está visível
        ActionChains(nav).move_to_element(produto).perform()
        
        # Encontra os produtos específicos dessa marca visível
        marcas = nav.find_elements(By.XPATH, '//p[@data-component="ProductCardBrandName"]')
        precos = nav.find_elements(By.XPATH, '//p[@data-component="PriceFinal"]')
        marcas = nav.find_elements(By.XPATH, '//p[@data-component="ProductCardBrandName"]')
        precos_og = nav.find_elements(By.XPATH, '//p[@data-component="PriceOriginal"]')
        precos_disc = nav.find_elements(By.XPATH, '//p[@data-component="PriceDiscount"]')

        
        # Filtra produtos e preços apenas dessa marca
        for marcas, precos, precos_og, precos_disc in zip(marcas, precos, precos_og, precos_disc):
            marcas = marcas.text  # Extrai o texto do nome do produto
            precos = precos.text  # Extrai o texto do preço
            precos_og = precos_og.text  # Extrai o texto do nome do produto
            precos_disc = precos_disc.text  # Extrai o texto do preço
            produtos_lista.append({
                    "Produto": produtos,
                    "Marca": marcas,
                    "Preço": precos,
                    "Preço Original": precos_og,
                    "Desconto": precos_disc
                })
                
    except Exception as e:
        print(f"Erro ao processar o produto para a marca {produto}: {e}")

# Converte a lista de dicionários para um DataFrame
df_produtos = pd.DataFrame(produtos_lista)
df_produtos
df_produtos.to_csv("produtos.csv", index=False, encoding='utf-8')
print("Dados salvos em produtos.csv com sucesso.")

# Fecha o navegador
nav.quit()
