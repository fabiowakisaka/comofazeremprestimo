// Configurações Globais
const ADSENSE_ID = "ca-pub-8996333447529356";
const ANALYTICS_ID = "G-CJ3H6M1SQ8";

// Injeção do Google Analytics
(function() {
    var ga = document.createElement('script');
    ga.async = true;
    ga.src = 'https://www.googletagmanager.com/gtag/js?id=' + ANALYTICS_ID;
    document.head.appendChild(ga);

    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', ANALYTICS_ID);
})();

// Injeção do AdSense
(function() {
    var ad = document.createElement('script');
    ad.async = true;
    ad.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" + ADSENSE_ID;
    ad.crossOrigin = "anonymous";
    document.head.appendChild(ad);
})();
