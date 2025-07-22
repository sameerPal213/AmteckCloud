document.getElementById('menuButton').addEventListener('click', function() {
    toggleSideMenu(this);
});

function toggleSideMenu(button) {
    var sideMenu = document.getElementById('sideMenu');


    if (parseInt(sideMenu.style.left) < 0 || sideMenu.style.left == '') {
        sideMenu.style.left = '10px';
        button.innerHTML = '&#10006;';
    } else {
        sideMenu.style.left = - sideMenu.offsetWidth - 50 + 'px';
        button.innerHTML = '&#9776;';
    }
}

function toggleChildMenu(button) {
    var childMenu = button.parentElement.nextElementSibling;
    var isOpen = childMenu.style.display === 'none' || childMenu.style.display === '';
    childMenu.style.display = isOpen ? 'inline-block' : 'none';
    button.innerHTML = isOpen ? '-' : '+';

    // save state to localStorage
    var menuId = button.parentElement.parentElement.dataset.menuId;
    localStorage.setItem('menu_' + menuId, isOpen ? 'open' : 'closed');
}

function restoreMenuState() {
    var menus = document.querySelectorAll('.child-menu');
    menus.forEach(function (menu) {
        var menuId = menu.parentElement.dataset.menuId;
        var state = localStorage.getItem('menu_' + menuId);
        if (state === 'open') {
            var button = menu.previousElementSibling.querySelector('.toggle-button');
            menu.style.display = 'inline-block';
            button.innerHTML = '-';
        }
    });
}

function checkMenuLocation() {
    var sideMenu = document.getElementById('sideMenu');
    var menuButton = document.getElementById('menuButton');

    menuCoversButton = sideMenu.offsetLeft + sideMenu.offsetWidth > menuButton.offsetLeft;
    menuWillCoverButton = sideMenu.offsetLeft < 0 && 10 + sideMenu.offsetWidth > menuButton.offsetLeft
    sideMenu.style.marginTop = menuCoversButton || menuWillCoverButton ? '80px' : '10px';
}

// Restore menu state on page load
document.addEventListener('DOMContentLoaded', restoreMenuState);
// Check menu location on page load and move
document.addEventListener('DOMContentLoaded', checkMenuLocation)
document.getElementById('sideMenu').addEventListener('transitionend', checkMenuLocation);
