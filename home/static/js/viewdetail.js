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


    /* Trending search buttons */

    suggestionButtons.forEach((button) => {

        button.addEventListener("click", () => {

            if (!searchInput) return;

            searchInput.value =
                button.textContent.trim();

            searchInput.focus();

        });

    });


    /* Search form */

    if (searchForm) {

        searchForm.addEventListener("submit", (event) => {

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

        });

    }


    /* Prevent empty Enter */

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

        document.body.appendChild(topButton);

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
        document.querySelector(".logo-circle");

    if (logo) {

        logo.addEventListener("click", () => {

            logo.classList.remove("logo-click");

            void logo.offsetWidth;

            logo.classList.add("logo-click");

            setTimeout(() => {

                logo.classList.remove(
                    "logo-click"
                );

            }, 500);

        });

    }


    /* =====================================================
       5. CUSTOM CURSOR
    ===================================================== */

    const cursor =
        document.querySelector(".cursor");

    const follower =
        document.querySelector(
            ".cursor-follower"
        );

    const finePointer =
        window.matchMedia("(pointer:fine)").matches;


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

                mouseX = event.clientX;
                mouseY = event.clientY;

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
                "a, button, " +
                ".modern-product, " +
                ".category-card, " +
                ".nav-link, " +
                ".cart-btn, " +
                ".detail-btn"
            );


        hoverElements.forEach((element) => {

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

        });

    }


    /* =====================================================
       6. TRUSTYSHOP MESSAGE ALERT

       NORMAL:
       Automatically closes after 2 seconds.

       PENDING:
       NEVER auto-closes.
       ONLY closes when "Got it" is clicked.
    ===================================================== */

    const messageOverlay = document.getElementById(
        "messageOverlay"
    );

    if (messageOverlay) {

        /* Always show overlay */
        messageOverlay.style.display = "flex";
        messageOverlay.style.opacity = "1";

        /* Get message type */
        const messageType =
            messageOverlay.getAttribute("data-message-type");

        const isPending =
            messageType === "pending";


        /* =================================================
           GLOBAL CLOSE FUNCTION
        ================================================= */

        window.closeSuccessAlert = function () {

            if (!messageOverlay) {
                return;
            }

            if (!document.body.contains(messageOverlay)) {
                return;
            }


            /* Prevent multiple close calls */
            if (
                messageOverlay.dataset.closing === "true"
            ) {
                return;
            }

            messageOverlay.dataset.closing = "true";


            /* Closing animation */
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


        /* =================================================
           NORMAL MESSAGE ONLY
           AUTO CLOSE AFTER 2 SECONDS
        ================================================= */

        if (!isPending) {

            setTimeout(() => {

                window.closeSuccessAlert();

            }, 2000);

        }


        /* =================================================
           CLICK OUTSIDE
        ================================================= */

        messageOverlay.addEventListener(
            "click",
            (event) => {

                /* Only react to the overlay itself */
                if (
                    event.target !==
                    messageOverlay
                ) {
                    return;
                }


                /* Pending messages NEVER close outside */
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

        sellerCards.forEach((card) => {

            card.addEventListener(
                "mousemove",
                (event) => {

                    /* Don't animate hidden cards */

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

                    card.style.transform = "";

                }
            );

        });

    }


    /* =====================================================
       8. BUTTON RIPPLE EFFECT
    ===================================================== */

    document
        .querySelectorAll(
            ".cart-btn, .detail-btn"
        )
        .forEach((button) => {

            button.addEventListener(
                "click",
                (event) => {

                    const ripple =
                        document.createElement(
                            "span"
                        );


                    ripple.className = "ripple";


                    const rect =
                        button.getBoundingClientRect();


                    ripple.style.left =
                        `${event.clientX - rect.left}px`;

                    ripple.style.top =
                        `${event.clientY - rect.top}px`;


                    button.appendChild(ripple);


                    setTimeout(() => {

                        ripple.remove();

                    }, 700);

                }
            );

        });


    /* =====================================================
       9. ADD TO CART
    ===================================================== */

    const cartButtons =
        document.querySelectorAll(
            ".cart-btn"
        );


    cartButtons.forEach((button) => {

        button.addEventListener(
            "click",
            () => {

                /* Prevent double-click */

                if (
                    button.dataset.cartBusy ===
                    "true"
                ) {
                    return;
                }


                button.dataset.cartBusy = "true";


                const originalHTML =
                    button.innerHTML;


                /* Success state */

                button.innerHTML =
                    '<i class="fa-solid fa-check"></i> Added';

                button.classList.add(
                    "cart-added"
                );


                /* Cart count */

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


                /* Cart shake */

                if (cartLink) {

                    cartLink.classList.remove(
                        "shake"
                    );


                    void cartLink.offsetWidth;


                    cartLink.classList.add(
                        "shake"
                    );

                }


                /* Remove animation classes */

                setTimeout(() => {

                    cartCount?.classList.remove(
                        "cart-pop"
                    );

                    cartLink?.classList.remove(
                        "shake"
                    );

                }, 600);


                /* Cart toast */

                const toast =
                    document.getElementById(
                        "cartToast"
                    );


                if (toast) {

                    toast.classList.add("show");


                    clearTimeout(
                        toast._hideTimer
                    );


                    toast._hideTimer =
                        setTimeout(() => {

                            toast.classList.remove(
                                "show"
                            );

                        }, 2200);

                }


                /* Restore button */

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

    });


    /* =====================================================
       10. VIEW DETAIL BUTTON
    ===================================================== */

    document
        .querySelectorAll(".detail-btn")
        .forEach((button) => {

            button.addEventListener(
                "click",
                () => {

                    const card =
                        button.closest(
                            ".seller-card"
                        );


                    if (!card) return;


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

        });


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

                    entries.forEach((entry) => {

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

                    });

                },
                {
                    threshold: 0.12
                }
            );


        revealCards.forEach((card) => {

            card.classList.add("hidden");

            observer.observe(card);

        });

    } else {

        revealCards.forEach((card) => {

            card.classList.add("show");

        });

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


        for (let i = 0; i < 35; i++) {

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


            fragment.appendChild(circle);

        }


        marketParticles.appendChild(
            fragment
        );

    }


    /* =====================================================
       13. MOUSE GLOW
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

                targetX = event.clientX;
                targetY = event.clientY;

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

       Uses ONE slider system only.
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
            .map((image) => image.trim())
            .filter(Boolean);

    }


    function changeSliderImage(
        slider,
        index
    ) {

        const images =
            getSliderImages(slider);


        if (!images.length) {
            return;
        }


        const imageElement =
            slider.querySelector("img");


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


        imageElement.style.opacity = "0";


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


        dots.forEach((dot, dotIndex) => {

            dot.classList.toggle(
                "active",
                dotIndex === index
            );

        });

    }


    function startSlide(slider) {

        if (!slider) return;


        const images =
            getSliderImages(slider);


        if (images.length <= 1) {
            return;
        }


        if (
            sliderIntervals.has(slider)
        ) {
            return;
        }


        let index =
            sliderIndexes.get(slider) || 0;


        const interval =
            setInterval(() => {

                index =
                    (index + 1) %
                    images.length;


                changeSliderImage(
                    slider,
                    index
                );

            }, 1500);


        sliderIntervals.set(
            slider,
            interval
        );

    }


    function stopSlide(slider) {

        if (!slider) return;


        const interval =
            sliderIntervals.get(
                slider
            );


        if (interval) {

            clearInterval(interval);

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


    /* Make functions available globally
       for inline HTML handlers if needed. */

    window.startSlide = startSlide;
    window.stopSlide = stopSlide;


    /* Attach sliders */

    document
        .querySelectorAll(
            ".post-image-slider"
        )
        .forEach((slider) => {

            const images =
                getSliderImages(slider);


            /* Initialize first dot */

            const dots =
                slider.querySelectorAll(
                    ".slider-dot"
                );


            if (
                images.length > 0 &&
                dots.length > 0
            ) {

                dots.forEach((dot, index) => {

                    dot.classList.toggle(
                        "active",
                        index === 0
                    );

                });

            }


            /* Desktop hover */

            slider.addEventListener(
                "mouseenter",
                () => {

                    if (finePointer) {
                        startSlide(slider);
                    }

                }
            );


            slider.addEventListener(
                "mouseleave",
                () => {

                    if (finePointer) {
                        stopSlide(slider);
                    }

                }
            );


            /* Mobile touch */

            slider.addEventListener(
                "touchstart",
                () => {

                    startSlide(slider);

                },
                {
                    passive: true
                }
            );


            /* Dots */

            dots.forEach((dot, index) => {

                dot.addEventListener(
                    "mouseenter",
                    () => {

                        if (!finePointer) {
                            return;
                        }


                        /* Stop automatic slider */

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


                        changeSliderImage(
                            slider,
                            index
                        );

                    }
                );


                dot.addEventListener(
                    "click",
                    (event) => {

                        event.preventDefault();
                        event.stopPropagation();

                        changeSliderImage(
                            slider,
                            index
                        );

                    }
                );

            });

        });


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
       16. ESCAPE KEY

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


            /* Close save menus */

            document
                .querySelectorAll(
                    ".save-box"
                )
                .forEach((box) => {

                    box.classList.remove(
                        "active"
                    );

                });


            /* Close message only if NOT pending */

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
       17. PREVENT IMAGE DRAGGING
    ===================================================== */

    document
        .querySelectorAll(
            ".seller-profile, " +
            ".product-image, " +
            ".post-image-slider img"
        )
        .forEach((image) => {

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

        });


    /* =====================================================
       18. REDUCE MOTION
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
       19. RESIZE CLEANUP
    ===================================================== */

    window.addEventListener(
        "resize",
        () => {

            document
                .querySelectorAll(
                    ".save-box"
                )
                .forEach((box) => {

                    box.classList.remove(
                        "active"
                    );

                });

        },
        {
            passive: true
        }
    );


    /* =====================================================
       20. PAGE INITIALIZATION COMPLETE
    ===================================================== */

    document.documentElement.classList.add(
        "trustyshop-js-ready"
    );

});

/* =====================================================
   21. WISHLIST TOGGLE
===================================================== */

const wishlistButton =
    document.getElementById("wishlistBtn");

const wishlistIcon =
    document.getElementById("wishlistIcon");


if (wishlistButton && wishlistIcon) {

    wishlistButton.addEventListener(
        "click",
        async function () {

            /* Prevent double click */

            if (
                wishlistButton.dataset.busy === "true"
            ) {
                return;
            }

            wishlistButton.dataset.busy = "true";


            const isWishlisted =
                wishlistButton.dataset.wishlisted === "true";


            const url = isWishlisted
                ? wishlistButton.dataset.removeUrl
                : wishlistButton.dataset.addUrl;


            try {

                const response =
                    await fetch(
                        url,
                        {
                            method: "GET",

                            headers: {
                                "X-Requested-With":
                                    "XMLHttpRequest"
                            }
                        }
                    );


                if (!response.ok) {

                    throw new Error(
                        "Wishlist request failed"
                    );

                }


                const data =
                    await response.json();


                if (data.success) {

                    const newState =
                        data.wishlisted;


                    /* =================================
                       UPDATE DATA STATE
                    ================================= */

                    wishlistButton.dataset.wishlisted =
                        newState
                            ? "true"
                            : "false";


                    /* =================================
                       UPDATE BUTTON CLASS
                    ================================= */

                    wishlistButton.classList.toggle(
                        "liked",
                        newState
                    );


                    /* =================================
                       UPDATE HEART ICON
                    ================================= */

                    wishlistIcon.classList.toggle(
                        "fa-solid",
                        newState
                    );

                    wishlistIcon.classList.toggle(
                        "fa-regular",
                        !newState
                    );


                    /* =================================
                       HEART POP ANIMATION
                    ================================= */

                    wishlistIcon.classList.remove(
                        "wishlist-heart-pop"
                    );

                    void wishlistIcon.offsetWidth;

                    wishlistIcon.classList.add(
                        "wishlist-heart-pop"
                    );

                }

            } catch (error) {

                console.error(
                    "Wishlist error:",
                    error
                );

            } finally {

                wishlistButton.dataset.busy =
                    "false";

            }

        }
    );

}