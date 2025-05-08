import os
import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

# Exemplo de scraping de um título de página
url = 'https://www.amazon.com.br/dp/B08CFSZLQ4'  # Exemplo: Echo Dot
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Extrai o título da página como exemplo
titulo = soup.title.string.strip() if soup.title else "Produto sem título"

# Carrega o template HTML com Jinja2
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('pagina.html')

# Gera a página preenchida
html_gerado = template.render(titulo=titulo)

# Salva o HTML no diretório de saída
os.makedirs('output', exist_ok=True)
with open('output/index.html', 'w', encoding='utf-8') as f:
    f.write(html_gerado)

print("Página gerada com sucesso.")
