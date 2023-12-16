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


function configureImage(type) {
    var imagePath;

    switch (type) {
        case 'RealState':
                imagePath = '../static/assets/image/icons8-houses-96.png';
                break;
            case 'PreOwnedCars':
                imagePath = '../static/assets/image/icons8-traffic-jam-96 (3).png';
                break;
            case 'HomeEssentials':
                imagePath = '../static/assets/image/icons8-lampshade-64 (1).png';
                break;
            case 'TechEssentials':
                imagePath = '../static/assets/image/icons8-laptop-96.png';
                break;
            case 'MusicalInstrument':
                imagePath = '../static/assets/image/icons8-musical-notes-100.png';
                break;
            case 'Children_Items_Toys':
                imagePath = '../static/assets/image/icons8-toys-64.png';
                break;
            case 'Pets':
                imagePath = '../static/assets/image/icons8-pets-100.png';
                break;
            case 'Commerce_office':
                imagePath = '../static/assets/image/icons8-office-100.png';
                break;
            case 'Fashion_Beauty':
                imagePath = '../static/assets/image/icons8-fashion-100.png';
                break;
            case 'Games':
                imagePath = '../static/assets/image/icons8-controller-100.png';
                break;
            default:
                imagePath = '../static/assets/favicon/favicon.png';
        }

    var categoryImage = document.getElementById('categoryImage');
    if (categoryImage) {
        categoryImage.src = imagePath;
    } else {
        console.error('Image Not Found.');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var dependencyList = document.getElementById('dependencyList');
    var detail_icons_list = dependencyList.querySelectorAll('.detail_icons');

    for (var i = 0; i < detail_icons_list.length; i++) {
        var content_detal = detail_icons_list[i].nextSibling.textContent.trim();
        configureIcons(content_detal, detail_icons_list[i]);
    }
});

function configureIcons(content_detal, element) {
    var imagePath;

    switch (content_detal) {
        case 'air conditioning':
            imagePath = '../static/assets/image/icons8-air-quality-50.png';
            break;
        case 'walk-in closets':
            imagePath = '../static/assets/image/icons8-cabinet-64.png';
            break;
        case 'laundry room':
            imagePath = '../static/assets/image/icons8-laundry-room-62.png';
            break;
        case "maid's room":
            imagePath = '../static/assets/image/icons8-room-100.png';
            break;
        case "balcony":
            imagePath = '../static/assets/image/icons8-balcony-50.png';
            break;
        case "kitchen cabinets":
            imagePath = '../static/assets/image/icons8-kitchen-room-100.png';
            break;
        case "grill / barbecue":
            imagePath = '../static/assets/image/icons8-grill-60.png';
            break;

        default:
            imagePath = '../static/assets/favicon/favicon.png';
    }

    element.src = imagePath;
}











