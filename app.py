from flask import Flask

app = Flask(__name__)

# Gera e salva um arquivo HTML antes de servir
html_content = "<h1>Bem-vindo!</h1><p>Esta é uma página gerada em Python.</p>"
with open("pagina.html", "w") as file:
    file.write(html_content)

@app.route("/")
def home():
    return open("pagina.html").read()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
