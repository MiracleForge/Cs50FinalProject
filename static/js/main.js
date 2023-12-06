// Adiciona um ouvinte de eventos para detectar quando o toggle é mostrado ou ocultado
document.getElementById('main-nav').addEventListener('show.bs.collapse', function () {
    // Verifica se o toogle está sendo mostrado
    if (document.getElementById('main-nav').classList.contains('show')) {
        // Esconde os elementos de Login e Register na primeira navegação
        document.getElementById('login').classList.add('d-none');
        document.getElementById('register').classList.add('d-none');

        // Exibe os elementos de Login e Register na segunda navegação
        document.getElementById('loginMobile').classList.remove('d-none');
        document.getElementById('registerMobile').classList.remove('d-none');
    }
});

document.getElementById('main-nav').addEventListener('hide.bs.collapse', function () {
    // Verifica se o toogle está sendo escondido
    if (!document.getElementById('main-nav').classList.contains('show')) {
        // Exibe os elementos de Login e Register na primeira navegação
        document.getElementById('login').classList.remove('d-none');
        document.getElementById('register').classList.remove('d-none');


        document.getElementById('loginMobile').classList.add('d-none');
        document.getElementById('registerMobile').classList.add('d-none');
    }
});

document.getElementById("announceBtn").addEventListener("click", function() {
    window.location.href = "/announce"

})









