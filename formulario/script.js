async function enviarTermo() {
  const termo = document.getElementById('termo').value;
  const token = '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'; // Evite expor tokens em produção!
  const repo = 'fabiowakisaka/comofazeremprestimo';
  const path = 'app/entrada.txt';
  const branch = 'main';

  const fileUrl = `https://api.github.com/repos/${repo}/contents/${path}`;
  const headers = {
    "Authorization": `Bearer ${token}`,
    "Accept": "application/vnd.github+json"
  };

  try {
    // Pega o SHA atual do arquivo
    const getResp = await fetch(fileUrl, { headers });
    if (!getResp.ok) throw new Error(`Erro ao buscar SHA: ${getResp.statusText}`);
    const fileData = await getResp.json();
    const sha = fileData.sha;

    // Codifica o novo conteúdo
    const conteudo = btoa(unescape(encodeURIComponent(termo)));

    // Atualiza o arquivo via PUT
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
  
  
  
  const repo = 'fabiowakisaka/comofazeremprestimo';
  const path = 'app/entrada.txt';
  const branch = 'main';

  const fileUrl = `https://api.github.com/repos/${repo}/contents/${path}`;
  const headers = {
    "Authorization": `Bearer ${token}`,
    "Accept": "application/vnd.github+json"
  };

  // Pega o SHA atual do arquivo
  const getResp = await fetch(fileUrl, { headers });
  const fileData = await getResp.json();
  const sha = fileData.sha;

  // Codifica o novo conteúdo
  const conteudo = btoa(unescape(encodeURIComponent(termo)));

  // Atualiza o arquivo via PUT
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

  if (putResp.ok) {
    document.getElementById('resposta').innerText = "Enviado com sucesso! Aguarde a geração.";
  } else {
    const err = await putResp.text();
    document.getElementById('resposta').innerText = "Erro: " + err;
  }
}
