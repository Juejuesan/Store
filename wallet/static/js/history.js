/*==================================================
    HISTORY PAGE
==================================================*/

document.addEventListener("DOMContentLoaded", function () {

    const filterButtons = document.querySelectorAll(".filter-btn");

    const rows = document.querySelectorAll(".history-row");

    const searchInput = document.getElementById("historySearch");

    /*==========================================
        FILTER TRANSACTIONS
    ==========================================*/

    filterButtons.forEach(button => {

        button.addEventListener("click", function () {

            filterButtons.forEach(btn => {

                btn.classList.remove("active");

            });

            this.classList.add("active");

            const filter = this.dataset.filter;

            rows.forEach(row => {

                if (
                    filter === "all" ||
                    row.dataset.type === filter
                ) {

                    row.style.display = "";

                } else {

                    row.style.display = "none";

                }

            });

        });

    });

    /*==========================================
        SEARCH
    ==========================================*/

    if (searchInput) {

        searchInput.addEventListener("keyup", function () {

            const keyword = this.value.toLowerCase();

            rows.forEach(row => {

                const text = row.innerText.toLowerCase();

                if (text.includes(keyword)) {

                    row.style.display = "";

                } else {

                    row.style.display = "none";

                }

            });

        });

    }

    /*==========================================
        HOVER ANIMATION
    ==========================================*/

    rows.forEach(row => {

        row.addEventListener("mouseenter", function () {

            this.style.transform = "scale(1.01)";

        });

        row.addEventListener("mouseleave", function () {

            this.style.transform = "scale(1)";

        });

    });

});