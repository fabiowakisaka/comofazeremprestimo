async function enviarTermo() {
  const termo = document.getElementById('termo').value;
  const token = 'SEU_TOKEN_GITHUB_COM_PERMISSAO';
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
