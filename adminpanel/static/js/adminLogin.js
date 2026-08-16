
/* =========================================================
   TRUSTYSHOP ADMIN LOGIN JAVASCRIPT
   COSMIC • BLUE • GLASS • MODERN • STABLE
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       ELEMENTS
    ===================================================== */

    const body =
        document.body;

    const loginForm =
        document.querySelector(
            ".admin-login-card form"
        );

    const submitButton =
        loginForm?.querySelector(
            'button[type="submit"]'
        );

    const passwordInput =
        document.querySelector(
            'input[name="password"]'
        );

    const togglePassword =
        document.querySelector(
            ".toggle-password"
        );


    /* =====================================================
       DEVICE
    ===================================================== */

    const canHover =
        window.matchMedia(
            "(hover: hover) and (pointer: fine)"
        ).matches;


    /* =====================================================
       RANDOM
    ===================================================== */

    function random(min, max) {

        return Math.random() *
            (max - min) +
            min;

    }


    /* =====================================================
       BASIC BODY
    ===================================================== */

    if (body) {

        body.style.margin =
            "0";

    }


    /* =====================================================
       CREATE PARTICLES CONTAINER
    ===================================================== */

    let particles =
        document.getElementById(
            "particles"
        );

    if (!particles) {

        particles =
            document.createElement(
                "div"
            );

        particles.id =
            "particles";

        body.appendChild(
            particles
        );

    }


    /* =====================================================
       CREATE STARS CONTAINER
    ===================================================== */

    let stars =
        document.getElementById(
            "stars"
        );

    if (!stars) {

        stars =
            document.createElement(
                "div"
            );

        stars.id =
            "stars";

        body.appendChild(
            stars
        );

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
            i < 85;
            i++
        ) {

            const particle =
                document.createElement(
                    "span"
                );


            const size =
                random(2, 4.5);


            particle.style.width =
                `${size}px`;

            particle.style.height =
                `${size}px`;


            particle.style.left =
                `${random(0, 100)}%`;

            particle.style.top =
                `${random(0, 100)}%`;


            particle.style.opacity =
                random(0.15, 0.7);


            particle.style.animationDuration =
                `${random(8, 20)}s`;


            particle.style.animationDelay =
                `${random(0, 10)}s`;


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
                random(0.30, 0.60);

        }, 1400);

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
            "-160px";


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
        5000
    );


    /* =====================================================
       CURSOR GLOW
    ===================================================== */

    if (
        canHover &&
        body
    ) {

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
       PASSWORD SHOW / HIDE
    ===================================================== */

    if (
        passwordInput &&
        togglePassword
    ) {

        togglePassword.addEventListener(
            "click",
            () => {

                const showing =
                    passwordInput.type ===
                    "text";


                passwordInput.type =
                    showing
                        ? "password"
                        : "text";


                const icon =
                    togglePassword.querySelector(
                        "i"
                    );


                if (icon) {

                    icon.classList.toggle(
                        "fa-eye",
                        showing
                    );

                    icon.classList.toggle(
                        "fa-eye-slash",
                        !showing
                    );

                }


                togglePassword.setAttribute(
                    "aria-label",
                    showing
                        ? "Show password"
                        : "Hide password"
                );


                passwordInput.focus();

            }
        );

    }


    /* =====================================================
       BUTTON RIPPLE
    ===================================================== */

    if (submitButton) {

        submitButton.addEventListener(
            "click",
            (event) => {

                if (
                    submitButton.disabled
                ) {

                    return;

                }


                const rect =
                    submitButton.getBoundingClientRect();


                const ripple =
                    document.createElement(
                        "span"
                    );


                ripple.className =
                    "ripple";


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
                    event.clientX -
                    rect.left;


                const y =
                    event.clientY -
                    rect.top;


                ripple.style.left =
                    `${x - size / 2}px`;


                ripple.style.top =
                    `${y - size / 2}px`;


                submitButton.appendChild(
                    ripple
                );


                setTimeout(() => {

                    ripple.remove();

                }, 700);

            }
        );

    }


    /* =====================================================
       INPUT SHINE
    ===================================================== */

    if (canHover) {

        const inputs =
            document.querySelectorAll(
                ".form-group input"
            );


        inputs.forEach(
            (input) => {

                input.addEventListener(
                    "focus",
                    () => {

                        input.parentElement
                            ?.classList.add(
                                "active"
                            );

                    }
                );


                input.addEventListener(
                    "blur",
                    () => {

                        input.parentElement
                            ?.classList.remove(
                                "active"
                            );

                    }
                );

            }
        );

    }


    /* =====================================================
       LOGIN SUBMIT
    ===================================================== */

    if (
        loginForm &&
        submitButton
    ) {

        loginForm.addEventListener(
            "submit",
            (event) => {

                const username =
                    loginForm.querySelector(
                        'input[name="username"]'
                    );


                const password =
                    loginForm.querySelector(
                        'input[name="password"]'
                    );


                /* -----------------------------------------
                   USERNAME VALIDATION
                ----------------------------------------- */

                if (
                    !username?.value.trim()
                ) {

                    event.preventDefault();

                    username?.focus();

                    return;

                }


                /* -----------------------------------------
                   PASSWORD VALIDATION
                ----------------------------------------- */

                if (
                    !password?.value
                ) {

                    event.preventDefault();

                    password?.focus();

                    return;

                }


                /* -----------------------------------------
                   LOADING STATE
                ----------------------------------------- */

                submitButton.disabled =
                    true;


                submitButton.innerHTML = `
                    <i class="fa-solid fa-spinner fa-spin"></i>
                    <span>Signing in...</span>
                `;

            }
        );

    }


    /* =====================================================
       AUTO FOCUS USERNAME
    ===================================================== */

    const usernameInput =
        document.querySelector(
            'input[name="username"]'
        );


    if (usernameInput) {

        setTimeout(() => {

            usernameInput.focus();

        }, 500);

    }


    /* =====================================================
       MESSAGE ANIMATION
    ===================================================== */

    const messages =
        document.querySelectorAll(
            ".admin-message"
        );


    messages.forEach(
        (message) => {

            message.addEventListener(
                "click",
                () => {

                    message.style.opacity =
                        "0";

                    message.style.transform =
                        "translateY(-5px)";


                    setTimeout(() => {

                        message.remove();

                    }, 250);

                }
            );

        }
    );

});

