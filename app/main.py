import json
import os

# Caminho para o payload
payload_path = os.path.join(os.getcwd(), 'payload.json')

# Carregar o payload
if os.path.exists(payload_path):
    with open(payload_path, 'r', encoding='utf-8') as f:
        payload = json.load(f)
        termo = payload.get("termo", "termo_padrao")  # chave que você mandou do JS
        print(f"Gerando página para o termo: {termo}")
else:
    termo = "termo_padrao"
    print("payload.json não encontrado. Usando termo padrão.")

# Aqui você faz o processamento e geração do HTML com o termo
with open(f"output/{termo}.html", "w", encoding="utf-8") as f:
    f.write(f"<html><body><h1>Informações sobre {termo}</h1></body></html>")
