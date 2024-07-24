import requests
from bs4 import BeautifulSoup
import csv

def fetch_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f'Falha ao acessar a página. Status code: {response.status_code}')
            return None
    except requests.RequestException as e:
        print(f'Erro na requisição HTTP: {e}')
        return None

def parse_informations(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Categoria', 'Informação'])
        for item in data:
            writer.writerow([item['Categoria'], item['Informação']])