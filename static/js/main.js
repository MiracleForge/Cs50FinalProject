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


function configIconsConfig(ad_conditions, ad_type) {
    var conditionImagePath;
    var typeImagePath;

    switch (ad_conditions) {
        case 'New':
            conditionImagePath = '../static/assets/image/icons8-new-50.png';
            break;
        case 'Used-Excellent':
            conditionImagePath = '../static/assets/image/icons8-used-50.png';
            break;
        case 'Used - Good':
            conditionImagePath = '../static/assets/image/icons8-used-product-64.png';
            break;
        case 'Refurbished':
            conditionImagePath = '../static/assets/image/icons8-refurbished.png';
            break;
        case 'Faulty':
            conditionImagePath = '../static/assets/image/icons8-reject-50.png';
            break;
    }

            // Choose image path based on ad_type
            switch (ad_type) {
                // Add cases for different ad types and set typeImagePath accordingly
                case 'Video Game Consoles,':
                    typeImagePath = '../static/assets/image/icons8-consoles.png';
                    break;
                case 'Games':
                    typeImagePath = '../static/assets/image/icons8-games-folder-64.png';
                    break;
                case 'Controls':
                    typeImagePath = '../static/assets/image/icons8-consoles.png';
                    break;
                case 'Acessories':
                    typeImagePath = '../static/assets/image/icons8-usb-50.png';
                    break;
                case 'Others':
                    typeImagePath = '../static/assets/image/icons8-where-what-quest-50.png';
                    break;
                case 'Beauty and Health,':
                    typeImagePath = '../static/assets/image/icons8-health-50.png';
                    break;
                case 'Clothing':
                    typeImagePath = '../static/assets/image/icons8-t-shirt-24.png';
                    break;
                case 'Bags, Suitcases, and Backpacks':
                    typeImagePath = '../static/assets/image/icons8-backpack-50.png';
                    break;
                case 'Footwear':
                    typeImagePath = '../static/assets/image/icons8-backpack-50.png';
                    break;
                case 'Pet Houses and Beds,':
                    typeImagePath = '../static/assets/image/icons8-pet-bed-64.png';
                    break;
                case 'Pet Toys':
                    typeImagePath = '../static/assets/image/icons8-dog-jump-64.png';
                    break;
                case 'Feeding and Bowls':
                    typeImagePath = '../static/assets/image/icons8-dog-bowl.png';
                    break;
                case 'Clothing and Accessories':
                    typeImagePath = '../static/assets/image/icons8-scratching-post-50.png';
                    break;
                case 'Pet Carriers':
                    typeImagePath = '../static/assets/image/icons8-pet-carrier-48.png';
                    break;
                case 'Hygiene and Health Products':
                    typeImagePath = '../static/assets/image/icons8-health-50.png';
                    break;
                case 'Cages and Aquariums':
                    typeImagePath = '../static/assets/image/icons8-aquarium-50.png';
                    break;
                case 'Training Equipment':
                    typeImagePath = '../static/assets/image/icons8-dog-training-50.png';
                    break;
                case 'Specific Cat Products':
                    typeImagePath = '../static/assets/image/icons8-cat-50.png';
                    break;
                case 'NootBook and Laptops':
                    typeImagePath = '../static/assets/image/icons8-multiple-devices-32.png';
                    break;
                case 'Pcs and Desktops':
                    typeImagePath = '../static/assets/image/icons8-computer-64.png';
                    break;
                case 'Cellphones':
                    typeImagePath = '../static/assets/image/icons8-cellphones-64.png';
                    break;
                case 'Prints':
                    typeImagePath = '../static/assets/image/icons8-printer-24.png';
                    break;
                case 'TVs':
                    typeImagePath = '../static/assets/image/icons8-printer-24.png';
                    break;
                case 'Cameras':
                    typeImagePath = '../static/assets/image/icons8-cameras-50.png';
                    break;
                case 'Dvd Players':
                    typeImagePath = '../static/assets/image/icons8-dvd-logo-50.png';
                    break;
                case 'Furniture':
                    typeImagePath = '../static/assets/image/icons8-furniture-50.png';
                    break;
                case 'Home Appliances':
                    typeImagePath = '../static/assets/image/icons8-home-appliances-58.png';
                    break;
                case 'Building Materials and Garden':
                    typeImagePath = '../static/assets/image/icons8-construction-materials-64.png';
                    break;
                case 'Household Utilities':
                    typeImagePath = '../static/assets/image/icons8-utilities-50.png';
                    break;
                case 'Decorative Objects':
                    typeImagePath = '../static/assets/image/icons8-humidifier-80.png';
                    break;
                case 'Small Appliances':
                    typeImagePath = '../static/assets/image/icons8-home-appliances-58.png';
                    break;
                case 'Eletrodomestics':
                    typeImagePath = '../static/assets/image/icons8-tumble-dryer-100(1).png';
                    break;
            
            }
    
            var iconsConditions = document.getElementsByClassName('iconsConditions');
            var iconsType = document.getElementsByClassName('iconsType');
    
            for (var i = 0; i < iconsConditions.length; i++) {
                iconsConditions[i].src = conditionImagePath;
            }
    
            // Use typeImagePath as needed
            for (var i = 0; i < iconsType.length; i++) {
                iconsType[i].src = typeImagePath;
            }
        }










