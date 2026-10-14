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
        return "- Controle de orçamento familiar, inflação, taxas de juros e crédito consciente no Brasil."

noticias_contexto = obter_termometro_noticias()

# 4. Matriz Tridimensional de Cruzamento (Público x Dor Financeira x Gatilho WhatsApp)
VETOR_PUBLICO = [
    {
        "perfil": "Aposentados e Pensionistas do INSS",
        "contexto": "Buscam segurança, têm medo de fraudes no benefício, precisam entender margem consignável e taxas máximas permitidas."
    },
    {
        "perfil": "Trabalhadores CLT com saldo no FGTS",
        "contexto": "Querem dinheiro rápido sem comprometer a renda mensal ou buscam entender se vale a pena antecipar o saque-aniversário ou usar consignado privado."
    },
    {
        "perfil": "Autônomos, MEIs e Profissionais Informais",
        "contexto": "Têm dificuldade de comprovar renda tradicional, precisam separar contas pessoais do negócio e buscar microcrédito ou linhas justas."
    },
    {
        "perfil": "Pessoas com Nome Restrito (Negativados)",
        "contexto": "Estão vulneráveis a golpes na internet, precisam limpar o nome com desconto real ou encontrar crédito legítimo com garantia."
    },
    {
        "perfil": "Endividados com Cartão de Crédito e Cheque Especial",
        "contexto": "Sofrem com o efeito bola de neve dos juros rotativos e precisam urgente trocar uma dívida cara por uma linha mais barata."
    },
    {
        "perfil": "Chefes de Família com Orçamento Apertado",
        "contexto": "Buscam fôlego financeiro no fim do mês, redução de despesas fixas e proteção patrimonial da família."
    },
    {
        "perfil": "Servidores Públicos",
        "contexto": "Possuem acesso às melhores taxas de consignado, mas frequentemente caem em armadilhas de renovação infinita de contratos ou cartão consignado (RMC)."
    }
]

VETOR_TEMAS = [
    {
        "tema": "Substituição Inteligente de Dívidas (Troca de Juros)",
        "diretriz": "Explique matematicamente e de forma simples como quitar dívidas que cobram mais de 10% ao mês usando um empréstimo planejado de taxa reduzida."
    },
    {
        "tema": "Blindagem Contra o Golpe do Falso Empréstimo",
        "diretriz": "Destaque a regra de ouro do Banco Central: nenhuma instituição financeira séria cobra taxa antecipada, frete de contrato, seguro-fiança ou depósito prévio para liberar crédito."
    },
    {
        "tema": "A Verdade sobre o Custo Efetivo Total (CET)",
        "diretriz": "Mostre como bancos embutem IOF, tarifas de cadastro e seguros opcionais na parcela, e como exigir a planilha do CET antes de assinar."
    },
    {
        "tema": "Seguro Prestamista Embutido (Venda Casada)",
        "diretriz": "Esclareça o direito do consumidor: o seguro no empréstimo quase sempre é opcional, e o cliente pode recusar ou pedir o cancelamento se foi incluído sem aviso."
    },
    {
        "tema": "Portabilidade de Crédito na Prática",
        "diretriz": "Ensine que o cliente não é obrigado a ficar preso ao banco onde tem conta; ele pode transferir sua dívida gratuitamente para outro banco que ofereça juros menores."
    },
    {
        "tema": "Desmistificando o Score de Crédito e o Cadastro Positivo",
        "diretriz": "Desmascare golpistas que vendem 'aumento de score' e ensine o que realmente os algoritmos dos bancos avaliam (histórico de pagamento em dia e relacionamento bancário)."
    },
    {
        "tema": "Direito de Amortização Antecipada com Desconto",
        "diretriz": "Revele a regra do Banco Central (Resolução CMN) que obriga qualquer banco a dar desconto proporcional dos juros se o cliente adiantar parcelas de trás para frente."
    },
    {
        "tema": "Perigos do Cartão de Crédito Consignado (RMC/RCC)",
        "diretriz": "Explique a diferença entre o empréstimo consignado comum (com prazo fixo) e o saque no cartão consignado, que pode descontar o mínimo da folha por anos se não for quitado integralmente."
    },
    {
        "tema": "Empréstimo com Garantia (Veículo, Imóvel ou FGTS)",
        "diretriz": "Mostre por que oferecer uma garantia real derruba drasticamente os juros cobrados pelo banco e quais cuidados tomar para não comprometer o bem."
    },
    {
        "tema": "Estratégias de Negociação de Dívidas Atrasadas",
        "diretriz": "Ensine a diferença entre aceitar o primeiro parcelamento automático do aplicativo do banco (que costuma ter juros altos) versus negociar quitação à vista ou em feirões oficiais."
    },
    {
        "tema": "Análise do Sistema Registrato do Banco Central",
        "diretriz": "Apresente a ferramenta oficial e gratuita do Banco Central (Registrato / SCR) onde o cidadão descobre se tem contas abertas em seu CPF ou dívidas esquecidas nos bancos."
    },
    {
        "tema": "Regra do Comprometimento Máximo de Renda (30%)",
        "diretriz": "Oriente como calcular o limite seguro da parcela no orçamento familiar antes de contratar crédito, evitando que o empréstimo vire uma nova dor de cabeça."
    }
]

VETOR_GATILHO_ZAP = [
    {
        "estilo": "Alerta de Utilidade Pública",
        "foco": "Tom de aviso urgente para proteger amigos e familiares de perderem dinheiro por falta de informação."
    },
    {
        "estilo": "Bastidor Bancário Revelado",
        "foco": "Revelar uma regra oficial ou direito do consumidor que é público, mas que as instituições raramente explicam no balcão."
    },
    {
        "estilo": "Alívio no Bolso e Economia Prática",
        "foco": "Mostrar com clareza como uma simples mudança de escolha economiza centenas ou milhares de reais no fim do contrato."
    },
    {
        "estilo": "Direito do Consumidor Financeiro",
        "foco": "Fundamentar a dica nas regras de proteção ao cidadão e transparência exigidas pelo Banco Central."
    },
    {
        "estilo": "Guia Rápido Anti-Sufoco",
        "foco": "Orientação direta, acolhedora e passo a passo para quem precisa de fôlego financeiro imediato sem cair em ciladas."
    }
]

# Evita repetir temas que já foram gerados recentemente olhando a pasta dicas/
pastas_existentes = []
if os.path.exists("dicas"):
    pastas_existentes = os.listdir("dicas")

# Semente diária determinística combinada com o histórico para garantir variedade
random.seed(f"{hoje_dt.strftime('%Y%m%d')}-{len(pastas_existentes)}")
publico_hoje = random.choice(VETOR_PUBLICO)
tema_hoje = random.choice(VETOR_TEMAS)
gatilho_hoje = random.choice(VETOR_GATILHO_ZAP)

# 5. Prompt de IA Sênior: Focado em Conversão WhatsApp + Rigor Técnico YMYL
prompt = f"""
Você é um Consultor Financeiro Sênior e Especialista em Defesa do Consumidor Bancário do portal 'Como Fazer Empréstimo' (um domínio com anos de autoridade e reputação).

Sua missão é escrever um conteúdo diário de altíssimo valor que será compartilhado em grupos de WhatsApp.
O leitor clicou em um link no WhatsApp atraído por uma promessa forte de utilidade. O seu texto DEVE entregar uma resposta completa, verdadeira, prática e reveladora, fazendo o visitante sentir que valeu muito a pena ter clicado.

CRUZAMENTO ESTRATÉGICO DE HOJE:
- PÚBLICO-ALVO PRINCIPAL: {publico_hoje['perfil']} ({publico_hoje['contexto']})
- TEMA CENTRAL: {tema_hoje['tema']} ({tema_hoje['diretriz']})
- ÂNGULO DE ENGAJAMENTO WHATSAPP: {gatilho_hoje['estilo']} ({gatilho_hoje['foco']})
- TERMÔMETRO ECONÔMICO DO DIA: {noticias_contexto}

DIRETRIZES INEGOCIÁVEIS DE REPUTAÇÃO E VERACIDADE (COMPLIANCE YMYL):
1. VERACIDADE ABSOLUTA: Jamais invente leis, taxas irreais ou promessas milagrosas (como 'empréstimo garantido sem análise' ou 'limpe seu nome em 24h'). Baseie-se exclusivamente na matemática financeira real, no Código de Defesa do Consumidor e nas boas práticas do Banco Central do Brasil.
2. ENTREGA DE ALTO VALOR (RECOMPENSA DO CLIQUE): Não escreva textos genéricos ou superficiais. Explique o 'como funciona' e o 'passo a passo prático' no segundo e terceiro parágrafos para que o leitor saia mais inteligente e protegido.
3. CONEXÃO NATURAL COM O SIMULADOR: Mostre que a melhor forma de não perder dinheiro é comparar o Custo Efetivo Total (CET) entre várias instituições confiáveis antes de fechar negócio.
4. FORMATAÇÃO VISUAL ESTILO WHATSAPP: Escreva 4 parágrafos bem estruturados e fáceis de ler no celular. Comece CADA parágrafo com um único emoji estratégico (ex: ⚠️, 💡, 📌, ✅, 🔍) seguido de uma frase curta de impacto.
5. PROIBIDO CLICHÊS DE IA: Nunca use palavras como 'jornada', 'tapeçaria', 'inabalável', 'farol', 'sinfonia', 'crucial' ou 'desbravar'. Use português claro, humano, respeitoso e direto.

Retorne EXCLUSIVAMENTE um objeto JSON puro e válido (sem blocos markdown ```json):
{{
  "titulo": "Título magnético de alta curiosidade e utilidade real (60 a 85 caracteres, sem emojis no título)",
  "chamada_zap": "Frase instigante de 1 a 2 linhas que desperta curiosidade imediata para ser enviada no WhatsApp da família ou amigos.",
  "paragrafos": [
    "Parágrafo 1 (Inicie com 1 emoji): O Gancho e Identificação. Conecte-se imediatamente com a dor do público-alvo e revele por que a maioria das pessoas perde dinheiro ou corre risco nessa situação.",
    "Parágrafo 2 (Inicie com 1 emoji): A Revelação Técnica Descomplicada. Explique a regra real, o funcionamento bancário ou o direito que resolve a dúvida prometida no título.",
    "Parágrafo 3 (Inicie com 1 emoji): O Passo a Passo Prático. Entregue 2 ou 3 ações diretas e aplicáveis hoje mesmo para o leitor economizar, negociar melhor ou se proteger.",
    "Parágrafo 4 (Inicie com 1 emoji): Conclusão Protetiva. Reforce a regra de segurança (nunca pagar taxas adiantadas) e oriente o leitor a sempre comparar propostas com calma."
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
        if chaves_obrigatorias.issubset(dados.keys()) and isinstance(dados["paragrafos"], list) and len(dados["paragrafos"]) >= 3:
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
url_completa = f"[https://www.comofazeremprestimo.com/](https://www.comofazeremprestimo.com/){caminho_pasta}/"

# 7. Renderização do Artigo (Sem duplicar emojis caso a IA já tenha incluído)
with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

paragrafos_limpos = []
for p in conteudo["paragrafos"]:
    texto_p = html.escape(re.sub(r'<[^>]+>', '', str(p)).strip())
    paragrafos_limpos.append(f"<p class='mb-4'>{texto_p}</p>")

reflexao_html = "\n".join(paragrafos_limpos)

# Mensagem de WhatsApp altamente convidativa para grupos de família e amigos
texto_compartilhar = (
    f"💡 *UTILIDADE PÚBLICA FINANCEIRA*\n\n"
    f"*{conteudo['titulo']}*\n\n"
    f"{conteudo['chamada_zap']}\n\n"
    f"👇 *Veja a explicação completa e proteja seu bolso:*\n"
    f"{url_completa}"
)
texto_whatsapp_encoded = urllib.parse.quote(texto_compartilhar)

# Varredura para coletar artigos para o rodapé
artigos_cadastrados = []
dir_dicas = "dicas"

if os.path.exists(dir_dicas):
    for pasta in os.listdir(dir_dicas):
        caminho_p = os.path.join(dir_dicas, pasta)
        if os.path.isdir(caminho_p) and pasta != slug_artigo:
            index_path = os.path.join(caminho_p, "index.html")
            if os.path.exists(index_path):
                try:
                    with open(index_path, "r", encoding="utf-8") as f_art:
                        conteudo_art = f_art.read()
                        m_title = re.search(r'<title>(.*?)</title>', conteudo_art)
                        titulo_art = m_title.group(1).split("—")[0].strip() if m_title else pasta.replace("-", " ").title()
                except Exception:
                    titulo_art = pasta.replace("-", " ").title()

                artigos_cadastrados.append({
                    "titulo": titulo_art,
                    "url": f"../{pasta}/"
                })

artigos_cadastrados.insert(0, {
    "titulo": conteudo["titulo"],
    "url": "./"
})

recomendados = random.sample(artigos_cadastrados[1:], min(3, len(artigos_cadastrados) - 1)) if len(artigos_cadastrados) > 1 else []
html_recomendados = ""
if recomendados:
    html_recomendados += '<div class="mt-5 pt-4 border-top">\n'
    html_recomendados += '  <h4 class="fw-bold text-dark mb-3">📚 Outras Dicas e Alertas Importantes:</h4>\n'
    html_recomendados += '  <ul class="list-unstyled">\n'
    for rec in recomendados:
        html_recomendados += f'    <li class="mb-2"><a href="{rec["url"]}" class="text-warning fw-bold text-decoration-none">&rarr; {rec["titulo"]}</a></li>\n'
    html_recomendados += '  </ul>\n'
    html_recomendados += '</div>\n'

html_final = template \
    .replace("{{TITULO}}", html.escape(conteudo["titulo"])) \
    .replace("{{CHAMADA_ZAP}}", html.escape(conteudo["chamada_zap"])) \
    .replace("{{DATA_EXTENSO}}", data_extenso) \
    .replace("{{REFLEXAO_HTML}}", reflexao_html + html_recomendados) \
    .replace("{{TEXTO_WHATSAPP}}", texto_whatsapp_encoded)

os.makedirs(caminho_pasta, exist_ok=True)
with open(f"{caminho_pasta}/index.html", "w", encoding="utf-8") as f:
    f.write(html_final)

# 8. Geração da Central de Dicas (`dicas/index.html`)
lista_html_indice = ""
for art in artigos_cadastrados:
    if art["url"] == "./":
        link_url = f"./{slug_artigo}/"
    else:
        slug_da_pasta = art["url"].replace("../", "").replace("/", "")
        link_url = f"./{slug_da_pasta}/"

    lista_html_indice += f"""
    <div class="card mb-4 shadow-sm border-0 border-start border-warning border-4">
      <div class="card-body p-4">
        <h3 class="h5 fw-bold mb-2"><a href="{link_url}" class="text-dark text-decoration-none">{art["titulo"]}</a></h3>
        <a href="{link_url}" class="text-warning fw-bold text-decoration-none fs--1">Ler Orientação Completa &rarr;</a>
      </div>
    </div>
    """

html_indice_central = """<!DOCTYPE html>
<html lang="pt-BR" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Central de Dicas e Alertas Financeiros — Como Fazer Empréstimo</title>
  <script src="../assets/js/monetization-config.js"></script>
  <script src="../assets/js/affiliate-manager.js" defer></script>
  <link href="../assets/css/theme.css" rel="stylesheet" />
  <link href="[https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap](https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap)" rel="stylesheet">
</head>
<body>
  <main class="main" id="top">
    <div id="header-placeholder"></div>

    <section class="py-6 bg-soft-primary">
      <div class="container text-center">
        <span class="badge bg-soft-warning text-warning mb-3 py-2 px-3 fw-bold">EDUCAÇÃO FINANCEIRA E PROTEÇÃO</span>
        <h1 class="fw-bold mb-3">Central de Dicas e Alertas</h1>
        <p class="lead text-secondary">Orientações diárias verificadas para proteger o seu bolso, evitar juros abusivos e encontrar crédito com segurança.</p>
      </div>
    </section>

    <section class="py-5">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-8">
            REPLACE_LISTA_ARTIGOS

            <div class="text-center mt-5">
              <a href="../index.html" class="btn btn-outline-secondary btn-md fw-bold">&larr; Voltar para a Página Principal</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <div id="footer-placeholder"></div>
  </main>

  <script>
    function loadComponent(id, file, callback) {
      fetch(file)
        .then(response => response.text())
        .then(data => {
          document.getElementById(id).innerHTML = data;
          if (callback) callback();
        });
    }
    loadComponent('header-placeholder', '../components/header.html');
    loadComponent('footer-placeholder', '../components/footer.html', function() {
      const footerImages = document.querySelectorAll('#footer-placeholder img');
      footerImages.forEach(img => {
        const src = img.getAttribute('src');
        if (src && !src.startsWith('http') && !src.startsWith('../')) {
          img.setAttribute('src', '../' + src);
        }
      });
      const footerLinks = document.querySelectorAll('#footer-placeholder a');
      footerLinks.forEach(a => {
        const href = a.getAttribute('href');
        if (href && !href.startsWith('http') && !href.startsWith('../') && !href.startsWith('#')) {
          a.setAttribute('href', '../' + href);
        }
      });
    });
  </script>

  <script src="../vendors/bootstrap/bootstrap.min.js"></script>
  <script src="../vendors/fontawesome/all.min.js"></script>
</body>
</html>
""".replace("REPLACE_LISTA_ARTIGOS", lista_html_indice)

with open(f"{dir_dicas}/index.html", "w", encoding="utf-8") as f_ind:
    f_ind.write(html_indice_central)

# 9. Varredura Global Automática do Sitemap
dominio_base = "[https://www.comofazeremprestimo.com](https://www.comofazeremprestimo.com)"
urls_encontradas = []

for root, dirs, files in os.walk("."):
    if any(ignorado in root for ignorado in [".git", ".github", "assets", "vendors", "components"]):
        continue

    for file in files:
        if file.endswith(".html") and file != "template.html":
            caminho_relativo = os.path.join(root, file).replace("\\", "/")
            if caminho_relativo == "./index.html":
                url = f"{dominio_base}/"
            elif file == "index.html":
                limpo = caminho_relativo.replace("./", "").replace("/index.html", "/")
                url = f"{dominio_base}/{limpo}"
            else:
                limpo = caminho_relativo.replace("./", "")
                url = f"{dominio_base}/{limpo}"
            urls_encontradas.append(url)

urls_encontradas = sorted(list(set(urls_encontradas)))

sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap_xml += '<urlset xmlns="[http://www.sitemaps.org/schemas/sitemap/0.9](http://www.sitemaps.org/schemas/sitemap/0.9)">\n'

for u in urls_encontradas:
    sitemap_xml += '  <url>\n'
    sitemap_xml += f'    <loc>{u}</loc>\n'
    sitemap_xml += f'    <lastmod>{data_hoje_iso}</lastmod>\n'
    sitemap_xml += '  </url>\n'

sitemap_xml += '</urlset>'

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

print(f"Sucesso: [{publico_hoje['perfil']}] x [{tema_hoje['tema']}] gerado em {caminho_pasta}.")
