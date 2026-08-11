// =======================================================
// TRUSTY SHOP JAVASCRIPT
// =======================================================

// document.addEventListener("DOMContentLoaded", function () {
//
//
//     // ===================================================
//     // 1. NAVBAR SCROLL EFFECT
//     // ===================================================
//
//     const navbar =
//         document.querySelector(".cute-navbar");
//
//     if (navbar) {
//
//         window.addEventListener("scroll", function () {
//
//             if (window.scrollY > 50) {
//
//                 navbar.classList.add("scrolled");
//
//             } else {
//
//                 navbar.classList.remove("scrolled");
//
//             }
//
//         });
//
//     }
//

    // ===================================================
    // 2. SEARCH
    // ===================================================

    const searchInput =
        document.getElementById("searchInput");

    const suggestionButtons =
        document.querySelectorAll(
            ".search-suggestions button"
        );


    // ---------------------------------------------------
    // TRENDING SEARCH BUTTONS
    // ---------------------------------------------------

    suggestionButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            if (!searchInput) {
                return;
            }

            searchInput.value =
                button.innerText.trim();

            searchInput.focus();

        });

    });


    // ---------------------------------------------------
    // SEARCH BUTTON
    // ---------------------------------------------------

    const searchButton =
        document.querySelector(
            ".modern-search button"
        );

    if (searchButton) {

        searchButton.addEventListener(
            "click",
            function () {

                if (!searchInput) {
                    return;
                }

                const value =
                    searchInput.value.trim();

                if (value !== "") {

                    alert(
                        "Searching for: " + value
                    );

                } else {

                    alert(
                        "Please enter product name"
                    );

                }

            }
        );

    }


    // ===================================================
    // 3. SCROLL TO TOP BUTTON
    // ===================================================

    const topButton =
        document.createElement("button");

    topButton.className = "top-btn";

    topButton.innerHTML =
        '<i class="fa-solid fa-arrow-up"></i>';

    document.body.appendChild(topButton);


    window.addEventListener("scroll", function () {

        if (window.scrollY > 500) {

            topButton.style.display = "flex";

        } else {

            topButton.style.display = "none";

        }

    });


    topButton.addEventListener(
        "click",
        function () {

            window.scrollTo({

                top: 0,

                behavior: "smooth"

            });

        }
    );


    // ===================================================
    // 4. LOGO CLICK ANIMATION
    // ===================================================

    const logo =
        document.querySelector(".logo-circle");

    if (logo) {

        logo.addEventListener(
            "click",
            function () {

                logo.classList.add(
                    "logo-click"
                );

                setTimeout(function () {

                    logo.classList.remove(
                        "logo-click"
                    );

                }, 500);

            }
        );

    }


    // ===================================================
    // 5. CUSTOM CURSOR
    // ===================================================

    const cursor =
        document.querySelector(".cursor");

    const follower =
        document.querySelector(
            ".cursor-follower"
        );


    if (cursor && follower) {

        document.addEventListener(
            "mousemove",
            function (e) {

                cursor.style.left =
                    e.clientX + "px";

                cursor.style.top =
                    e.clientY + "px";


                setTimeout(function () {

                    follower.style.left =
                        e.clientX + "px";

                    follower.style.top =
                        e.clientY + "px";

                }, 80);

            }
        );


        const hoverElements =
            document.querySelectorAll(
                "a, button, .modern-product, .category-card, .nav-link"
            );


        hoverElements.forEach(
            function (element) {

                element.addEventListener(
                    "mouseenter",
                    function () {

                        follower.style.width =
                            "70px";

                        follower.style.height =
                            "70px";

                        follower.style.background =
                            "rgba(13,110,253,0.2)";

                    }
                );


                element.addEventListener(
                    "mouseleave",
                    function () {

                        follower.style.width =
                            "40px";

                        follower.style.height =
                            "40px";

                        follower.style.background =
                            "transparent";

                    }
                );

            }
        );

    }


    // ===================================================
    // 6. TRUSTY SHOP MESSAGE ALERT
    // ===================================================
    // APPEARS IMMEDIATELY
    // DISAPPEARS AFTER 2 SECONDS
    // ===================================================

    const messageOverlay =
        document.getElementById("messageOverlay");


    if (messageOverlay) {

        // Make sure the alert is visible immediately.
        messageOverlay.style.display = "flex";
        messageOverlay.style.opacity = "1";


        // ------------------------------------------------
        // WAIT 2 SECONDS
        // ------------------------------------------------

        setTimeout(function () {

            // Start CSS closing animation
            messageOverlay.classList.add(
                "message-closing"
            );


            // ------------------------------------------------
            // REMOVE AFTER FADE ANIMATION
            // ------------------------------------------------

            setTimeout(function () {

                if (messageOverlay) {

                    messageOverlay.remove();

                }

            }, 450);


            // ------------------------------------------------
            // EXTRA FALLBACK
            // ------------------------------------------------

            setTimeout(function () {

                if (messageOverlay) {

                    messageOverlay.style.display =
                        "none";

                }

            }, 500);


        }, 2000);

    }


    // ===================================================
    // 7. SAVE POST
    // ===================================================

    window.savePost = function (button) {

        const box =
            button.nextElementSibling;


        if (!box) {
            return;
        }


        document
            .querySelectorAll(".save-box")
            .forEach(function (item) {

                if (item !== box) {

                    item.classList.remove(
                        "active"
                    );

                }

            });


        box.classList.toggle("active");

    };


    // ---------------------------------------------------
    // CLOSE SAVE MENU
    // ---------------------------------------------------

    document.addEventListener(
        "click",
        function (e) {

            if (!e.target.closest(".seller-right")) {

                document
                    .querySelectorAll(".save-box")
                    .forEach(function (box) {

                        box.classList.remove(
                            "active"
                        );

                    });

            }

        }
    );


    // ===================================================
    // 8. SELLER CARD HOVER
    // ===================================================

    document
        .querySelectorAll(".seller-card")
        .forEach(function (card) {

            card.addEventListener(
                "mousemove",
                function (e) {

                    const rect =
                        card.getBoundingClientRect();


                    const x =
                        e.clientX - rect.left;

                    const y =
                        e.clientY - rect.top;


                    const rotateY =
                        (x - rect.width / 2) / 18;

                    const rotateX =
                        (rect.height / 2 - y) / 18;


                    card.style.transform =
                        `perspective(900px)
                         rotateX(${rotateX}deg)
                         rotateY(${rotateY}deg)
                         translateY(-10px)`;

                }
            );


            card.addEventListener(
                "mouseleave",
                function () {

                    card.style.transform = "";

                }
            );

        });


    // ===================================================
    // 9. BUTTON RIPPLE
    // ===================================================

    document
        .querySelectorAll(
            ".cart-btn, .detail-btn"
        )
        .forEach(function (button) {

            button.addEventListener(
                "click",
                function (e) {

                    const ripple =
                        document.createElement("span");


                    ripple.className =
                        "ripple";


                    const rect =
                        this.getBoundingClientRect();


                    ripple.style.left =
                        e.clientX -
                        rect.left +
                        "px";


                    ripple.style.top =
                        e.clientY -
                        rect.top +
                        "px";


                    this.appendChild(ripple);


                    setTimeout(function () {

                        ripple.remove();

                    }, 700);

                }
            );

        });


    // ===================================================
    // 10. ADD TO CART
    // ===================================================

    document
        .querySelectorAll(".cart-btn")
        .forEach(function (btn) {

            btn.addEventListener(
                "click",
                function () {

                    const original =
                        this.innerHTML;


                    // ------------------------------------------------
                    // CHANGE BUTTON
                    // ------------------------------------------------

                    this.innerHTML =
                        '<i class="fa-solid fa-check"></i> Added';


                    this.style.background =
                        "#43A047";


                    // ------------------------------------------------
                    // CART BADGE
                    // ------------------------------------------------

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
                                cartCount.textContent
                            ) || 0;


                        count++;


                        cartCount.textContent =
                            count;


                        cartCount.classList.add(
                            "cart-pop"
                        );

                    }


                    if (cartLink) {

                        cartLink.classList.add(
                            "shake"
                        );

                    }


                    setTimeout(function () {

                        if (cartCount) {

                            cartCount.classList.remove(
                                "cart-pop"
                            );

                        }


                        if (cartLink) {

                            cartLink.classList.remove(
                                "shake"
                            );

                        }

                    }, 500);


                    // ------------------------------------------------
                    // CART TOAST
                    // ------------------------------------------------

                    const toast =
                        document.getElementById(
                            "cartToast"
                        );


                    if (toast) {

                        toast.classList.add(
                            "show"
                        );


                        setTimeout(function () {

                            toast.classList.remove(
                                "show"
                            );

                        }, 2200);

                    }


                    // ------------------------------------------------
                    // RESTORE BUTTON
                    // ------------------------------------------------

                    setTimeout(function () {

                        btn.innerHTML =
                            original;


                        btn.style.background =
                            "";

                    }, 1800);

                }
            );

        });


    // ===================================================
    // 11. VIEW DETAIL EFFECT
    // ===================================================

    document
        .querySelectorAll(".detail-btn")
        .forEach(function (btn) {

            btn.addEventListener(
                "click",
                function () {

                    const card =
                        this.closest(
                            ".seller-card"
                        );


                    if (!card) {
                        return;
                    }


                    card.animate(

                        [
                            {
                                transform:
                                    "scale(1)"
                            },

                            {
                                transform:
                                    "scale(.97)"
                            },

                            {
                                transform:
                                    "scale(1)"
                            }
                        ],

                        {
                            duration: 350
                        }

                    );

                }
            );

        });


    // ===================================================
    // 12. SCROLL REVEAL
    // ===================================================

    const cards =
        document.querySelectorAll(
            ".seller-card"
        );


    if (cards.length > 0) {

        const observer =
            new IntersectionObserver(
                function (entries) {

                    entries.forEach(
                        function (entry) {

                            if (
                                entry.isIntersecting
                            ) {

                                entry.target.classList.add(
                                    "show"
                                );

                            }

                        }
                    );

                },
                {
                    threshold: 0.15
                }
            );


        cards.forEach(
            function (card) {

                card.classList.add(
                    "hidden"
                );

                observer.observe(card);

            }
        );

    }


    // ===================================================
    // 13. FLOATING BACKGROUND
    // ===================================================

    const bg =
        document.getElementById(
            "marketParticles"
        );


    if (bg) {

        for (let i = 0; i < 35; i++) {

            const circle =
                document.createElement("span");


            circle.className =
                "floating-circle";


            circle.style.left =
                Math.random() * 100 + "%";


            circle.style.animationDuration =
                8 + Math.random() * 8 + "s";


            circle.style.animationDelay =
                Math.random() * 5 + "s";


            circle.style.width =
                8 + Math.random() * 20 + "px";


            circle.style.height =
                circle.style.width;


            bg.appendChild(circle);

        }

    }


    // ===================================================
    // 14. MOUSE GLOW
    // ===================================================

    const glow =
        document.getElementById(
            "mouseGlow"
        );


    if (glow) {

        document.addEventListener(
            "mousemove",
            function (e) {

                glow.style.left =
                    e.clientX + "px";

                glow.style.top =
                    e.clientY + "px";

            }
        );

    }


    // ===================================================
    // 15. FLOATING SELLER CARDS
    // ===================================================

    document
        .querySelectorAll(".seller-card")
        .forEach(function (card, index) {

            setInterval(
                function () {

                    card.animate(

                        [
                            {
                                transform:
                                    "translateY(0px)"
                            },

                            {
                                transform:
                                    "translateY(-6px)"
                            },

                            {
                                transform:
                                    "translateY(0px)"
                            }
                        ],

                        {
                            duration:
                                4000 +
                                index * 400,

                            iterations: 1
                        }

                    );

                },

                4500 +
                index * 600

            );

        });

    // ============================================
// HOME PAGE IMAGE SLIDER
// ============================================
let slideIntervals = {};

function startSlide(element) {
    const images = element.dataset.images.split(',');
    if (images.length <= 1 || !images[0]) return;

    let currentIndex = 0;
    const imgElement = element.querySelector('img');

    slideIntervals[element] = setInterval(function() {
        currentIndex = (currentIndex + 1) % images.length;
        imgElement.style.opacity = '0';
        setTimeout(function() {
            imgElement.src = images[currentIndex];
            imgElement.style.opacity = '1';
        }, 200);
    }, 1500);
}

function stopSlide(element) {
    clearInterval(slideIntervals[element]);
    const images = element.dataset.images.split(',');
    if (images.length > 0 && images[0]) {
        const imgElement = element.querySelector('img');
        imgElement.style.opacity = '0';
        setTimeout(function() {
            imgElement.src = images[0];
            imgElement.style.opacity = '1';
        }, 150);
    }
}

