document.getElementById('formulario').addEventListener('submit', async function (e) {
  e.preventDefault();

  const termo = document.getElementById('termo').value;
  const resultado = document.getElementById('resultado');

  // Substitua pelo SEU usuário e repositório
  const usuario = 'fabiowakisaka';
  const repositorio = 'comofazeremprestimo';

  // Personal Access Token com escopo 'repo'
  const token = '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';  // coloque temporariamente para testes locais

  const response = await fetch(`https://api.github.com/repos/${usuario}/${repositorio}/dispatches`, {
    method: 'POST',
    headers: {
      'Authorization': `token ${token}`,
      'Accept': 'application/vnd.github.everest-preview+json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      event_type: 'gerar-pagina',
      client_payload: {
        termo: termo
      }
    })
  });

  if (response.ok) {
    resultado.innerText = `Solicitação enviada para gerar a página sobre "${termo}". Aguarde o GitHub Actions finalizar o deploy.`;
  } else {
    resultado.innerText = 'Erro ao enviar solicitação.';
    console.error(await response.text());
  }
});
