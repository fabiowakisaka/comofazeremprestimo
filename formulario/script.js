async function enviarTermo() {
  const termo = document.getElementById('termo').value;
  const token = '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'; 
  const repo = 'fabiowakisaka/comofazeremprestimo';
  const path = 'app/entrada.txt';
  const branch = 'main';

  const fileUrl = `https://api.github.com/repos/${repo}/contents/${path}`;
  const headers = {
    "Authorization": `Bearer ${token}`,
    "Accept": "application/vnd.github+json"
  };

  try {
    // Buscar SHA atual
    const getResp = await fetch(fileUrl, { headers });

    // **Exibe o erro detalhado na API para depuração**
    console.log("Resposta da API - GET:", await getResp.text());

    if (!getResp.ok) throw new Error(`Erro ao buscar SHA: ${getResp.statusText}`);
    const fileData = await getResp.json();
    const sha = fileData.sha;

    // Codificar novo conteúdo
    const conteudo = btoa(unescape(encodeURIComponent(termo)));

    // Fazer PUT para atualizar
    const body = {
      message: `Novo termo: ${termo}`,
      content: conteudo,
      sha: sha,
      branch: branch
    };

    const putResp = await fetch(fileUrl, {
      method: "PUT",
      headers,
      body: JSON.stringify(body)
    });

    // **Exibe a resposta do PUT também**
    console.log("Resposta da API - PUT:", await putResp.text());

    if (putResp.ok) {
      document.getElementById('resultado').innerText = "✅ Enviado com sucesso! Aguarde a geração da página.";
    } else {
      const err = await putResp.json();
      console.error("Erro PUT:", err);
      document.getElementById('resultado').innerText = "❌ Erro ao atualizar o arquivo:\n" + JSON.stringify(err, null, 2);
    }

  } catch (err) {
    console.error("Erro geral:", err);
    document.getElementById('resultado').innerText = "❌ Erro ao enviar solicitação:\n" + err.message;
  }
}

// Conecta o envio do formulário com a função
document.getElementById("formulario").addEventListener("submit", function (event) {
  event.preventDefault();
  enviarTermo();
});
