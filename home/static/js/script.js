/* =========================================================
   TRUSTYSHOP HOME PAGE JAVASCRIPT
   MODERN • STABLE • RESPONSIVE • CLEAN
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       1. NAVBAR SCROLL EFFECT
    ===================================================== */

    const navbar = document.querySelector(".cute-navbar");

    const handleNavbarScroll = () => {

        if (!navbar) return;

        navbar.classList.toggle(
            "scrolled",
            window.scrollY > 50
        );

    };

    handleNavbarScroll();

    window.addEventListener(
        "scroll",
        handleNavbarScroll,
        { passive: true }
    );


    /* =====================================================
       2. SEARCH
    ===================================================== */

    const searchInput =
        document.getElementById("searchInput");

    const searchForm =
        document.querySelector(".modern-search");

    const suggestionButtons =
        document.querySelectorAll(
            ".search-suggestions button"
        );


    /* -----------------------------------------------------
       Trending Search Buttons
    ----------------------------------------------------- */

    suggestionButtons.forEach((button) => {

        button.addEventListener("click", () => {

            if (!searchInput) return;

            searchInput.value =
                button.textContent.trim();

            searchInput.focus();

        });

    });


    /* -----------------------------------------------------
       Search Form
    ----------------------------------------------------- */

    if (searchForm) {

        searchForm.addEventListener(
            "submit",
            (event) => {

                if (!searchInput) return;

                const value =
                    searchInput.value.trim();


                if (!value) {

                    event.preventDefault();

                    searchInput.focus();

                    searchInput.classList.add(
                        "search-error"
                    );


                    setTimeout(() => {

                        searchInput.classList.remove(
                            "search-error"
                        );

                    }, 700);

                }

            }
        );

    }


    /* -----------------------------------------------------
       Prevent Empty Enter
    ----------------------------------------------------- */

    if (searchInput) {

        searchInput.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key === "Enter" &&
                    !searchInput.value.trim()
                ) {

                    event.preventDefault();

                    searchInput.focus();

                }

            }
        );

    }


    /* =====================================================
       3. SCROLL TO TOP
    ===================================================== */

    let topButton =
        document.querySelector(".top-btn");


    if (!topButton) {

        topButton =
            document.createElement("button");

        topButton.className = "top-btn";

        topButton.type = "button";

        topButton.setAttribute(
            "aria-label",
            "Scroll to top"
        );

        topButton.innerHTML =
            '<i class="fa-solid fa-arrow-up"></i>';

        document.body.appendChild(
            topButton
        );

    }


    const handleTopButton = () => {

        topButton.style.display =
            window.scrollY > 500
                ? "flex"
                : "none";

    };


    handleTopButton();


    window.addEventListener(
        "scroll",
        handleTopButton,
        { passive: true }
    );


    topButton.addEventListener(
        "click",
        () => {

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });

        }
    );


    /* =====================================================
       4. LOGO CLICK EFFECT
    ===================================================== */

    const logo =
        document.querySelector(
            ".logo-circle"
        );


    if (logo) {

        logo.addEventListener(
            "click",
            () => {

                logo.classList.remove(
                    "logo-click"
                );

                void logo.offsetWidth;

                logo.classList.add(
                    "logo-click"
                );


                setTimeout(() => {

                    logo.classList.remove(
                        "logo-click"
                    );

                }, 500);

            }
        );

    }


    /* =====================================================
       5. CUSTOM CURSOR
       DESKTOP ONLY
    ===================================================== */

    const cursor =
        document.querySelector(
            ".cursor"
        );


    const follower =
        document.querySelector(
            ".cursor-follower"
        );


    const finePointer =
        window.matchMedia(
            "(pointer:fine)"
        ).matches;


    if (
        cursor &&
        follower &&
        finePointer
    ) {

        let mouseX = 0;
        let mouseY = 0;

        let followerX = 0;
        let followerY = 0;


        document.addEventListener(
            "mousemove",
            (event) => {

                mouseX =
                    event.clientX;

                mouseY =
                    event.clientY;


                cursor.style.left =
                    `${mouseX}px`;

                cursor.style.top =
                    `${mouseY}px`;

            }
        );


        const animateFollower = () => {

            followerX +=
                (mouseX - followerX) * 0.15;

            followerY +=
                (mouseY - followerY) * 0.15;


            follower.style.left =
                `${followerX}px`;

            follower.style.top =
                `${followerY}px`;


            requestAnimationFrame(
                animateFollower
            );

        };


        animateFollower();


        const hoverElements =
            document.querySelectorAll(
                [
                    "a",
                    "button",
                    ".modern-product",
                    ".category-card",
                    ".nav-link",
                    ".cart-btn",
                    ".detail-btn",
                    ".wishlist-btn-home",
                    ".menu-btn",
                    ".slider-dot"
                ].join(", ")
            );


        hoverElements.forEach(
            (element) => {

                element.addEventListener(
                    "mouseenter",
                    () => {

                        follower.classList.add(
                            "cursor-hover"
                        );

                    }
                );


                element.addEventListener(
                    "mouseleave",
                    () => {

                        follower.classList.remove(
                            "cursor-hover"
                        );

                    }
                );

            }
        );

    }


    /* =====================================================
       6. TRUSTYSHOP MESSAGE ALERT

       NORMAL:
       Automatically closes after 2 seconds.

       PENDING:
       NEVER auto-closes.
       ONLY closes when "Got it" is clicked.
    ===================================================== */

    const messageOverlay =
        document.getElementById(
            "messageOverlay"
        );


    if (messageOverlay) {

        messageOverlay.style.display =
            "flex";

        messageOverlay.style.opacity =
            "1";


        const messageType =
            messageOverlay.getAttribute(
                "data-message-type"
            );


        const isPending =
            messageType === "pending";


        /* -------------------------------------------------
           Global Close Function
        ------------------------------------------------- */

        window.closeSuccessAlert =
            function () {

                if (!messageOverlay) {
                    return;
                }


                if (
                    !document.body.contains(
                        messageOverlay
                    )
                ) {
                    return;
                }


                if (
                    messageOverlay.dataset.closing ===
                    "true"
                ) {
                    return;
                }


                messageOverlay.dataset.closing =
                    "true";


                messageOverlay.classList.add(
                    "message-closing"
                );


                setTimeout(() => {

                    if (
                        messageOverlay &&
                        document.body.contains(
                            messageOverlay
                        )
                    ) {

                        messageOverlay.remove();

                    }

                }, 300);

            };


        /* -------------------------------------------------
           Normal Message Auto Close
        ------------------------------------------------- */

        if (!isPending) {

            setTimeout(() => {

                window.closeSuccessAlert();

            }, 2000);

        }


        /* -------------------------------------------------
           Click Outside
        ------------------------------------------------- */

        messageOverlay.addEventListener(
            "click",
            (event) => {

                if (
                    event.target !==
                    messageOverlay
                ) {
                    return;
                }


                if (isPending) {
                    return;
                }


                window.closeSuccessAlert();

            }
        );

    }


    /* =====================================================
       7. SELLER CARD 3D HOVER
       DESKTOP ONLY
    ===================================================== */

    const sellerCards =
        document.querySelectorAll(
            ".seller-card"
        );


    if (
        sellerCards.length &&
        finePointer
    ) {

        sellerCards.forEach(
            (card) => {

                card.addEventListener(
                    "mousemove",
                    (event) => {

                        if (
                            !card.classList.contains(
                                "show"
                            )
                        ) {
                            return;
                        }


                        const rect =
                            card.getBoundingClientRect();


                        const x =
                            event.clientX -
                            rect.left;


                        const y =
                            event.clientY -
                            rect.top;


                        const rotateY =
                            (
                                x -
                                rect.width / 2
                            ) / 35;


                        const rotateX =
                            (
                                rect.height / 2 -
                                y
                            ) / 35;


                        card.style.transform =
                            `perspective(1200px)
                             rotateX(${rotateX}deg)
                             rotateY(${rotateY}deg)
                             translateY(-8px)`;

                    }
                );


                card.addEventListener(
                    "mouseleave",
                    () => {

                        card.style.transform =
                            "";

                    }
                );

            }
        );

    }


    /* =====================================================
       8. BUTTON RIPPLE EFFECT
    ===================================================== */

    document
        .querySelectorAll(
            ".cart-btn, .detail-btn"
        )
        .forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    (event) => {

                        const ripple =
                            document.createElement(
                                "span"
                            );


                        ripple.className =
                            "ripple";


                        const rect =
                            button.getBoundingClientRect();


                        ripple.style.left =
                            `${event.clientX - rect.left}px`;


                        ripple.style.top =
                            `${event.clientY - rect.top}px`;


                        button.appendChild(
                            ripple
                        );


                        setTimeout(() => {

                            ripple.remove();

                        }, 700);

                    }
                );

            }
        );


    /* =====================================================
       9. ADD TO CART
    ===================================================== */

    const cartButtons =
        document.querySelectorAll(
            ".cart-btn"
        );


    cartButtons.forEach(
        (button) => {

            button.addEventListener(
                "click",
                () => {

                    /* -------------------------------------
                       Prevent Double Click
                    ------------------------------------- */

                    if (
                        button.dataset.cartBusy ===
                        "true"
                    ) {
                        return;
                    }


                    button.dataset.cartBusy =
                        "true";


                    const originalHTML =
                        button.innerHTML;


                    /* -------------------------------------
                       Success State
                    ------------------------------------- */

                    button.innerHTML =
                        '<i class="fa-solid fa-check"></i> Added';


                    button.classList.add(
                        "cart-added"
                    );


                    /* -------------------------------------
                       Cart Count
                    ------------------------------------- */

                    const cartCount =
                        document.querySelector(
                            ".cart-count"
                        );


                    const cartLink =
                        document.querySelector(
                            ".cart-link"
                        );


                    if (cartCount) {

                        let count =
                            parseInt(
                                cartCount.textContent,
                                10
                            ) || 0;


                        count++;


                        cartCount.textContent =
                            count;


                        cartCount.classList.remove(
                            "cart-pop"
                        );


                        void cartCount.offsetWidth;


                        cartCount.classList.add(
                            "cart-pop"
                        );

                    }


                    /* -------------------------------------
                       Cart Shake
                    ------------------------------------- */

                    if (cartLink) {

                        cartLink.classList.remove(
                            "shake"
                        );


                        void cartLink.offsetWidth;


                        cartLink.classList.add(
                            "shake"
                        );

                    }


                    setTimeout(() => {

                        cartCount?.classList.remove(
                            "cart-pop"
                        );


                        cartLink?.classList.remove(
                            "shake"
                        );

                    }, 600);


                    /* -------------------------------------
                       Cart Toast
                    ------------------------------------- */

                    const toast =
                        document.getElementById(
                            "cartToast"
                        );


                    if (toast) {

                        toast.classList.add(
                            "show"
                        );


                        clearTimeout(
                            toast._hideTimer
                        );


                        toast._hideTimer =
                            setTimeout(
                                () => {

                                    toast.classList.remove(
                                        "show"
                                    );

                                },
                                2200
                            );

                    }


                    /* -------------------------------------
                       Restore Button
                    ------------------------------------- */

                    setTimeout(() => {

                        button.innerHTML =
                            originalHTML;


                        button.classList.remove(
                            "cart-added"
                        );


                        button.dataset.cartBusy =
                            "false";

                    }, 1800);

                }
            );

        }
    );


    /* =====================================================
       10. VIEW DETAIL BUTTON
    ===================================================== */

    document
        .querySelectorAll(
            ".detail-btn"
        )
        .forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {

                        const card =
                            button.closest(
                                ".seller-card"
                            );


                        if (!card) {
                            return;
                        }


                        if (
                            typeof card.animate ===
                            "function"
                        ) {

                            card.animate(
                                [
                                    {
                                        transform:
                                            "scale(1)"
                                    },
                                    {
                                        transform:
                                            "scale(.98)"
                                    },
                                    {
                                        transform:
                                            "scale(1)"
                                    }
                                ],
                                {
                                    duration: 350,
                                    easing: "ease-out"
                                }
                            );

                        }

                    }
                );

            }
        );


    /* =====================================================
       11. SCROLL REVEAL
    ===================================================== */

    const revealCards =
        document.querySelectorAll(
            ".seller-card"
        );


    if (
        revealCards.length &&
        "IntersectionObserver" in window
    ) {

        const observer =
            new IntersectionObserver(
                (entries) => {

                    entries.forEach(
                        (entry) => {

                            if (
                                entry.isIntersecting
                            ) {

                                entry.target.classList.add(
                                    "show"
                                );


                                observer.unobserve(
                                    entry.target
                                );

                            }

                        }
                    );

                },
                {
                    threshold: 0.12
                }
            );


        revealCards.forEach(
            (card) => {

                card.classList.add(
                    "hidden"
                );


                observer.observe(
                    card
                );

            }
        );

    } else {

        revealCards.forEach(
            (card) => {

                card.classList.add(
                    "show"
                );

            }
        );

    }


    /* =====================================================
       12. MARKET FLOATING PARTICLES
    ===================================================== */

    const marketParticles =
        document.getElementById(
            "marketParticles"
        );


    if (marketParticles) {

        const fragment =
            document.createDocumentFragment();


        for (
            let i = 0;
            i < 35;
            i++
        ) {

            const circle =
                document.createElement(
                    "span"
                );


            circle.className =
                "floating-circle";


            const size =
                8 +
                Math.random() * 20;


            circle.style.left =
                `${Math.random() * 100}%`;


            circle.style.width =
                `${size}px`;


            circle.style.height =
                `${size}px`;


            circle.style.animationDuration =
                `${8 + Math.random() * 8}s`;


            circle.style.animationDelay =
                `${Math.random() * 5}s`;


            fragment.appendChild(
                circle
            );

        }


        marketParticles.appendChild(
            fragment
        );

    }


    /* =====================================================
       13. MOUSE GLOW
       DESKTOP ONLY
    ===================================================== */

    const mouseGlow =
        document.getElementById(
            "mouseGlow"
        );


    if (
        mouseGlow &&
        finePointer
    ) {

        let targetX = 0;
        let targetY = 0;

        let glowX = 0;
        let glowY = 0;


        document.addEventListener(
            "mousemove",
            (event) => {

                targetX =
                    event.clientX;

                targetY =
                    event.clientY;

            }
        );


        const animateGlow = () => {

            glowX +=
                (targetX - glowX) * 0.12;


            glowY +=
                (targetY - glowY) * 0.12;


            mouseGlow.style.left =
                `${glowX}px`;


            mouseGlow.style.top =
                `${glowY}px`;


            requestAnimationFrame(
                animateGlow
            );

        };


        animateGlow();

    }


    /* =====================================================
       14. IMAGE SLIDER

       ONE SLIDER SYSTEM ONLY.
       Prevents duplicate intervals.
    ===================================================== */

    const sliderIntervals =
        new WeakMap();


    const sliderIndexes =
        new WeakMap();


    function getSliderImages(slider) {

        if (!slider) {
            return [];
        }


        const data =
            slider.dataset.images;


        if (!data) {
            return [];
        }


        return data
            .split(",")
            .map(
                (image) =>
                    image.trim()
            )
            .filter(Boolean);

    }


    function changeSliderImage(
        slider,
        index
    ) {

        if (!slider) {
            return;
        }


        const images =
            getSliderImages(
                slider
            );


        if (!images.length) {
            return;
        }


        const imageElement =
            slider.querySelector(
                "img"
            );


        if (!imageElement) {
            return;
        }


        index =
            index % images.length;


        if (index < 0) {

            index =
                images.length - 1;

        }


        sliderIndexes.set(
            slider,
            index
        );


        imageElement.style.opacity =
            "0";


        setTimeout(() => {

            imageElement.src =
                images[index];


            imageElement.style.opacity =
                "1";

        }, 150);


        /* Update dots */

        const dots =
            slider.querySelectorAll(
                ".slider-dot"
            );


        dots.forEach(
            (dot, dotIndex) => {

                dot.classList.toggle(
                    "active",
                    dotIndex === index
                );

            }
        );

    }


    function startSlide(slider) {

        if (!slider) {
            return;
        }


        const images =
            getSliderImages(
                slider
            );


        if (
            images.length <= 1
        ) {
            return;
        }


        if (
            sliderIntervals.has(
                slider
            )
        ) {
            return;
        }


        let index =
            sliderIndexes.get(
                slider
            ) || 0;


        const interval =
            setInterval(
                () => {

                    index =
                        (
                            index + 1
                        ) %
                        images.length;


                    changeSliderImage(
                        slider,
                        index
                    );

                },
                1500
            );


        sliderIntervals.set(
            slider,
            interval
        );

    }


    function stopSlide(slider) {

        if (!slider) {
            return;
        }


        const interval =
            sliderIntervals.get(
                slider
            );


        if (interval) {

            clearInterval(
                interval
            );


            sliderIntervals.delete(
                slider
            );

        }


        /* Return to first image */

        changeSliderImage(
            slider,
            0
        );

    }


    /* -----------------------------------------------------
       Make Slider Functions Globally Available
    ----------------------------------------------------- */

    window.startSlide =
        startSlide;


    window.stopSlide =
        stopSlide;


    /* -----------------------------------------------------
       Attach Sliders
    ----------------------------------------------------- */

    document
        .querySelectorAll(
            ".post-image-slider"
        )
        .forEach(
            (slider) => {

                const images =
                    getSliderImages(
                        slider
                    );


                const dots =
                    slider.querySelectorAll(
                        ".slider-dot"
                    );


                /* -----------------------------------------
                   Initialize First Dot
                ----------------------------------------- */

                if (
                    images.length > 0 &&
                    dots.length > 0
                ) {

                    dots.forEach(
                        (dot, index) => {

                            dot.classList.toggle(
                                "active",
                                index === 0
                            );

                        }
                    );

                }


                /* -----------------------------------------
                   Desktop Hover
                ----------------------------------------- */

                slider.addEventListener(
                    "mouseenter",
                    () => {

                        if (finePointer) {

                            startSlide(
                                slider
                            );

                        }

                    }
                );


                slider.addEventListener(
                    "mouseleave",
                    () => {

                        if (finePointer) {

                            stopSlide(
                                slider
                            );

                        }

                    }
                );


                /* -----------------------------------------
                   Mobile Touch
                ----------------------------------------- */

                slider.addEventListener(
                    "touchstart",
                    () => {

                        startSlide(
                            slider
                        );

                    },
                    {
                        passive: true
                    }
                );


                slider.addEventListener(
                    "touchend",
                    () => {

                        /*
                         * Stop after the user
                         * finishes touching.
                         */

                        if (!finePointer) {

                            setTimeout(
                                () => {

                                    stopSlide(
                                        slider
                                    );

                                },
                                2500
                            );

                        }

                    },
                    {
                        passive: true
                    }
                );


                /* -----------------------------------------
                   Slider Dots
                ----------------------------------------- */

                dots.forEach(
                    (dot, index) => {

                        /* Desktop Hover */

                        dot.addEventListener(
                            "mouseenter",
                            () => {

                                if (!finePointer) {
                                    return;
                                }


                                stopSlide(
                                    slider
                                );


                                changeSliderImage(
                                    slider,
                                    index
                                );

                            }
                        );


                        /* Click */

                        dot.addEventListener(
                            "click",
                            (event) => {

                                event.preventDefault();

                                event.stopPropagation();


                                stopSlide(
                                    slider
                                );


                                changeSliderImage(
                                    slider,
                                    index
                                );

                            }
                        );

                    }
                );

            }
        );


    /* =====================================================
       15. CART TOAST
    ===================================================== */

    const cartToast =
        document.getElementById(
            "cartToast"
        );


    if (cartToast) {

        cartToast.addEventListener(
            "click",
            () => {

                cartToast.classList.remove(
                    "show"
                );

            }
        );

    }


    /* =====================================================
       16. SAVE MENU

       Handles:
       - Three-dot menu
       - Open/close
       - Outside click
       - Escape key
    ===================================================== */

    const menuButtons =
        document.querySelectorAll(
            ".menu-btn"
        );


    menuButtons.forEach(
        (button) => {

            button.addEventListener(
                "click",
                (event) => {

                    event.preventDefault();

                    event.stopPropagation();


                    const sellerRight =
                        button.closest(
                            ".seller-right"
                        );


                    if (!sellerRight) {
                        return;
                    }


                    const saveBox =
                        sellerRight.querySelector(
                            ".save-box"
                        );


                    if (!saveBox) {
                        return;
                    }


                    /* Close other menus */

                    document
                        .querySelectorAll(
                            ".save-box.active"
                        )
                        .forEach(
                            (box) => {

                                if (
                                    box !==
                                    saveBox
                                ) {

                                    box.classList.remove(
                                        "active"
                                    );

                                }

                            }
                        );


                    saveBox.classList.toggle(
                        "active"
                    );

                }
            );

        }
    );


    /* -----------------------------------------------------
       Save Box Click Protection
    ----------------------------------------------------- */

    document
        .querySelectorAll(
            ".save-box"
        )
        .forEach(
            (box) => {

                box.addEventListener(
                    "click",
                    (event) => {

                        event.stopPropagation();

                    }
                );

            }
        );


    /* -----------------------------------------------------
       Close Save Menus Outside
    ----------------------------------------------------- */

    document.addEventListener(
        "click",
        () => {

            document
                .querySelectorAll(
                    ".save-box.active"
                )
                .forEach(
                    (box) => {

                        box.classList.remove(
                            "active"
                        );

                    }
                );

        }
    );


    /* =====================================================
       17. HOME WISHLIST BUTTON

       UI state only.
       Backend saving should be handled by
       your Django wishlist endpoint if available.
    ===================================================== */

    const wishlistButtons =
        document.querySelectorAll(
            ".wishlist-btn-home"
        );


    wishlistButtons.forEach(
        (button) => {

            button.addEventListener(
                "click",
                (event) => {

                    event.preventDefault();

                    event.stopPropagation();


                    /* Toggle liked state */

                    button.classList.toggle(
                        "liked"
                    );


                    /* Heart animation */

                    button.classList.remove(
                        "wishlist-heart-pop"
                    );


                    void button.offsetWidth;


                    button.classList.add(
                        "wishlist-heart-pop"
                    );


                    /* Update icon */

                    const icon =
                        button.querySelector(
                            ".wishlist-icon-home"
                        );


                    if (icon) {

                        if (
                            button.classList.contains(
                                "liked"
                            )
                        ) {

                            icon.classList.remove(
                                "fa-regular"
                            );

                            icon.classList.add(
                                "fa-solid"
                            );

                        } else {

                            icon.classList.remove(
                                "fa-solid"
                            );

                            icon.classList.add(
                                "fa-regular"
                            );

                        }

                    }


                    /* Accessibility */

                    button.setAttribute(
                        "aria-pressed",
                        button.classList.contains(
                            "liked"
                        )
                            ? "true"
                            : "false"
                    );

                }
            );

        }
    );


    /* =====================================================
       18. ESCAPE KEY

       Important:
       Pending messages are NOT closed by Escape.
    ===================================================== */

    document.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key !== "Escape"
            ) {
                return;
            }


            /* ---------------------------------------------
               Close Save Menus
            --------------------------------------------- */

            document
                .querySelectorAll(
                    ".save-box"
                )
                .forEach(
                    (box) => {

                        box.classList.remove(
                            "active"
                        );

                    }
                );


            /* ---------------------------------------------
               Close Message
            --------------------------------------------- */

            const overlay =
                document.getElementById(
                    "messageOverlay"
                );


            if (!overlay) {
                return;
            }


            const isPending =
                overlay.dataset.messageType ===
                "pending";


            if (isPending) {
                return;
            }


            if (
                typeof window.closeSuccessAlert ===
                "function"
            ) {

                window.closeSuccessAlert();

            }

        }
    );


    /* =====================================================
       19. PREVENT IMAGE DRAGGING
    ===================================================== */

    document
        .querySelectorAll(
            [
                ".seller-profile",
                ".product-image",
                ".post-image-slider img",
                ".nav-profile-img"
            ].join(", ")
        )
        .forEach(
            (image) => {

                image.setAttribute(
                    "draggable",
                    "false"
                );


                image.addEventListener(
                    "dragstart",
                    (event) => {

                        event.preventDefault();

                    }
                );

            }
        );


    /* =====================================================
       20. REDUCE MOTION
       ACCESSIBILITY
    ===================================================== */

    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        );


    const applyReducedMotion = () => {

        document.documentElement.classList.toggle(
            "reduce-motion",
            reducedMotion.matches
        );

    };


    applyReducedMotion();


    if (
        typeof reducedMotion.addEventListener ===
        "function"
    ) {

        reducedMotion.addEventListener(
            "change",
            applyReducedMotion
        );

    }


    /* =====================================================
       21. RESIZE CLEANUP
    ===================================================== */

    window.addEventListener(
        "resize",
        () => {

            /* Close save menus */

            document
                .querySelectorAll(
                    ".save-box"
                )
                .forEach(
                    (box) => {

                        box.classList.remove(
                            "active"
                        );

                    }
                );


            /* Reset card transforms */

            document
                .querySelectorAll(
                    ".seller-card"
                )
                .forEach(
                    (card) => {

                        card.style.transform =
                            "";

                    }
                );

        },
        {
            passive: true
        }
    );


    /* =====================================================
       22. PAGE INITIALIZATION COMPLETE
    ===================================================== */

    document.documentElement.classList.add(
        "trustyshop-js-ready"
    );


});