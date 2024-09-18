import random
import time
from functions import fetch_html, parse_informations, save_to_csv

def main():
    base_url = "https://bases.cinemateca.org.br/cgi-bin/wxis.exe/iah/?IsisScript=iah/iah.xis&base=FILMOGRAFIA&lang=p&nextAction=lnk&exprSearch=ID={}&format=detailed.pft#1"
    
    start_id = 0
    end_id = 999999

    headers = []
    all_data = {}

    for film_id in range(start_id, end_id + 1):
        time.sleep(random.uniform(5, 10))  # Delay aleatório entre 5 e 10 segundos
        film_id_str = str(film_id).zfill(6)
        url = base_url.format(film_id_str)
        html_content = fetch_html(url)
        
        if html_content:
            soup = parse_informations(html_content)

            title = soup.find('b', class_='title')
            title = title.text.strip() if title else "Não encontrado"

            headers.append(f"Filme {film_id_str}")
            
            labels = soup.find_all('b', class_='label')
            
            # Adiciona o título à primeira categoria
            if 'Título' not in all_data:
                all_data['Título'] = []
            all_data['Título'].append(title)

            for label in labels:
                label_name = label.text.strip()
                label_value = ""

                for sibling in label.next_siblings:
                    if sibling.name == 'b' and 'label' in sibling.get('class', []):
                        break
                    if isinstance(sibling, str):
                        label_value += sibling.strip()
                    elif sibling.name == 'br':
                        label_value += '\n'
                    elif sibling.name == 'blockquote':
                        label_value += sibling.get_text(strip=True)
                    else:
                        label_value += sibling.get_text(strip=True)

                label_value = label_value.strip()
                
                if label_name not in all_data:
                    all_data[label_name] = []

                all_data[label_name].append(label_value)

            print(f"Filme ID {film_id_str} processado com sucesso.")
        
        else:
            print(f"Falha ao processar o ID {film_id_str}")

    max_columns = len(headers)
    for category in all_data:
        while len(all_data[category]) < max_columns:
            all_data[category].append("")

    csv_filename = 'informacoes_filmes.csv'
    save_to_csv(headers, all_data, csv_filename)
    print(f'Dados salvos em {csv_filename}')
 
if __name__ == "__main__":
    main()