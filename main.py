# app/main.py
import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

# Criar pastas de saída se não existirem
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Configurar Jinja2 para usar templates
env = Environment(loader=FileSystemLoader('app/templates'))

# Exemplo simples de scraping de produtos
def scrape_amazon_mock():
    # Simulação de scraping (no real, usaria requests + headers ou Selenium)
    produtos = [
        {"nome": "Echo Dot", "preco": "R$ 249,00", "link": "https://amzn.to/xyz"},
        {"nome": "Kindle Paperwhite", "preco": "R$ 499,00", "link": "https://amzn.to/abc"},
    ]
    return produtos

# Geração de página HTML
def gerar_html(produtos):
    template = env.get_template('pagina.html')
    html = template.render(produtos=produtos, data=datetime.today().strftime('%Y-%m-%d'))

    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    produtos = scrape_amazon_mock()
    gerar_html(produtos)
