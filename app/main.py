from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/gerar-pagina', methods=['POST'])
def gerar_pagina():
    termo = request.json.get('termo', '')  # Recebe o termo via JSON

    # Aqui você pode adicionar a lógica de machine learning ou outro processamento
    # Exemplo: Vamos apenas gerar uma página simples com o termo fornecido
    pagina_html = f"""
    <html>
        <head><title>{termo}</title></head>
        <body>
            <h1>Resultado para {termo}</h1>
            <p>Esta é a página gerada com base no termo: {termo}</p>
        </body>
    </html>
    """

    # Salva o arquivo HTML gerado
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f'{termo}.html')
    with open(file_path, 'w') as file:
        file.write(pagina_html)

    return jsonify({"message": "Página gerada com sucesso!", "url": f"/{file_path}"}), 200

if __name__ == '__main__':
    app.run(debug=True)
