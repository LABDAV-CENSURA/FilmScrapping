import requests
from bs4 import BeautifulSoup
import csv

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_html(url):
    # Configurar o WebDriver do Chrome
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Para rodar sem abrir uma janela do navegador
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Inicializar o navegador
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Esperar para carregar a página (pode ser ajustado)
        
        html_content = driver.page_source
        return html_content
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return None
    finally:
        driver.quit()

def parse_informations(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def save_to_csv(headers, all_data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Categoria'] + headers)
        for category, infos in all_data.items():
            writer.writerow([category] + infos)