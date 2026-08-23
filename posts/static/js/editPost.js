// =========================================================
// EDIT POST JAVASCRIPT
// =========================================================

document.addEventListener("DOMContentLoaded", function() {

    /* =====================================================
       APPROVED POST - PRICE & QUANTITY EDIT
    ===================================================== */

    const approvedForm = document.getElementById("approvedEditForm");

    if (approvedForm) {
        approvedForm.addEventListener("submit", function(e) {
            e.preventDefault();

            let isValid = true;

            // Validate all price inputs
            document.querySelectorAll(".price-input").forEach(input => {
                const value = parseInt(input.value);
                if (isNaN(value) || value < 1) {
                    isValid = false;
                    input.style.borderColor = "#dc2626";
                    input.style.boxShadow = "0 0 0 3px rgba(220, 38, 38, 0.1)";
                } else {
                    input.style.borderColor = "#cbd5e1";
                    input.style.boxShadow = "none";
                }
            });

            // Validate all quantity inputs
            document.querySelectorAll(".qty-input").forEach(input => {
                const value = parseInt(input.value);
                if (isNaN(value) || value < 0) {
                    isValid = false;
                    input.style.borderColor = "#dc2626";
                    input.style.boxShadow = "0 0 0 3px rgba(220, 38, 38, 0.1)";
                } else {
                    input.style.borderColor = "#cbd5e1";
                    input.style.boxShadow = "none";
                }
            });

            if (!isValid) {
                alert("Please enter valid prices and quantities.");
                return;
            }

            // Submit form
            const submitBtn = approvedForm.querySelector(".btn-save");
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';

            approvedForm.submit();
        });
    }

    /* =====================================================
       LIVE PRICE UPDATE DISPLAY
    ===================================================== */

    document.querySelectorAll(".price-input").forEach(input => {
        input.addEventListener("input", function() {
            const value = parseInt(this.value);
            if (value > 0) {
                this.style.borderColor = "#10b981";
            } else {
                this.style.borderColor = "#dc2626";
            }
        });
    });

    document.querySelectorAll(".qty-input").forEach(input => {
        input.addEventListener("input", function() {
            const value = parseInt(this.value);
            if (value >= 0) {
                this.style.borderColor = "#10b981";
            } else {
                this.style.borderColor = "#dc2626";
            }
        });
    });

});