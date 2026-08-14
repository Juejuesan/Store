/* ==========================================================
   TRUSTY SHOP ADMIN PANEL JAVASCRIPT
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* ==========================================================
       LOADER
    ========================================================== */

    const loader = document.getElementById("loader");

    if (loader) {
        window.addEventListener("load", () => {

            setTimeout(() => {
                loader.style.opacity = "0";
                loader.style.visibility = "hidden";
            }, 1200);

        });
    }


    /* ==========================================================
       LIVE CLOCK
    ========================================================== */

    const clock = document.getElementById("liveClock");

    function updateClock() {

        if (!clock) {
            return;
        }

        const now = new Date();

        const options = {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit"
        };

        clock.textContent = now.toLocaleTimeString(
            [],
            options
        );
    }

    updateClock();

    setInterval(updateClock, 1000);


    /* ==========================================================
       THEME TOGGLE
    ========================================================== */

    const themeBtn = document.getElementById("themeToggle");

    if (themeBtn) {

        themeBtn.addEventListener("click", () => {

            document.body.classList.toggle("dark");

            const isDarkMode =
                document.body.classList.contains("dark");

            if (isDarkMode) {

                themeBtn.innerHTML =
                    '<i class="fa-solid fa-sun"></i>';

                themeBtn.setAttribute(
                    "title",
                    "Switch to Light Mode"
                );

            } else {

                themeBtn.innerHTML =
                    '<i class="fa-solid fa-moon"></i>';

                themeBtn.setAttribute(
                    "title",
                    "Switch to Dark Mode"
                );
            }

        });

    }


    /* ==========================================================
       SIDEBAR TOGGLE
    ========================================================== */

    const sidebar =
        document.querySelector(".sidebar");

    const toggleBtn =
        document.getElementById("toggle-btn");

    if (toggleBtn && sidebar) {

        toggleBtn.addEventListener("click", () => {

            sidebar.classList.toggle("active");

        });

    }


    /* ==========================================================
       NOTIFICATION PANEL
    ========================================================== */

    const notificationBell =
        document.getElementById("notificationBell");

    const notificationPanel =
        document.getElementById("notificationPanel");

    const closeNotification =
        document.getElementById("closeNotification");


    /* Open notification panel */

    if (notificationBell && notificationPanel) {

        notificationBell.addEventListener("click", () => {

            notificationPanel.classList.add("active");

        });

    }


    /* Close notification panel */

    if (closeNotification && notificationPanel) {

        closeNotification.addEventListener("click", () => {

            notificationPanel.classList.remove("active");

        });

    }


    /* ==========================================================
       CARD HOVER ANIMATION
    ========================================================== */

    const cards =
        document.querySelectorAll(".card");

    cards.forEach((card) => {

        card.addEventListener("mouseenter", () => {

            card.style.transform =
                "transeY(-12px) scale(1.02)";

        });


        card.addEventListener("mouseleave", () => {

            card.style.transform =
                "transeY(0) scale(1)";

        });

    });


    /* ==========================================================
       ANIMATED COUNTERS
    ========================================================== */

    const counters =
        document.querySelectorAll(".counter");

    counters.forEach((counter) => {

        const target =
            Number(counter.getAttribute("data-target"));

        let current = 0;

        counter.textContent = "0";


        function updateCounter() {

            const increment = target / 80;

            if (current < target) {

                current += increment;

                counter.textContent =
                    Math.ceil(current);

                setTimeout(updateCounter, 25);

            } else {

                counter.textContent = target;

            }

        }


        updateCounter();

    });


    /* ==========================================================
       GLOBAL TABLE SEARCH
    ========================================================== */

    const searchInput =
        document.querySelector(".search-box input");

    if (searchInput) {

        searchInput.addEventListener("input", () => {

            const searchValue =
                searchInput.value.toLowerCase().trim();

            const rows =
                document.querySelectorAll("tbody tr");

            rows.forEach((row) => {

                const rowText =
                    row.innerText.toLowerCase();

                row.style.display =
                    rowText.includes(searchValue)
                        ? ""
                        : "none";

            });

        });

    }


    /* ==========================================================
       WALLET SEARCH
    ========================================================== */

    function setupTableSearch(inputId, tableId) {

        const input =
            document.getElementById(inputId);

        const table =
            document.getElementById(tableId);

        if (!input || !table) {
            return;
        }


        const rows =
            table.querySelectorAll("tr");


        input.addEventListener("input", () => {

            const searchValue =
                input.value.toLowerCase().trim();


            rows.forEach((row) => {

                const rowText =
                    row.innerText.toLowerCase();

                row.style.display =
                    rowText.includes(searchValue)
                        ? ""
                        : "none";

            });

        });

    }


    /* Deposit search */

    setupTableSearch(
        "walletSearch",
        "walletTable"
    );


    /* Withdraw search */

    setupTableSearch(
        "withdrawSearch",
        "withdrawTable"
    );


    /* ==========================================================
       SIDEBAR MENU
       Django controls navigation.
    ========================================================== */

    const menuLinks =
        document.querySelectorAll(".menu a");

    menuLinks.forEach((link) => {

        link.addEventListener("click", (event) => {

            const url =
                link.getAttribute("href");

            if (url === "#") {
                event.preventDefault();
            }

        });

    });


    /* ==========================================================
       FLOATING BACKGROUND
    ========================================================== */

    document.addEventListener("mousemove", (event) => {

        const circles =
            document.querySelectorAll(".circle");

        circles.forEach((circle, index) => {

            const speed =
                (index + 1) * 0.01;

            const x =
                (window.innerWidth - event.pageX) * speed;

            const y =
                (window.innerHeight - event.pageY) * speed;

            circle.style.transform =
                `transe(${x}px, ${y}px)`;

        });

    });


    /* ==========================================================
       RIPPLE EFFECT
    ========================================================== */

    const buttons =
        document.querySelectorAll(".btn");

    buttons.forEach((button) => {

        button.addEventListener("click", function (event) {

            const ripple =
                document.createElement("span");

            ripple.classList.add("ripple");

            this.appendChild(ripple);


            const rect =
                this.getBoundingClientRect();

            const x =
                event.clientX - rect.left;

            const y =
                event.clientY - rect.top;


            ripple.style.left =
                `${x}px`;

            ripple.style.top =
                `${y}px`;


            setTimeout(() => {

                ripple.remove();

            }, 600);

        });

    });

});