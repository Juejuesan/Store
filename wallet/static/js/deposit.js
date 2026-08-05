/*==================================================
    DEPOSIT PAGE
==================================================*/

document.addEventListener("DOMContentLoaded", () => {

    initImagePreview();

    initDragAndDrop();

    // initFormValidation();

    initSubmitLoading();

});


/*==================================================
    IMAGE PREVIEW
==================================================*/

function initImagePreview() {

    const input = document.querySelector(
        'input[type="file"]'
    );

    const preview = document.getElementById(
        "previewImage"
    );

    if (!input || !preview)
        return;

    input.addEventListener("change", function () {

        const file = this.files[0];

        if (!file)
            return;

        const reader = new FileReader();

        reader.onload = function (e) {

            preview.src = e.target.result;

            preview.classList.remove("d-none");

        };

        reader.readAsDataURL(file);

    });

}


/*==================================================
    DRAG & DROP
==================================================*/

function initDragAndDrop() {

    const uploadBox = document.querySelector(
        ".upload-box"
    );

    const input = document.querySelector(
        'input[type="file"]'
    );

    if (!uploadBox || !input)
        return;

    uploadBox.addEventListener("dragover", function (e) {

        e.preventDefault();

        uploadBox.classList.add(
            "dragover"
        );

    });

    uploadBox.addEventListener("dragleave", function () {

        uploadBox.classList.remove(
            "dragover"
        );

    });

    uploadBox.addEventListener("drop", function (e) {

        e.preventDefault();

        uploadBox.classList.remove(
            "dragover"
        );

        input.files = e.dataTransfer.files;

        input.dispatchEvent(
            new Event("change")
        );

    });

}


/*==================================================
    AMOUNT FORMAT
==================================================*/

const amountInput = document.querySelector(
    'input[name="amount"]'
);

if (amountInput) {

    amountInput.addEventListener("input", function () {

        this.value = this.value.replace(
            /[^0-9]/g,
            ""
        );

    });

}


/*==================================================
    TRANSACTION ID
==================================================*/

const txInput = document.querySelector(
    'input[name="transaction_id"]'
);

if (txInput) {

    txInput.addEventListener("input", function () {

        this.value = this.value.replace(
            /\s/g,
            ""
        );

    });

}
/*==================================================
    SUBMIT LOADING
==================================================*/

function initSubmitLoading() {

    const form = document.getElementById("depositForm");
    const button = document.getElementById("submitBtn");

    if (!form || !button) return;

    form.addEventListener("submit", function () {

        // Disable button
        button.disabled = true;

        // Add loading style
        button.classList.add("loading");

        // Change button text
        button.innerHTML = `
            <i class="fa-solid fa-spinner fa-spin"></i>
            Submitting...
        `;

    });

}
/*==================================================
    RIPPLE EFFECT
==================================================*/

const submitButton = document.getElementById(
    "submitBtn"
);

if (submitButton) {

    submitButton.addEventListener("click", function (e) {

        const ripple = document.createElement(
            "span"
        );

        ripple.className = "ripple";

        const rect = this.getBoundingClientRect();

        ripple.style.left =
            (e.clientX - rect.left) + "px";

        ripple.style.top =
            (e.clientY - rect.top) + "px";

        this.appendChild(ripple);

        setTimeout(() => {

            ripple.remove();

        }, 600);

    });

}


/*==================================================
    PREVIEW ANIMATION
==================================================*/

const previewImage = document.getElementById(
    "previewImage"
);

if (previewImage) {

    previewImage.addEventListener("load", function () {

        this.style.opacity = "0";

        this.style.transform = "translateY(20px)";

        setTimeout(() => {

            this.style.transition =
                "all .4s ease";

            this.style.opacity = "1";

            this.style.transform =
                "translateY(0)";

        }, 50);

    });

}


/*==================================================
    AUTO HIDE ALERTS
==================================================*/

const alerts = document.querySelectorAll(
    ".alert"
);

alerts.forEach(alert => {

    setTimeout(() => {

        alert.style.transition =
            "opacity .5s";

        alert.style.opacity = "0";

        setTimeout(() => {

            alert.remove();

        }, 500);

    }, 4000);

});


/*==================================================
    PAGE READY
==================================================*/

console.log(
    "Deposit page loaded successfully."
);
