/* =========================================================
TRUSTYSHOP AUTH JAVASCRIPT
LOGIN + REGISTER
MODERN • STABLE • CENTER ALERT
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
/* =====================================================
   ELEMENTS
===================================================== */

const body =
    document.body;

const particles =
    document.getElementById("particles");

const stars =
    document.getElementById("stars");

const profileInput =
    document.getElementById("id_profile_pic");

const previewImage =
    document.getElementById("previewImage");

const password =
    document.getElementById("id_password");

const confirmPassword =
    document.getElementById("id_confirm_password");

const strengthFill =
    document.getElementById("strengthFill");

const strengthText =
    document.getElementById("strengthText");

const registerForm =
    document.querySelector(
        ".register-card form"
    );

const toggleButtons =
    document.querySelectorAll(
        ".toggle-password"
    );

const authButtons =
    document.querySelectorAll(
        ".auth-btn"
    );

const socialButtons =
    document.querySelectorAll(
        ".social-login button"
    );


/* =====================================================
   CENTER ALERT ELEMENTS
===================================================== */

const alertOverlay =
    document.getElementById(
        "authAlert"
    );

const alertCard =
    alertOverlay?.querySelector(
        ".auth-alert"
    );

const alertTitle =
    document.getElementById(
        "authAlertTitle"
    );

const alertMessage =
    document.getElementById(
        "authAlertMessage"
    );

const alertIcon =
    document.getElementById(
        "authAlertIcon"
    );

const alertOk =
    document.getElementById(
        "authAlertOk"
    );


/* =====================================================
   DEVICE
===================================================== */

const canHover =
    window.matchMedia(
        "(hover: hover) and (pointer: fine)"
    ).matches;


/* =====================================================
   BASIC BODY SAFETY
===================================================== */

if (body) {

    body.style.backgroundColor =
        "#020617";

    body.style.color =
        "#ffffff";

    body.style.margin =
        "0";

}


/* =====================================================
   RANDOM NUMBER
===================================================== */

function random(min, max) {

    return Math.random() *
        (max - min) +
        min;

}


/* =====================================================
   PARTICLES
===================================================== */

function createParticles() {

    if (!particles)
        return;

    const fragment =
        document.createDocumentFragment();

    for (
        let i = 0;
        i < 90;
        i++
    ) {

        const particle =
            document.createElement(
                "span"
            );

        const size =
            random(2, 5);

        particle.style.width =
            `${size}px`;

        particle.style.height =
            `${size}px`;

        particle.style.left =
            `${random(0, 100)}%`;

        particle.style.top =
            `${random(0, 100)}%`;

        particle.style.opacity =
            random(0.2, 0.8);

        particle.style.animationDuration =
            `${random(8, 20)}s`;

        particle.style.animationDelay =
            `${random(0, 8)}s`;

        fragment.appendChild(
            particle
        );

    }

    particles.appendChild(
        fragment
    );

}


createParticles();


/* =====================================================
   STAR TWINKLE
===================================================== */

if (stars) {

    setInterval(() => {

        stars.style.opacity =
            random(0.45, 0.85);

    }, 1200);

}


/* =====================================================
   SHOOTING STARS
===================================================== */

function createShootingStar() {

    if (!body)
        return;

    const star =
        document.createElement(
            "div"
        );

    star.className =
        "shooting-star";

    star.style.top =
        `${random(0, 40)}%`;

    star.style.left =
        "-150px";

    star.style.animationDuration =
        `${random(2, 3.5)}s`;

    body.appendChild(
        star
    );

    setTimeout(() => {

        star.remove();

    }, 4000);

}


setInterval(
    createShootingStar,
    4500
);


/* =====================================================
   CURSOR GLOW
===================================================== */

if (canHover && body) {

    const cursorGlow =
        document.createElement(
            "div"
        );

    cursorGlow.className =
        "cursor-glow";

    body.appendChild(
        cursorGlow
    );

    document.addEventListener(
        "mousemove",
        (event) => {

            cursorGlow.style.left =
                `${event.clientX}px`;

            cursorGlow.style.top =
                `${event.clientY}px`;

        }
    );

}


/* =====================================================
   CENTER ALERT SYSTEM
===================================================== */

function getAlertType(level) {

    const value =
        String(level || "")
            .toLowerCase();

    if (
        value.includes("success")
    ) {

        return "success";

    }

    if (
        value.includes("warning")
    ) {

        return "warning";

    }

    if (
        value.includes("info")
    ) {

        return "info";

    }

    return "error";

}


function setAlertIcon(type) {

    if (!alertIcon)
        return;

    alertIcon.className =
        "fa-solid";

    if (type === "success") {

        alertIcon.classList.add(
            "fa-circle-check"
        );

        return;
    }

    if (type === "warning") {

        alertIcon.classList.add(
            "fa-triangle-exclamation"
        );

        return;
    }

    if (type === "info") {

        alertIcon.classList.add(
            "fa-circle-info"
        );

        return;
    }

    alertIcon.classList.add(
        "fa-circle-exclamation"
    );

}


function showAlert(
    message,
    type = "error",
    title = null
) {

    if (
        !alertOverlay ||
        !alertCard ||
        !alertMessage
    ) {

        return;

    }


    const alertType =
        getAlertType(type);


    /* Remove previous state */

    alertCard.classList.remove(
        "error",
        "success",
        "warning",
        "info"
    );


    alertCard.classList.add(
        alertType
    );


    /* Icon */

    setAlertIcon(
        alertType
    );


    /* Title */

    if (alertTitle) {

        if (title) {

            alertTitle.textContent =
                title;

        } else if (
            alertType === "success"
        ) {

            alertTitle.textContent =
                "Success";

        } else if (
            alertType === "warning"
        ) {

            alertTitle.textContent =
                "Warning";

        } else if (
            alertType === "info"
        ) {

            alertTitle.textContent =
                "Information";

        } else {

            alertTitle.textContent =
                "Please check";

        }

    }


    /* Message */

    alertMessage.textContent =
        message;


    /* Show */

    alertOverlay.classList.add(
        "show"
    );

    alertOverlay.setAttribute(
        "aria-hidden",
        "false"
    );


    /* Prevent background scrolling */

    document.body.style.overflow =
        "hidden";


    /* Focus OK */

    setTimeout(() => {

        if (alertOk) {

            alertOk.focus();

        }

    }, 100);

}


function hideAlert() {

    if (!alertOverlay)
        return;


    alertOverlay.classList.remove(
        "show"
    );

    alertOverlay.setAttribute(
        "aria-hidden",
        "true"
    );


    document.body.style.overflow =
        "";

}


/* =====================================================
   OK BUTTON
===================================================== */

if (alertOk) {

    alertOk.addEventListener(
        "click",
        hideAlert
    );

}


/* =====================================================
   ESC KEY
   Optional keyboard support
===================================================== */

document.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Escape" &&
            alertOverlay?.classList.contains(
                "show"
            )
        ) {

            hideAlert();

        }

    }
);


/* =====================================================
   DJANGO MESSAGES
===================================================== */

const djangoMessages =
    document.querySelectorAll(
        "#djangoMessages .django-message"
    );


djangoMessages.forEach(
    (messageElement) => {

        const message =
            messageElement.textContent
                .trim();

        const level =
            messageElement.dataset.level ||
            "error";


        if (message) {

            showAlert(
                message,
                level
            );

        }

    }
);


/* =====================================================
   FORM ERRORS
===================================================== */

const formErrors =
    document.querySelectorAll(
        "#formErrors .form-error"
    );


if (formErrors.length > 0) {

    const errors = [];


    formErrors.forEach(
        (errorElement) => {

            const message =
                errorElement.textContent
                    .trim();

            if (
                message &&
                !errors.includes(
                    message
                )
            ) {

                errors.push(
                    message
                );

            }

        }
    );


    if (errors.length > 0) {

        showAlert(
            errors.join("\n"),
            "error",
            "Please check your information"
        );

    }

}


/* =====================================================
   PROFILE IMAGE PREVIEW
===================================================== */

if (
    profileInput &&
    previewImage
) {

    profileInput.addEventListener(
        "change",
        (event) => {

            const file =
                event.target.files?.[0];

            if (!file)
                return;


            if (
                !file.type.startsWith(
                    "image/"
                )
            ) {

                profileInput.value = "";

                showAlert(
                    "Please select a valid image file.",
                    "error",
                    "Invalid Image"
                );

                return;

            }


            previewImage.style.opacity =
                "0.3";

            previewImage.style.transform =
                "scale(0.85)";


            const reader =
                new FileReader();


            reader.onload =
                (loadEvent) => {

                    previewImage.src =
                        loadEvent.target.result;

                    requestAnimationFrame(
                        () => {

                            previewImage.style.opacity =
                                "1";

                            previewImage.style.transform =
                                "scale(1)";

                        }
                    );

                };


            reader.readAsDataURL(
                file
            );

        }
    );

}


/* =====================================================
   PASSWORD SHOW / HIDE
===================================================== */

toggleButtons.forEach(
    (button) => {

        button.addEventListener(
            "click",
            () => {

                const box =
                    button.closest(
                        ".password-box"
                    );

                if (!box)
                    return;


                const input =
                    box.querySelector(
                        "input"
                    );

                const icon =
                    button.querySelector(
                        "i"
                    );

                if (!input)
                    return;


                const showPassword =
                    input.type ===
                    "password";


                input.type =
                    showPassword
                        ? "text"
                        : "password";


                button.setAttribute(
                    "aria-label",
                    showPassword
                        ? "Hide password"
                        : "Show password"
                );


                if (icon) {

                    icon.classList.toggle(
                        "fa-eye",
                        showPassword
                    );

                    icon.classList.toggle(
                        "fa-eye-slash",
                        !showPassword
                    );

                }

            }
        );

    }
);


/* =====================================================
   PASSWORD STRENGTH
===================================================== */

function updatePasswordStrength() {

    if (
        !password ||
        !strengthFill ||
        !strengthText
    ) {

        return;

    }


    const value =
        password.value;

    let score = 0;


    if (value.length >= 8)
        score++;

    if (/[A-Z]/.test(value))
        score++;

    if (/[a-z]/.test(value))
        score++;

    if (/[0-9]/.test(value))
        score++;

    if (
        /[!@#$%^&*(),.?":{}|<>]/.test(
            value
        )
    ) {

        score++;

    }


    if (!value) {

        strengthFill.style.width =
            "0";

        strengthText.textContent =
            "Password Strength";

        strengthText.style.color =
            "#9fdcff";

        return;

    }


    const percentage =
        score * 20;


    strengthFill.style.width =
        `${percentage}%`;


    const strength = {

        1: {
            color: "#ef4444",
            text: "Weak Password"
        },

        2: {
            color: "#f97316",
            text: "Fair Password"
        },

        3: {
            color: "#facc15",
            text: "Good Password"
        },

        4: {
            color: "#38bdf8",
            text: "Strong Password"
        },

        5: {
            color: "#22c55e",
            text: "Excellent Password 🔥"
        }

    };


    const result =
        strength[score] ||
        strength[1];


    strengthFill.style.background =
        result.color;

    strengthText.textContent =
        result.text;

    strengthText.style.color =
        result.color;

}


if (password) {

    password.addEventListener(
        "input",
        updatePasswordStrength
    );

    updatePasswordStrength();

}


/* =====================================================
   PASSWORD REQUIREMENTS
   RED → GREEN WHEN SATISFIED
===================================================== */

const passwordLengthRule =
    document.getElementById("passwordLengthRule");

const passwordSpecialRule =
    document.getElementById("passwordSpecialRule");


function updatePasswordRequirements() {

    if (!password)
        return;


    const value =
        password.value;


    /* -------------------------------------------------
       PASSWORD LENGTH
    ------------------------------------------------- */

    if (passwordLengthRule) {

        const lengthIcon =
            passwordLengthRule.querySelector("i");

        if (value.length >= 8) {

            passwordLengthRule.classList.remove(
                "invalid"
            );

            passwordLengthRule.classList.add(
                "valid"
            );

            if (lengthIcon) {

                lengthIcon.classList.remove(
                    "fa-circle-xmark"
                );

                lengthIcon.classList.add(
                    "fa-circle-check"
                );

            }

        } else {

            passwordLengthRule.classList.remove(
                "valid"
            );

            passwordLengthRule.classList.add(
                "invalid"
            );

            if (lengthIcon) {

                lengthIcon.classList.remove(
                    "fa-circle-check"
                );

                lengthIcon.classList.add(
                    "fa-circle-xmark"
                );

            }

        }

    }


    /* -------------------------------------------------
       SPECIAL CHARACTER
    ------------------------------------------------- */

    if (passwordSpecialRule) {

        const specialIcon =
            passwordSpecialRule.querySelector("i");

        const hasSpecialCharacter =
            /[!@#$%^&*(),.?":{}|<>]/.test(value);


        if (hasSpecialCharacter) {

            passwordSpecialRule.classList.remove(
                "invalid"
            );

            passwordSpecialRule.classList.add(
                "valid"
            );

            if (specialIcon) {

                specialIcon.classList.remove(
                    "fa-circle-xmark"
                );

                specialIcon.classList.add(
                    "fa-circle-check"
                );

            }

        } else {

            passwordSpecialRule.classList.remove(
                "valid"
            );

            passwordSpecialRule.classList.add(
                "invalid"
            );

            if (specialIcon) {

                specialIcon.classList.remove(
                    "fa-circle-check"
                );

                specialIcon.classList.add(
                    "fa-circle-xmark"
                );

            }

        }

    }

}


/* -----------------------------------------------------
   UPDATE WHILE TYPING
----------------------------------------------------- */

if (password) {

    password.addEventListener(
        "input",
        updatePasswordRequirements
    );

    updatePasswordRequirements();

}


/* =====================================================
   CONFIRM PASSWORD
===================================================== */

function checkPasswordMatch() {

    if (
        !password ||
        !confirmPassword
    ) {

        return;

    }


    if (!confirmPassword.value) {

        confirmPassword.style.borderColor =
            "";

        confirmPassword.style.boxShadow =
            "";

        return;

    }


    const matches =
        password.value ===
        confirmPassword.value;


    confirmPassword.style.borderColor =
        matches
            ? "#22c55e"
            : "#ef4444";


    confirmPassword.style.boxShadow =
        matches
            ? "0 0 20px rgba(34, 197, 94, 0.25)"
            : "0 0 20px rgba(239, 68, 68, 0.25)";

}


if (
    password &&
    confirmPassword
) {

    password.addEventListener(
        "input",
        checkPasswordMatch
    );

    confirmPassword.addEventListener(
        "input",
        checkPasswordMatch
    );

}


/* =====================================================
   BUTTON RIPPLE
===================================================== */

authButtons.forEach(
    (button) => {

        button.addEventListener(
            "click",
            (event) => {

                if (button.disabled)
                    return;


                const ripple =
                    document.createElement(
                        "span"
                    );

                ripple.className =
                    "ripple";


                const rect =
                    button.getBoundingClientRect();


                const size =
                    Math.max(
                        rect.width,
                        rect.height
                    );


                ripple.style.width =
                    `${size}px`;

                ripple.style.height =
                    `${size}px`;


                const x =
                    event.clientX ||
                    rect.left +
                    rect.width / 2;


                const y =
                    event.clientY ||
                    rect.top +
                    rect.height / 2;


                ripple.style.left =
                    `${x - rect.left - size / 2}px`;

                ripple.style.top =
                    `${y - rect.top - size / 2}px`;


                button.appendChild(
                    ripple
                );


                setTimeout(
                    () => {

                        ripple.remove();

                    },
                    700
                );

            }
        );

    }
);


/* =====================================================
   REGISTER FORM VALIDATION
===================================================== */

if (registerForm) {

    registerForm.addEventListener(
        "submit",
        (event) => {

            const terms =
                registerForm.querySelector(
                    "#terms, " +
                    "#id_terms, " +
                    'input[name="terms"]'
                );


            /* Terms */

            if (
                terms &&
                !terms.checked
            ) {

                event.preventDefault();

                showAlert(
                    "Please accept the Terms & Conditions before creating your account.",
                    "warning",
                    "Terms Required"
                );

                terms.focus();

                return;

            }


            /* Password confirmation */

            if (
                password &&
                confirmPassword &&
                password.value !==
                confirmPassword.value
            ) {

                event.preventDefault();

                showAlert(
                    "Your passwords do not match. Please enter the same password in both fields.",
                    "error",
                    "Password Mismatch"
                );

                confirmPassword.focus();

                return;

            }


            /* Submit */

            const button =
                registerForm.querySelector(
                    ".auth-btn"
                );


            if (!button)
                return;


            button.disabled =
                true;

            button.innerHTML = `
                <i class="fa-solid fa-spinner fa-spin"></i>
                <span>Creating Account...</span>
            `;

        }
    );

}


/* =====================================================
   INPUT HOVER
===================================================== */

if (canHover) {

    const inputBoxes =
        document.querySelectorAll(
            ".input-box, .password-box"
        );


    inputBoxes.forEach(
        (box) => {

            box.addEventListener(
                "mouseenter",
                () => {

                    box.classList.add(
                        "shine"
                    );

                }
            );


            box.addEventListener(
                "mouseleave",
                () => {

                    box.classList.remove(
                        "shine"
                    );

                }
            );

        }
    );


    socialButtons.forEach(
        (button) => {

            button.addEventListener(
                "mouseenter",
                () => {

                    button.classList.add(
                        "shine"
                    );

                }
            );


            button.addEventListener(
                "mouseleave",
                () => {

                    button.classList.remove(
                        "shine"
                    );

                }
            );

        }
    );

}


/* =====================================================
   RESET OTP FORM
===================================================== */

const resetOtpForm =
    document.getElementById(
        "resetOtpForm"
    );

const resetOtpBtn =
    document.getElementById(
        "resetOtpBtn"
    );

const otpInput =
    document.getElementById(
        "id_otp"
    );

if (otpInput) {

    otpInput.setAttribute(
        "maxlength",
        "6"
    );

    otpInput.addEventListener(
        "input",
        () => {

            otpInput.value =
                otpInput.value
                    .replace(/\D/g, "")
                    .slice(0, 6);

        }
    );

}

if (
    resetOtpForm &&
    resetOtpBtn
) {

    resetOtpForm.addEventListener(
        "submit",
        () => {

            resetOtpBtn.disabled =
                true;

            resetOtpBtn.innerHTML = `
                <span class="reset-otp-btn-content">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                    <span>Verifying...</span>
                </span>
            `;

        }
    );

}
/* =====================================================
   END
===================================================== */


});
