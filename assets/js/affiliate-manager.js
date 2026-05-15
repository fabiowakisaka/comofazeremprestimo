const AFFILIATE_LINKS = {
    CARREFOUR: "https://apretailer.com.br/click/6a067c0f2bfa813f282890f5/188661/358914/subaccount",
    JUCA_FGTS: "https://apretailer.com.br/click/6a067c0e2bfa8163f07f0eb3/188162/358914/subaccount",
    SUPERSIM: "https://apretailer.com.br/click/6a067c102bfa8163f07f0eb5/184363/358914/subaccount",
    BV_VEICULO: "https://apretailer.com.br/click/6a067c0f2bfa8163ea1cf294/188286/358914/subaccount",
    SANTANDER_CARD: "https://apretailer.com.br/click/6a067c0c2bfa813f4604f6b9/188413/358914/subaccount"
};

document.addEventListener("DOMContentLoaded", function() {
    // Vincula classes CSS aos links
    const map = {
        '.btn-carrefour': AFFILIATE_LINKS.CARREFOUR,
        '.btn-fgts': AFFILIATE_LINKS.JUCA_FGTS,
        '.btn-supersim': AFFILIATE_LINKS.SUPERSIM,
        '.btn-veiculo': AFFILIATE_LINKS.BV_VEICULO,
        '.btn-santander': AFFILIATE_LINKS.SANTANDER_CARD
    };

    Object.keys(map).forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            el.href = map[selector];
            el.target = "_blank";
            el.rel = "nofollow noopener noreferrer";
        });
    });
});
