/*==================================================
    WITHDRAW PAGE
==================================================*/

document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    const submitBtn = document.querySelector(".withdraw-btn");

    const amountInput = document.querySelector("#id_amount");

    const phoneInput = document.querySelector("#id_receiver_phone");

    /*==========================================
        AUTO FOCUS
    ==========================================*/

    if (amountInput) {

        amountInput.focus();

    }

    /*==========================================
        PHONE NUMBER
    ==========================================*/

    if (phoneInput) {

        phoneInput.addEventListener("input", function () {

            this.value = this.value.replace(/[^0-9]/g, "");

        });

    }

    /*==========================================
        FORM SUBMIT
    ==========================================*/

    if (form) {

        form.addEventListener("submit", function (e) {

            const amount = parseFloat(amountInput.value);

            if (isNaN(amount) || amount <= 0) {

                e.preventDefault();

                alert("Please enter a valid withdrawal amount.");

                amountInput.focus();

                return;

            }

            submitBtn.classList.add("loading");

            submitBtn.disabled = true;

            submitBtn.innerHTML = `
                <i class="fa-solid fa-spinner"></i>
                Processing...
            `;

        });

    }

});



