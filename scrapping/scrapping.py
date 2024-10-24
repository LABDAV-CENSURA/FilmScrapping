from flask import Flask, request, jsonify
import random
import time
from functions import fetch_html, parse_informations
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/scrape', methods=['POST'])
def scrape():
    start_id = request.json.get('start_id', 1)
    end_id = request.json.get('end_id', 10)
    year_start = request.json.get('year_start', 1931)
    year_end = request.json.get('year_end', year_start)

    base_url = "https://bases.cinemateca.org.br/cgi-bin/wxis.exe/iah/?IsisScript=iah/iah.xis&base=FILMOGRAFIA&lang=p&nextAction=lnk&exprSearch=ID={}&format=detailed.pft#1"

    all_data = []

    for film_id in range(start_id, end_id + 1):
        time.sleep(random.uniform(0.05, 0.03))  
        film_id_str = str(film_id).zfill(6)
        url = base_url.format(film_id_str)
        html_content = fetch_html(url)

        if html_content:
            soup = parse_informations(html_content)

            # Título do filme
            title = soup.find('b', class_='title')
            title = title.text.strip() if title else "Não encontrado"

            # Extração do ano de produção
            year = None
            data_producao = soup.find('b', text="Ano:")
            if data_producao:
                year = data_producao.next_sibling.strip()

            # Verificar se o ano está dentro da faixa desejada
            if year and year.isdigit() and year_start <= int(year) <= year_end:
                # Inicializa o dicionário com ID, Título e Ano
                film_data = {
                    "ID": film_id_str,
                    "Título": title,
                    "Ano": year,
                }

                # Extraindo as informações adicionais, ignorando Título, ID, e Ano
                labels = soup.find_all('b', class_='label')

                for label in labels:
                    label_name = label.text.strip()
                    # Ignorar os campos já extraídos
                    if label_name.lower() in ['título', 'id', 'ano']:
                        continue

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

                    # Adiciona diretamente a informação no dicionário do filme
                    film_data[label_name] = label_value

                # Adiciona o filme ao dicionário de todos os filmes
                all_data.append(film_data)

                print(f"Filme ID {film_id_str} processado com sucesso. Ano: {year}")
            else:
                print(f"Filme ID {film_id_str} fora da faixa de anos ({year}).")

        else:
            print(f"Falha ao processar o ID {film_id_str}")

    # Retorna os dados em formato JSON
    return jsonify(all_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)