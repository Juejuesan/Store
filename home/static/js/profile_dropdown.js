document.addEventListener('click', function(e) {
    const trigger = e.target.closest('.profile-trigger-link');
    const allMenus = document.querySelectorAll('.profile-menu-card');

    if (trigger) {
        e.preventDefault();
        e.stopPropagation();

        const container = trigger.closest('.profile-dropdown-container');
        const currentMenu = container ? container.querySelector('.profile-menu-card') : null;

        allMenus.forEach(menu => {
            if (menu !== currentMenu) menu.classList.remove('active-dropdown');
        });

        if (currentMenu) {
            currentMenu.classList.toggle('active-dropdown');
        }
    } else {
        if (!e.target.closest('.profile-menu-card')) {
            allMenus.forEach(menu => menu.classList.remove('active-dropdown'));
        }
    }
});