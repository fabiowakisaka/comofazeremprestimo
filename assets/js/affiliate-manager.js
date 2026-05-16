// ============================================================
// AFFILIATE MANAGER — comofazeremprestimo.com
// Plataforma: Actionpay | Atualizado: 2026
// ============================================================

const AFFILIATES = {
  // Crédito Consignado
  carrefour_consignado: {
    name: "Carrefour Consignado",
    url: "https://apretailer.com.br/click/6a067c0f2bfa813f282890f5/188661/358914/subaccount",
    type: "CPA",
    category: "consignado"
  },
  // Antecipação FGTS
  juca_fgts: {
    name: "Juca — Antecipação FGTS",
    url: "https://apretailer.com.br/click/6a067c0e2bfa8163f07f0eb3/188162/358914/subaccount",
    type: "CPA",
    category: "fgts"
  },
  credspot_fgts: {
    name: "Credspot — Antecipação FGTS",
    url: "https://apretailer.com.br/click/6a067c0e2bfa8163ea1cf292/186580/358914/subaccount",
    type: "CPA",
    category: "fgts"
  },
  consigmais_fgts: {
    name: "Consigmais — FGTS",
    url: "https://apretailer.com.br/click/6a067c0c2bfa813f2e6451c4/184986/358914/subaccount",
    type: "CPA",
    category: "fgts"
  },
  // Garantia de Veículo
  bv_veiculo: {
    name: "Banco BV — Garantia de Veículo",
    url: "https://apretailer.com.br/click/6a067c0f2bfa8163ea1cf294/188286/358914/subaccount",
    type: "CPL",
    category: "veiculo"
  },
  santander_automovel: {
    name: "Santander CPAuto",
    url: "https://apretailer.com.br/click/6a067c0f2bfa8163e435c25b/188625/358914/subaccount",
    type: "CPA",
    category: "veiculo"
  },
  juros_baixos_veiculo: {
    name: "Juros Baixos — Garantia",
    url: "https://apretailer.com.br/click/6a067c0e2bfa8163e435c253/183013/358914/subaccount",
    type: "CPA",
    category: "veiculo"
  },
  // Empréstimo Pessoal / Negativados
  supersim: {
    name: "SuperSim — Garantia Celular",
    url: "https://apretailer.com.br/click/6a067c102bfa8163f07f0eb5/184363/358914/subaccount",
    type: "CPA",
    category: "negativados"
  },
  velotax: {
    name: "Velotax",
    url: "https://apretailer.com.br/click/6a067c0e2bfa8163ea1cf293/188130/358914/subaccount",
    type: "CPA",
    category: "negativados"
  },
  hiper_cash: {
    name: "Hiper Cash",
    url: "https://apretailer.com.br/click/6a067c0e2bfa813f282890f4/182687/358914/subaccount",
    type: "CPA",
    category: "negativados"
  },
  upp_emprestimos: {
    name: "UP.P Empréstimos",
    url: "https://apretailer.com.br/click/6a067c0e2bfa8132653a81a2/179925/358914/subaccount",
    type: "CPA",
    category: "negativados"
  },
  bom_pra_credito: {
    name: "BomPraCrédito",
    url: "https://apretailer.com.br/click/6a067c0e2bfa8163e435c255/148693/358914/subaccount",
    type: "CPA",
    category: "negativados"
  },
  // Cartão de Crédito
  santander_cartao: {
    name: "Santander Cartão PF",
    url: "https://apretailer.com.br/click/6a067c0c2bfa813f4604f6b9/188413/358914/subaccount",
    type: "CPA",
    category: "cartao"
  }
};

// Retorna URL de um afiliado pelo ID
function getAffiliateUrl(id) {
  return AFFILIATES[id] ? AFFILIATES[id].url : '#';
}

// Preenche automaticamente todos os elementos com data-affiliate
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('[data-affiliate]').forEach(function(el) {
    var id = el.getAttribute('data-affiliate');
    if (AFFILIATES[id]) {
      el.href = AFFILIATES[id].url;
      el.target = '_blank';
      el.rel = 'noopener sponsored';
      el.removeAttribute('disabled');
      el.classList.remove('disabled');
    }
  });
});
