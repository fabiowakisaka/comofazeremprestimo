# app/main.py
import sys
import os

# Pega o termo passado como argumento
termo = sys.argv[1] if len(sys.argv) > 1 else "produto-desconhecido"
print(f"Gerando página para: {termo}")

# Garante que a pasta 'output' existe
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Gera HTML básico com o termo
html_content = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Sobre {termo}</title>
</head>
<body>
    <h1>Informações sobre {termo}</h1>
    <p>Esta é uma página gerada automaticamente para o produto: <strong>{termo}</strong>.</p>
</body>
</html>
"""

# Salva no arquivo output/{termo}.html
output_file = os.path.join(output_dir, f"{termo}.html")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Página criada com sucesso em: {output_file}")
