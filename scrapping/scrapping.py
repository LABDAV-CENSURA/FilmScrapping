from bs4 import NavigableString
from functions import fetch_html, parse_informations, save_to_csv

def main():
    url = "https://bases.cinemateca.org.br/cgi-bin/wxis.exe/iah/?IsisScript=iah/iah.xis&base=FILMOGRAFIA&lang=p&nextAction=lnk&exprSearch=ID=039949&format=detailed.pft#1"
    
    html_content = fetch_html(url)
    
    if html_content:
        data = parse_informations(html_content)
        if data:
            title = data.find('b', class_='title')
            title = title.text.strip() if title else "Não encontrado"
            print(f"Título: {title}")

            # Find all labels
            labels = data.find_all('b', class_='label')
            data = []
            
            for label in labels:
                label_name = label.text.strip()
                label_value = ""
                
                # Iterate through the siblings until the next label or end of section
                for sibling in label.next_siblings:
                    if sibling.name == 'b' and 'label' in sibling.get('class', []):
                        break  # Stop at the next label
                    if isinstance(sibling, NavigableString):
                        label_value += sibling.strip()
                    elif sibling.name == 'br':
                        label_value += '\n'
                    elif sibling.name == 'blockquote':
                        label_value += sibling.get_text(strip=True)
                    else:
                        label_value += sibling.get_text(strip=True)

                label_value = label_value.strip()
                print(f"{label_name}: {label_value}")
                data.append({'Categoria': label_name, 'Informação': label_value})
            
            # Optionally, save the data to CSV
            csv_filename = 'informacoes_filme.csv'
            save_to_csv(data, csv_filename)
            print(f"Dados salvos em {csv_filename}")
    
    else:
        print('Não foi possível obter o conteúdo HTML.')

if __name__ == "__main__":
    main()