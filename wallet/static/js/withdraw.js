/*==================================================
    WITHDRAW PAGE
==================================================*/

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("withdrawForm");

    const submitBtn = document.querySelector(".withdraw-btn");

    const amountInput = document.getElementById("id_amount");

    const phoneInput = document.getElementById("id_receiver_phone");

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

            this.value = this.value
                .trim()
                .replace(/[^0-9]/g, "");

        });

    }

    /*==========================================
        AMOUNT INPUT
    ==========================================*/

    if (amountInput) {

        amountInput.addEventListener("input", function () {

            this.value = this.value.replace(/[^0-9]/g, "");

        });

    }

    /*==========================================
        SUBMIT BUTTON LOADING
    ==========================================*/

    if (form && submitBtn) {

        form.addEventListener("submit", function () {

            // Prevent double clicking
            if (submitBtn.disabled) {
                return;
            }

            submitBtn.disabled = true;

            submitBtn.classList.add("loading");

            submitBtn.innerHTML = `
                <i class="fa-solid fa-spinner fa-spin"></i>
                Processing...
            `;

        });

    }

    console.log("Withdraw page loaded successfully.");

});