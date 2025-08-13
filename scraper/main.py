import json
import requests
from bs4 import BeautifulSoup, Tag

URL_BASE = "https://quotes.toscrape.com"
# Lista  donde se almacenaran los logs en caso de errores
logs = []

def process_page(soup: BeautifulSoup, url: str):
    """
    #### Función ocupada para procesar paginas y extraer la información necesaria.
    """
    quotes = soup.find_all("div", class_="quote")
    next_button = soup.find("li", class_="next")
    res = []

    for i, quote in enumerate(quotes):
        if type(quote) != Tag:
            logs.append(f"{url}: la cita {i} no cumplio con ser del tipo Tag\n")
            continue
        content = quote.find("span", class_="text")
        author = quote.find("small", class_="author")

        if not content:
            logs.append(f"{url}: no se encontro el contenido de la cita {i}.\n")
            continue
        content = content.text

        if not author:
            logs.append(f"{url}: no se encontro el autor de la cita {i}.\n")
            continue
        author = author.text

        res.append({
            "cita": content,
            "autor": author
        })
    url = next_button.find("a") if type(next_button) == Tag else None
    return res, url


def main():
    """
    #### Punto de entrada del script.
    """
    # Se obtiene la información de la primera pagina
    res = requests.get(URL_BASE)
    soup = BeautifulSoup(res.content, "html.parser")
    response, next_button = process_page(soup, URL_BASE)

    # Si se encontro el boton de siguiente (next) se cargan las siguientes paginas
    # hasta encontrar una que no tenga el boton siguiente (next).
    while next_button:
        if type(next_button) != Tag:
            logs.append("El boton de siguiente no es una instancia del tipo Tag\n")
            continue
        # Se obtiene el url de la siguiente pagina del boton siguiente (next)
        url = next_button.attrs['href']
        url = URL_BASE + str(url)
        res_page = requests.get(url)
        soup = BeautifulSoup(res_page.content, "html.parser")
        response_page, next_button = process_page(soup, url)

        response.extend(response_page)

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(response, f, indent=4)

    with open("logs", "w", encoding="utf-8") as f:
        f.writelines(logs)

if __name__ == "__main__":
    main()
