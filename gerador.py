import os
import re
import sys
import json
import html
import urllib.parse
import unicodedata
import random
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from google import genai

# 1. Configuração Segura da Nova SDK Gemini
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERRO CRÍTICO: A chave GEMINI_API_KEY não foi encontrada nos Secrets do GitHub.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

# 2. Tratamento de Datas
hoje_dt = datetime.now()
data_hoje_iso = hoje_dt.strftime("%Y-%m-%d")

dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
data_extenso = f"{dias_semana[hoje_dt.weekday()]}, {hoje_dt.day} de {meses[hoje_dt.month - 1]} de {hoje_dt.year}"

# 3. Termômetro Social (Notícias de Economia do G1)
def obter_termometro_noticias():
    try:
        url = "https://g1.globo.com/rss/g1/economia/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        xml_data = urllib.request.urlopen(req, timeout=6).read()
        root = ET.fromstring(xml_data)
        titulos = [item.find('title').text for item in root.findall('./channel/item')[:5]]
        return "\n".join([f"- {t.strip()}" for t in titulos if t])
    except Exception as e:
        print(f"Aviso ao consultar notícias: {e}")
        return "- Controle de orçamento familiar, inflação, boletos e crédito consciente no Brasil."

noticias_contexto = obter_termometro_noticias()

# 4. Matriz de Ângulos Financeiros
ANGULOS_FINANCEIROS = [
    {"tema": "Como organizar dívidas caras", "diretriz": "Foque em trocar dívidas de juros altos por linhas mais baratas."},
    {"tema": "O perigo do depósito antecipado", "diretriz": "Alerta rigoroso contra golpistas que cobram taxa para liberar empréstimo."},
    {"tema": "Calculando o Custo Efetivo Total", "diretriz": "Explique por que a taxa de juros mensal não é o único valor que importa."},
    {"tema": "Organizando o orçamento com o método 50-30-20", "diretriz": "Dica prática de divisão de renda para sobrar dinheiro."},
    {"tema": "Como recuperar o Score de crédito", "diretriz": "Passos práticos e reais para subir a pontuação sem falsas promessas."},
    {"tema": "Empréstimo consignado vale a pena?", "diretriz": "Analise prós e contras para aposentados, pensionistas e CLT."},
    {"tema": "Negociação de dívidas", "diretriz": "Oriente sobre como conseguir descontos reais para limpar o nome."}
]

random.seed(hoje_dt.strftime("%Y%m%d"))
angulo_hoje = random.choice(ANGULOS_FINANCEIROS)

# 5. Prompt de IA Focado em Estilo WhatsApp e Clareza
prompt = f"""
Você é um consultor financeiro sênior, especialista em crédito consciente.
Escreva um artigo objetivo, com uma abordagem que desperte curiosidade logo no início e entregue uma solução clara.
O texto deve ser extremamente escaneável, utilizando emojis estratégicos (como ✅, ⚠️, 💡, 📌) no início dos parágrafos ou tópicos para destacar as informações, lembrando o formato de mensagens de alto engajamento no WhatsApp.

TEMA DO DIA: {angulo_hoje['tema']} - {angulo_hoje['diretriz']}
CONTEXTO ATUAL: {noticias_contexto}

REGRAS:
1. Linguagem simples, direta e protetiva.
2. Insira emojis de destaque de forma elegante no início de frases-chave.
3. Proibido clichês de IA (jornada, tapeçaria, inabalável, farol).

Retorne EXCLUSIVAMENTE um JSON puro e válido (sem blocos markdown):
{{
  "titulo": "Título com forte curiosidade (ex: O erro silencioso que faz seu empréstimo custar o dobro)",
  "chamada_zap": "Uma frase de impacto curta gerando curiosidade para quem recebe no WhatsApp.",
  "paragrafos": [
    "Parágrafo 1 com emoji inicial: O gancho que revela o problema oculto ou a dúvida principal.",
    "Parágrafo 2 com emoji inicial: O esclarecimento prático, com orientações detalhadas passo a passo.",
    "Parágrafo 3 com emoji inicial: A conclusão protetiva e orientações de segurança final."
  ]
}}
"""

# 5.1 Cascata de Modelos Failproof
modelos_candidatos = ["gemini-2.5-flash", "gemini-3.0-flash", "gemini-2.5-pro", "gemini-2.0-flash"]
try:
    for m in client.models.list():
        nome_m = m.name.replace("models/", "")
        if "gemini" in nome_m and ("flash" in nome_m or "pro" in nome_m):
            if not any(x in nome_m for x in ["vision", "embedding", "audio", "tts"]):
                if nome_m not in modelos_candidatos:
                    modelos_candidatos.append(nome_m)
except Exception as e:
    print(f"Aviso ao listar modelos: {e}")

conteudo = None
chaves_obrigatorias = {"titulo", "chamada_zap", "paragrafos"}

for nome_modelo in modelos_candidatos:
    try:
        print(f"Tentando gerar com {nome_modelo}...")
        response = client.models.generate_content(model=nome_modelo, contents=prompt)
        raw_text = (response.text or "").strip()
        if not raw_text:
            continue

        if "```" in raw_text:
            partes = raw_text.split("```")
            for p in partes:
                if "{" in p and "}" in p:
                    raw_text = p
                    break
        inicio = raw_text.find("{")
        fim = raw_text.rfind("}")
        if inicio != -1 and fim != -1:
            raw_text = raw_text[inicio:fim + 1]

        dados = json.loads(raw_text.strip())
        if chaves_obrigatorias.issubset(dados.keys()) and isinstance(dados["paragrafos"], list):
            conteudo = dados
            print(f"✅ Conteúdo gerado com sucesso usando {nome_modelo}!")
            break
    except Exception as e:
        print(f"Erro com {nome_modelo}: {e}")

if not conteudo:
    print("❌ ERRO CRÍTICO: Falha em todos os modelos Gemini. Abortando script.")
    sys.exit(1)

# 6. Função para criar Slug Amigável
def criar_slug(texto):
    nfkd = unicodedata.normalize('NFKD', texto)
    palavra_sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
    slug = re.sub(r'[^a-zA-Z0-9\s]', '', palavra_sem_acento).lower()
    slug = re.sub(r'\s+', '-', slug).strip('-')
    return slug

slug_artigo = criar_slug(conteudo["titulo"])
caminho_pasta = f"dicas/{slug_artigo}"
url_completa = f"https://www.comofazeremprestimo.com/{caminho_pasta}/"

# 7. Renderização e Sanitização do HTML
with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

paragrafos_limpos = [f"<p class='mb-4'>✨ {html.escape(re.sub(r'<[^>]+>', '', str(p)).strip())}</p>" for p in conteudo["paragrafos"]]
reflexao_html = "".join(paragrafos_limpos)

# Texto formatado para o compartilhamento via WhatsApp
texto_compartilhar = f"⚠️ *ALERTA E DICA FINANCEIRA* ⚠️\n\n{conteudo['chamada_zap']}\n\n👉 Leia os detalhes completos aqui:\n{url_completa}"
texto_whatsapp_encoded = urllib.parse.quote(texto_compartilhar)

html_final = template \
    .replace("{{TITULO}}", html.escape(conteudo["titulo"])) \
    .replace("{{CHAMADA_ZAP}}", html.escape(conteudo["chamada_zap"])) \
    .replace("{{DATA_EXTENSO}}", data_extenso) \
    .replace("{{REFLEXAO_HTML}}", reflexao_html) \
    .replace("{{TEXTO_WHATSAPP}}", texto_whatsapp_encoded)

os.makedirs(caminho_pasta, exist_ok=True)
with open(f"{caminho_pasta}/index.html", "w", encoding="utf-8") as f:
    f.write(html_final)

# 8. Varredura Global Automática do Sitemap (Sitemap Crawler)
dominio_base = "https://www.comofazeremprestimo.com"
urls_encontradas = []

# Varre o diretório à procura de index.html e páginas html principais
for root, dirs, files in os.walk("."):
    # Ignora pastas ocultas como .git e .github
    if ".git" in root or ".github" in root or "assets" in root or "vendors" in root or "components" in root:
        continue
    
    for file in files:
        if file.endswith(".html"):
            caminho_relativo = os.path.join(root, file).replace("\\", "/")
            
            # Converte o caminho do arquivo para URL amigável
            if caminho_relativo == "./index.html":
                url = f"{dominio_base}/"
            elif file == "index.html":
                # Remove o './' inicial e o '/index.html' final para virar uma pasta limpa com barra
                limpo = caminho_relativo.replace("./", "").replace("/index.html", "/")
                url = f"{dominio_base}/{limpo}"
            else:
                # Páginas soltas (ex: simulador.html)
                limpo = caminho_relativo.replace("./", "")
                url = f"{dominio_base}/{limpo}"
            
            urls_encontradas.append(url)

# Remove duplicadas e ordena para manter o sitemap limpo
urls_encontradas = sorted(list(set(urls_encontradas)))

# Constrói o XML do Sitemap do zero com todas as páginas ativas
sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for u in urls_encontradas:
    sitemap_xml += '  <url>\n'
    sitemap_xml += f'    <loc>{u}</loc>\n'
    sitemap_xml += f'    <lastmod>{data_hoje_iso}</lastmod>\n'
    sitemap_xml += '  </url>\n'

sitemap_xml += '</urlset>'

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

print(f"Sucesso: Artigo gerado em {caminho_pasta}. Sitemap global reconstruído com {len(urls_encontradas)} URLs indexadas.")
