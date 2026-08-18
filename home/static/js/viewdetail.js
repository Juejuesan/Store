
/* =========================================================
   TRUSTYSHOP — VIEW DETAIL JAVASCRIPT
   CLEAN • STABLE • MERGED
   HEAD + adminAuthenticate
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       1. COMMON HELPERS
    ===================================================== */

    const finePointer =
        window.matchMedia("(pointer:fine)").matches;


    function getCookie(name) {

        const cookies = document.cookie
            ? document.cookie.split(";")
            : [];

        for (const cookie of cookies) {

            const trimmedCookie = cookie.trim();

            if (trimmedCookie.startsWith(`${name}=`)) {

                return decodeURIComponent(
                    trimmedCookie.substring(
                        name.length + 1
                    )
                );
            }
        }

        return null;
    }


    function getCSRFToken() {

        const cookieToken =
            getCookie("csrftoken");

        if (cookieToken) {
            return cookieToken;
        }

        const csrfInput =
            document.querySelector(
                'input[name="csrfmiddlewaretoken"]'
            );

        return csrfInput
            ? csrfInput.value
            : "";
    }


    function showTemporaryMessage(
        message,
        type = "error"
    ) {

        let messageBox =
            document.getElementById(
                "viewDetailMessage"
            );

        if (!messageBox) {

            messageBox =
                document.createElement("div");

            messageBox.id =
                "viewDetailMessage";

            messageBox.style.position =
                "fixed";

            messageBox.style.top =
                "90px";

            messageBox.style.right =
                "20px";

            messageBox.style.zIndex =
                "99999";

            messageBox.style.padding =
                "14px 20px";

            messageBox.style.borderRadius =
                "12px";

            messageBox.style.fontWeight =
                "600";

            messageBox.style.boxShadow =
                "0 10px 30px rgba(0,0,0,.15)";

            messageBox.style.transition =
                "all .3s ease";

            document.body.appendChild(
                messageBox
            );
        }

        messageBox.textContent =
            message;

        messageBox.style.background =
            type === "success"
                ? "#dcfce7"
                : "#fee2e2";

        messageBox.style.color =
            type === "success"
                ? "#166534"
                : "#991b1b";

        messageBox.style.opacity =
            "1";

        clearTimeout(
            messageBox._hideTimer
        );

        messageBox._hideTimer =
            setTimeout(() => {

                messageBox.style.opacity =
                    "0";

            }, 2500);
    }


    /* =====================================================
       2. REFRESH WHEN RETURNING FROM CART
    ===================================================== */

    const needsRefresh =
        sessionStorage.getItem(
            "refreshItemDetail"
        );

    if (needsRefresh === "true") {

        sessionStorage.removeItem(
            "refreshItemDetail"
        );

        window.location.reload();
    }


    window.addEventListener(
        "pageshow",
        (event) => {

            if (!event.persisted) {
                return;
            }

            const refreshFlag =
                sessionStorage.getItem(
                    "refreshItemDetail"
                );

            if (refreshFlag === "true") {

                sessionStorage.removeItem(
                    "refreshItemDetail"
                );

                window.location.reload();
            }
        }
    );


    document.addEventListener(
        "visibilitychange",
        () => {

            if (document.hidden) {
                return;
            }

            const refreshFlag =
                sessionStorage.getItem(
                    "refreshItemDetail"
                );

            if (refreshFlag === "true") {

                sessionStorage.removeItem(
                    "refreshItemDetail"
                );

                window.location.reload();
            }
        }
    );


    /* =====================================================
       3. NAVBAR SCROLL EFFECT
    ===================================================== */

    const navbar =
        document.querySelector(
            ".cute-navbar"
        );


    function handleNavbarScroll() {

        if (!navbar) {
            return;
        }

        navbar.classList.toggle(
            "scrolled",
            window.scrollY > 50
        );
    }


    handleNavbarScroll();

    window.addEventListener(
        "scroll",
        handleNavbarScroll,
        {
            passive: true
        }
    );


    /* =====================================================
       4. SEARCH
    ===================================================== */

    const searchInput =
        document.getElementById(
            "searchInput"
        );

    const searchForm =
        document.querySelector(
            ".modern-search"
        );

    const suggestionButtons =
        document.querySelectorAll(
            ".search-suggestions button"
        );


    suggestionButtons.forEach(
        (button) => {

            button.addEventListener(
                "click",
                () => {

                    if (!searchInput) {
                        return;
                    }

                    searchInput.value =
                        button.textContent.trim();

                    searchInput.focus();
                }
            );
        }
    );


    if (searchForm) {

        searchForm.addEventListener(
            "submit",
            (event) => {

                if (!searchInput) {
                    return;
                }

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
       5. SCROLL TO TOP
    ===================================================== */

    let topButton =
        document.querySelector(
            ".top-btn"
        );


    if (!topButton) {

        topButton =
            document.createElement(
                "button"
            );

        topButton.className =
            "top-btn";

        topButton.type =
            "button";

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


    function handleTopButton() {

        topButton.style.display =
            window.scrollY > 500
                ? "flex"
                : "none";
    }


    handleTopButton();


    window.addEventListener(
        "scroll",
        handleTopButton,
        {
            passive: true
        }
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
       6. LOGO CLICK EFFECT
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
       7. CUSTOM CURSOR
    ===================================================== */

    const cursor =
        document.querySelector(
            ".cursor"
        );

    const follower =
        document.querySelector(
            ".cursor-follower"
        );


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


        function animateFollower() {

            followerX +=
                (mouseX - followerX) *
                0.15;

            followerY +=
                (mouseY - followerY) *
                0.15;

            follower.style.left =
                `${followerX}px`;

            follower.style.top =
                `${followerY}px`;

            requestAnimationFrame(
                animateFollower
            );
        }


        animateFollower();


        const hoverElements =
            document.querySelectorAll(
                "a, button, " +
                ".modern-product, " +
                ".category-card, " +
                ".nav-link, " +
                ".cart-btn, " +
                ".detail-btn, " +
                ".size-btn, " +
                ".qty-btn, " +
                ".add-to-cart-btn, " +
                ".thumbnail-wrapper"
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
       8. MESSAGE ALERT
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


        window.closeSuccessAlert =
            () => {

                if (
                    !messageOverlay ||
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


        if (!isPending) {

            setTimeout(
                () => window.closeSuccessAlert(),
                2000
            );
        }


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
       9. SELLER CARD 3D HOVER
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
       10. BUTTON RIPPLE
    ===================================================== */

    document
        .querySelectorAll(
            ".cart-btn, " +
            ".detail-btn, " +
            ".add-to-cart-btn"
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
       11. ITEM VIEWER
    ===================================================== */

    const itemSlides =
        document.querySelectorAll(
            ".item-slide"
        );

    const prevButton =
        document.getElementById(
            "prevBtn"
        );

    const nextButton =
        document.getElementById(
            "nextBtn"
        );

    const itemCounter =
        document.getElementById(
            "itemCounter"
        );


    let currentItemIndex = 0;


    function getCurrentSlide() {

        return (
            itemSlides[
                currentItemIndex
            ] || null
        );
    }


    /* =====================================================
       11A. THUMBNAIL → MAIN IMAGE
    ===================================================== */

    function setupThumbnailSystem(
        slide
    ) {

        if (!slide) {
            return;
        }


        const mainImage =
            slide.querySelector(
                ".main-image"
            );


        const thumbnails =
            slide.querySelectorAll(
                ".thumbnail-wrapper"
            );


        if (
            !mainImage ||
            !thumbnails.length
        ) {
            return;
        }


        thumbnails.forEach(
            (thumbnail) => {

                if (
                    thumbnail.dataset.thumbnailReady ===
                    "true"
                ) {
                    return;
                }


                thumbnail.dataset.thumbnailReady =
                    "true";


                thumbnail.addEventListener(
                    "click",
                    (event) => {

                        event.preventDefault();
                        event.stopPropagation();


                        const imageURL =
                            thumbnail.dataset.imageUrl;


                        if (!imageURL) {

                            console.warn(
                                "Thumbnail image URL is missing."
                            );

                            return;
                        }


                        if (
                            mainImage.src.endsWith(
                                imageURL
                            )
                        ) {

                            thumbnails.forEach(
                                (thumb) => {

                                    thumb.classList.remove(
                                        "active"
                                    );
                                }
                            );

                            thumbnail.classList.add(
                                "active"
                            );

                            return;
                        }


                        const newImage =
                            new Image();


                        newImage.onload =
                            () => {

                                mainImage.classList.add(
                                    "image-changing"
                                );


                                setTimeout(() => {

                                    mainImage.src =
                                        imageURL;

                                    mainImage.classList.remove(
                                        "image-changing"
                                    );

                                }, 150);
                            };


                        newImage.onerror =
                            () => {

                                console.error(
                                    "Unable to load image:",
                                    imageURL
                                );

                                mainImage.classList.remove(
                                    "image-changing"
                                );

                                showTemporaryMessage(
                                    "Unable to load this image.",
                                    "error"
                                );
                            };


                        newImage.src =
                            imageURL;


                        thumbnails.forEach(
                            (thumb) => {

                                thumb.classList.remove(
                                    "active"
                                );
                            }
                        );


                        thumbnail.classList.add(
                            "active"
                        );
                    }
                );
            }
        );
    }


    itemSlides.forEach(
        (slide) => {

            setupThumbnailSystem(
                slide
            );
        }
    );


    /* =====================================================
       11B. FULLSCREEN IMAGE LIGHTBOX
    ===================================================== */

    function setupImageLightbox(
        slide
    ) {

        if (!slide) {
            return;
        }


        const mainImage =
            slide.querySelector(
                ".main-image"
            );


        if (!mainImage) {
            return;
        }


        if (
            mainImage.dataset.lightboxReady ===
            "true"
        ) {
            return;
        }


        mainImage.dataset.lightboxReady =
            "true";


        mainImage.style.cursor =
            "zoom-in";


        mainImage.addEventListener(
            "click",
            function (event) {

                event.preventDefault();
                event.stopPropagation();


                const imageURL =
                    mainImage.currentSrc ||
                    mainImage.src;


                if (!imageURL) {
                    return;
                }


                const existingLightbox =
                    document.getElementById(
                        "trustyshopImageLightbox"
                    );


                if (existingLightbox) {
                    existingLightbox.remove();
                }


                const lightbox =
                    document.createElement(
                        "div"
                    );


                lightbox.id =
                    "trustyshopImageLightbox";


                lightbox.setAttribute(
                    "role",
                    "dialog"
                );


                lightbox.setAttribute(
                    "aria-modal",
                    "true"
                );


                lightbox.setAttribute(
                    "aria-label",
                    "Full screen product image"
                );


                lightbox.innerHTML = `
                    <button
                        type="button"
                        class="lightbox-close"
                        aria-label="Close image viewer"
                    >
                        <i class="fa-solid fa-xmark"></i>
                    </button>

                    <img
                        src="${imageURL}"
                        class="lightbox-image"
                        alt="${mainImage.alt || "Product image"}"
                        draggable="false"
                    >
                `;


                document.body.appendChild(
                    lightbox
                );


                const closeButton =
                    lightbox.querySelector(
                        ".lightbox-close"
                    );


                const lightboxImage =
                    lightbox.querySelector(
                        ".lightbox-image"
                    );


                /* -----------------------------
                   Lightbox style
                ----------------------------- */

                lightbox.style.position =
                    "fixed";

                lightbox.style.inset =
                    "0";

                lightbox.style.width =
                    "100vw";

                lightbox.style.height =
                    "100vh";

                lightbox.style.background =
                    "rgba(0,0,0,.96)";

                lightbox.style.display =
                    "flex";

                lightbox.style.alignItems =
                    "center";

                lightbox.style.justifyContent =
                    "center";

                lightbox.style.padding =
                    "40px";

                lightbox.style.boxSizing =
                    "border-box";

                lightbox.style.zIndex =
                    "999999";

                lightbox.style.opacity =
                    "0";

                lightbox.style.visibility =
                    "hidden";

                lightbox.style.transition =
                    "opacity .25s ease, visibility .25s ease";

                lightbox.style.overflow =
                    "hidden";


                /* -----------------------------
                   Image style
                ----------------------------- */

                if (lightboxImage) {

                    lightboxImage.style.display =
                        "block";

                    lightboxImage.style.maxWidth =
                        "calc(100vw - 80px)";

                    lightboxImage.style.maxHeight =
                        "calc(100vh - 80px)";

                    lightboxImage.style.width =
                        "auto";

                    lightboxImage.style.height =
                        "auto";

                    lightboxImage.style.objectFit =
                        "contain";

                    lightboxImage.style.borderRadius =
                        "12px";

                    lightboxImage.style.boxShadow =
                        "0 25px 80px rgba(0,0,0,.65)";

                    lightboxImage.style.userSelect =
                        "none";

                    lightboxImage.style.webkitUserDrag =
                        "none";

                    lightboxImage.style.cursor =
                        "default";

                    lightboxImage.style.transition =
                        "transform .25s ease";
                }


                /* -----------------------------
                   Close button
                ----------------------------- */

                if (closeButton) {

                    closeButton.style.position =
                        "fixed";

                    closeButton.style.top =
                        "24px";

                    closeButton.style.right =
                        "24px";

                    closeButton.style.width =
                        "48px";

                    closeButton.style.height =
                        "48px";

                    closeButton.style.border =
                        "1px solid rgba(255,255,255,.2)";

                    closeButton.style.borderRadius =
                        "50%";

                    closeButton.style.background =
                        "rgba(255,255,255,.14)";

                    closeButton.style.color =
                        "#fff";

                    closeButton.style.display =
                        "flex";

                    closeButton.style.alignItems =
                        "center";

                    closeButton.style.justifyContent =
                        "center";

                    closeButton.style.fontSize =
                        "22px";

                    closeButton.style.cursor =
                        "pointer";

                    closeButton.style.zIndex =
                        "1000000";

                    closeButton.style.backdropFilter =
                        "blur(12px)";

                    closeButton.style.webkitBackdropFilter =
                        "blur(12px)";

                    closeButton.style.transition =
                        "all .2s ease";
                }


                if (closeButton) {

                    closeButton.addEventListener(
                        "mouseenter",
                        () => {

                            closeButton.style.background =
                                "rgba(255,255,255,.25)";

                            closeButton.style.transform =
                                "rotate(90deg) scale(1.08)";
                        }
                    );


                    closeButton.addEventListener(
                        "mouseleave",
                        () => {

                            closeButton.style.background =
                                "rgba(255,255,255,.14)";

                            closeButton.style.transform =
                                "rotate(0deg) scale(1)";
                        }
                    );
                }


                requestAnimationFrame(
                    () => {

                        lightbox.style.opacity =
                            "1";

                        lightbox.style.visibility =
                            "visible";

                        if (lightboxImage) {

                            lightboxImage.style.transform =
                                "scale(1)";
                        }
                    }
                );


                document.body.classList.add(
                    "lightbox-active"
                );


                const previousBodyOverflow =
                    document.body.style.overflow;


                document.body.dataset.previousOverflow =
                    previousBodyOverflow;


                document.body.style.overflow =
                    "hidden";


                let isClosing = false;


                function closeLightbox() {

                    if (
                        isClosing ||
                        !lightbox
                    ) {
                        return;
                    }


                    isClosing = true;


                    document.removeEventListener(
                        "keydown",
                        handleEscape
                    );


                    lightbox.style.opacity =
                        "0";

                    lightbox.style.visibility =
                        "hidden";


                    document.body.classList.remove(
                        "lightbox-active"
                    );


                    const previousOverflow =
                        document.body.dataset.previousOverflow;


                    document.body.style.overflow =
                        previousOverflow || "";


                    delete document.body.dataset.previousOverflow;


                    setTimeout(() => {

                        if (
                            lightbox &&
                            document.body.contains(
                                lightbox
                            )
                        ) {

                            lightbox.remove();
                        }

                    }, 250);
                }


                if (closeButton) {

                    closeButton.addEventListener(
                        "click",
                        (event) => {

                            event.preventDefault();
                            event.stopPropagation();

                            closeLightbox();
                        }
                    );
                }


                if (lightboxImage) {

                    lightboxImage.addEventListener(
                        "click",
                        (event) => {

                            event.preventDefault();
                            event.stopPropagation();
                        }
                    );


                    lightboxImage.addEventListener(
                        "dragstart",
                        (event) => {

                            event.preventDefault();
                        }
                    );
                }


                function handleEscape(event) {

                    if (
                        event.key ===
                        "Escape"
                    ) {

                        event.preventDefault();

                        closeLightbox();
                    }
                }


                document.addEventListener(
                    "keydown",
                    handleEscape
                );


                if (closeButton) {

                    setTimeout(
                        () => closeButton.focus(),
                        50
                    );
                }
            }
        );
    }


    itemSlides.forEach(
        (slide) => {

            setupImageLightbox(
                slide
            );
        }
    );


       /* =====================================================
       11C. RESET CURRENT ITEM CONTROLS
    ===================================================== */

    function resetCurrentItemControls() {

        const slide =
            getCurrentSlide();


        if (!slide) {
            return;
        }


        const quantityInput =
            slide.querySelector(
                ".qty-input"
            );


        if (quantityInput) {

            quantityInput.value =
                "1";

            quantityInput.max =
                quantityInput.dataset.defaultMax ||
                "1";

            quantityInput.disabled =
                false;
        }


        const sizeButtons =
            slide.querySelectorAll(
                ".size-btn"
            );


        sizeButtons.forEach(
            (button) => {

                button.classList.remove(
                    "selected",
                    "active"
                );
            }
        );


        const sizeVariantInput =
            slide.querySelector(
                'input[name="size_variant_id"]'
            );


        if (sizeVariantInput) {

            sizeVariantInput.value =
                "";
        }


        /* Reset stock display */
        const stockDisplay =
            slide.querySelector(
                '.size-stock-display .stock-text'
            );


        if (stockDisplay) {

            stockDisplay.textContent =
                "Select a size";
        }


        const mainImage =
            slide.querySelector(
                ".main-image"
            );


        const thumbnails =
            slide.querySelectorAll(
                ".thumbnail-wrapper"
            );


        if (
            mainImage &&
            thumbnails.length
        ) {

            thumbnails.forEach(
                (thumbnail) => {

                    thumbnail.classList.remove(
                        "active"
                    );
                }
            );


            const firstThumbnail =
                thumbnails[0];


            if (firstThumbnail) {

                firstThumbnail.classList.add(
                    "active"
                );


                const firstImageURL =
                    firstThumbnail.dataset.imageUrl;


                if (firstImageURL) {

                    mainImage.classList.add(
                        "image-changing"
                    );


                    const resetImage =
                        new Image();


                    resetImage.onload =
                        () => {

                            mainImage.src =
                                firstImageURL;

                            mainImage.classList.remove(
                                "image-changing"
                            );
                        };


                    resetImage.onerror =
                        () => {

                            mainImage.classList.remove(
                                "image-changing"
                            );
                        };


                    resetImage.src =
                        firstImageURL;
                }
            }
        }


        const priceElement =
            slide.querySelector(
                ".item-price"
            );


        if (priceElement) {

            const firstSize =
                slide.querySelector(
                    ".size-btn"
                );


            if (firstSize) {

                const basePrice =
                    firstSize.dataset.price;


                if (basePrice) {

                    priceElement.textContent =
                        `${parseInt(
                            basePrice,
                            10
                        ).toLocaleString()} MMK`;

                    priceElement.dataset.originalPrice =
                        basePrice;
                }
            }
        }
    }

    /* =====================================================
       11D. UPDATE ITEM NAVIGATION
    ===================================================== */

    function updateItemNavigation() {

        const total =
            itemSlides.length;


        if (itemCounter) {

            itemCounter.textContent =
                `Item ${
                    currentItemIndex + 1
                } of ${total}`;
        }


        if (prevButton) {

            prevButton.disabled =
                currentItemIndex <= 0;
        }


        if (nextButton) {

            nextButton.disabled =
                currentItemIndex >=
                total - 1;
        }
    }


    /* =====================================================
       11E. AUTO SELECT FIRST AVAILABLE SIZE
    ===================================================== */

    function autoSelectFirstSize(
        slide
    ) {

        if (!slide) {
            return;
        }


        const sizeButtons =
            slide.querySelectorAll(
                ".size-btn"
            );


        const quantityInput =
            slide.querySelector(
                ".qty-input"
            );


        if (!sizeButtons.length) {

            if (quantityInput) {

                const defaultMax =
                    parseInt(
                        quantityInput.dataset.defaultMax,
                        10
                    ) || 0;


                quantityInput.value =
                    defaultMax > 0
                        ? "1"
                        : "0";

                quantityInput.max =
                    defaultMax;

                quantityInput.disabled =
                    defaultMax <= 0;
            }

            return;
        }


        const availableSizes =
            Array.from(
                sizeButtons
            ).filter(
                (button) => {

                    const stock =
                        parseInt(
                            button.dataset.quantity,
                            10
                        ) || 0;

                    return (
                        stock > 0 &&
                        !button.disabled
                    );
                }
            );


        if (availableSizes.length) {

            availableSizes[0].click();

        } else {

            if (quantityInput) {

                quantityInput.value =
                    "0";

                quantityInput.max =
                    "0";

                quantityInput.disabled =
                    true;
            }
        }
    }


    /* =====================================================
       11F. SHOW ITEM
    ===================================================== */

    function showItem(index) {

        if (!itemSlides.length) {
            return;
        }


        if (index < 0) {
            index = 0;
        }


        if (
            index >=
            itemSlides.length
        ) {

            index =
                itemSlides.length - 1;
        }


        itemSlides.forEach(
            (slide, slideIndex) => {

                if (
                    slideIndex ===
                    index
                ) {

                    slide.style.display =
                        "block";

                    slide.classList.add(
                        "item-enter"
                    );


                    setTimeout(() => {

                        slide.classList.remove(
                            "item-enter"
                        );

                    }, 400);

                } else {

                    slide.style.display =
                        "none";
                }
            }
        );


        currentItemIndex =
            index;


        resetCurrentItemControls();

        updateItemNavigation();

        autoSelectFirstSize(
            itemSlides[
                currentItemIndex
            ]
        );


        const page =
            document.querySelector(
                ".pd-page"
            );


        if (page) {

            page.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        } else {

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        }
    }


    if (prevButton) {

        prevButton.addEventListener(
            "click",
            () => {

                showItem(
                    currentItemIndex - 1
                );
            }
        );
    }


    if (nextButton) {

        nextButton.addEventListener(
            "click",
            () => {

                showItem(
                    currentItemIndex + 1
                );
            }
        );
    }


    updateItemNavigation();


        /* =====================================================
       12. SIZE SELECTION
    ===================================================== */

    itemSlides.forEach(
        (slide) => {

            const sizeButtons =
                slide.querySelectorAll(
                    ".size-btn"
                );

            const quantityInput =
                slide.querySelector(
                    ".qty-input"
                );

            const sizeVariantInput =
                slide.querySelector(
                    'input[name="size_variant_id"]'
                );

            const sizeInfo =
                slide.querySelector(
                    ".size-info"
                );

            const priceElement =
                slide.querySelector(
                    ".item-price"
                );

            if (!sizeButtons.length) {
                return;
            }

            sizeButtons.forEach(
                (sizeButton) => {

                    sizeButton.addEventListener(
                        "click",
                        () => {

                            if (
                                sizeButton.disabled
                            ) {
                                return;
                            }

                            const size =
                                sizeButton.dataset.size;

                            const price =
                                parseInt(
                                    sizeButton.dataset.price,
                                    10
                                ) || 0;

                            const stock =
                                parseInt(
                                    sizeButton.dataset.quantity,
                                    10
                                ) || 0;

                            const variantId =
                                sizeButton.dataset.variantId;

                            sizeButtons.forEach(
                                (button) => {
                                    button.classList.remove(
                                        "selected",
                                        "active"
                                    );
                                }
                            );

                            sizeButton.classList.add(
                                "selected",
                                "active"
                            );

                            if (sizeVariantInput) {
                                sizeVariantInput.value =
                                    variantId || "";
                            }

                            if (priceElement) {
                                priceElement.textContent =
                                    `${price.toLocaleString()} MMK`;
                            }

                            if (quantityInput) {
                                quantityInput.min = "1";
                                quantityInput.max = String(stock);
                                quantityInput.value = stock > 0 ? "1" : "0";
                                quantityInput.disabled = stock <= 0;
                            }

                             const stockDisplay = slide.querySelector('.size-stock-display .stock-text');
                            if (stockDisplay) {
                                stockDisplay.textContent =
                                    stock > 0
                                 ? `${stock} available`
                                  : 'Out of stock';
                            }
                        }
                    );
                }
            );
        }
    );

    /* =====================================================
       13. INITIALIZE ALL SLIDES
    ===================================================== */

    itemSlides.forEach(
        (slide) => {

            autoSelectFirstSize(
                slide
            );
        }
    );


    /* =====================================================
       14. QUANTITY SELECTOR
    ===================================================== */

    itemSlides.forEach(
        (slide) => {

            const minusButton =
                slide.querySelector(
                    ".qty-minus"
                );


            const plusButton =
                slide.querySelector(
                    ".qty-plus"
                );


            const quantityInput =
                slide.querySelector(
                    ".qty-input"
                );


            if (!quantityInput) {
                return;
            }


            function getMaxQuantity() {

                const max =
                    parseInt(
                        quantityInput.max,
                        10
                    );


                if (
                    Number.isFinite(max) &&
                    max > 0
                ) {

                    return max;
                }


                const defaultMax =
                    parseInt(
                        quantityInput.dataset.defaultMax,
                        10
                    );


                return Number.isFinite(
                    defaultMax
                )
                    ? defaultMax
                    : 1;
            }


            function setQuantity(
                value
            ) {

                let quantity =
                    parseInt(
                        value,
                        10
                    );


                if (
                    Number.isNaN(
                        quantity
                    )
                ) {

                    quantity = 1;
                }


                const max =
                    getMaxQuantity();


                quantity =
                    Math.max(
                        1,
                        Math.min(
                            quantity,
                            max
                        )
                    );


                quantityInput.value =
                    quantity;
            }


            if (minusButton) {

                minusButton.addEventListener(
                    "click",
                    (event) => {

                        event.preventDefault();
                        event.stopPropagation();


                        const current =
                            parseInt(
                                quantityInput.value,
                                10
                            ) || 1;


                        setQuantity(
                            current - 1
                        );
                    }
                );
            }


            if (plusButton) {

                plusButton.addEventListener(
                    "click",
                    (event) => {

                        event.preventDefault();
                        event.stopPropagation();


                        const current =
                            parseInt(
                                quantityInput.value,
                                10
                            ) || 1;


                        setQuantity(
                            current + 1
                        );
                    }
                );
            }


            quantityInput.readOnly =
                true;
        }
    );


       /* =====================================================
       15. ADD TO CART
    ===================================================== */

    const addToCartButtons =
        document.querySelectorAll(
            ".add-to-cart-btn"
        );


    addToCartButtons.forEach(
        (button) => {

            button.addEventListener(
                "click",
                async (event) => {

                    event.preventDefault();


                    if (
                        button.dataset.busy ===
                        "true"
                    ) {
                        return;
                    }


                    const slideIndex =
                        parseInt(
                            button.dataset.slideIndex,
                            10
                        );


                    const slide =
                        itemSlides[
                            slideIndex
                        ];


                    if (!slide) {

                        console.error(
                            "Item slide not found."
                        );

                        return;
                    }


                    const itemId =
                        button.dataset.itemId;


                    const quantityInput =
                        slide.querySelector(
                            ".qty-input"
                        );


                    const sizeVariantInput =
                        slide.querySelector(
                            'input[name="size_variant_id"]'
                        );


                    const sizeButtons =
                        slide.querySelectorAll(
                            ".size-btn"
                        );


                    const selectedSize =
                        slide.querySelector(
                            ".size-btn.selected, .size-btn.active"
                        );


                    const quantity =
                        parseInt(
                            quantityInput?.value,
                            10
                        ) || 1;


                    let sizeVariantId =
                        "";


                    /* Size validation */
                    if (
                        sizeButtons.length > 0
                    ) {

                        if (!selectedSize) {

                            showTemporaryMessage(
                                "Please select a size first.",
                                "error"
                            );

                            return;
                        }


                        sizeVariantId =
                            sizeVariantInput?.value ||
                            selectedSize.dataset.variantId ||
                            "";


                        if (!sizeVariantId) {

                            showTemporaryMessage(
                                "Selected size is invalid.",
                                "error"
                            );

                            return;
                        }
                    }


                    /* Quantity validation */
                    if (
                        quantity < 1
                    ) {

                        showTemporaryMessage(
                            "Quantity must be at least 1.",
                            "error"
                        );

                        return;
                    }


                    const maxQuantity =
                        parseInt(
                            quantityInput?.max,
                            10
                        );


                    if (
                        Number.isFinite(
                            maxQuantity
                        ) &&
                        maxQuantity > 0 &&
                        quantity > maxQuantity
                    ) {

                        showTemporaryMessage(
                            `Only ${maxQuantity} item(s) available.`,
                            "error"
                        );

                        return;
                    }


                    /* Loading state */
                    button.dataset.busy =
                        "true";


                    const originalHTML =
                        button.innerHTML;


                    button.disabled =
                        true;


                    button.innerHTML =
                        '<i class="fa-solid fa-spinner fa-spin"></i> Adding...';


                    /* Form data */
                    const formData =
                        new FormData();


                    formData.append(
                        "quantity",
                        quantity
                    );


                    if (sizeVariantId) {

                        formData.append(
                            "size_variant_id",
                            sizeVariantId
                        );
                    }


                    const addCartUrl =
                        `/cart/add/${itemId}/`;


                    try {

                        const response =
                            await fetch(
                                addCartUrl,
                                {
                                    method: "POST",
                                    body: formData,

                                    headers: {
                                        "X-CSRFToken":
                                            getCSRFToken(),

                                        "X-Requested-With":
                                            "XMLHttpRequest",

                                        "Accept":
                                            "application/json"
                                    },

                                    credentials:
                                        "same-origin"
                                }
                            );


                        let data =
                            null;


                        try {

                            data =
                                await response.json();

                        } catch (
                            jsonError
                        ) {

                            throw new Error(
                                "Invalid server response."
                            );
                        }


                        if (
                            !response.ok ||
                            !data.success
                        ) {

                            throw new Error(
                                data.message ||
                                "Unable to add item to cart."
                            );
                        }


                        /* Success */
                        button.innerHTML =
                            '<i class="fa-solid fa-check"></i> Added';


                        button.classList.add(
                            "cart-added"
                        );


                        updateCartCount(
                            data.cart_count
                        );


                        animateCart();


                        showCartToast(
                            data.message ||
                            "Added to cart successfully!"
                        );


                        /* Update stock display */
                        if (
                            selectedSize &&
                            sizeVariantId
                        ) {

                            const currentQty =
                                parseInt(
                                    selectedSize.dataset.quantity,
                                    10
                                ) || 0;


                            const newQty =
                                Math.max(
                                    0,
                                    currentQty -
                                    quantity
                                );


                            selectedSize.dataset.quantity =
                                newQty;


                            /* UPDATE STOCK TEXT */
                            const stockDisplay =
                                slide.querySelector(
                                    '.size-stock-display .stock-text'
                                );


                            if (stockDisplay) {

                                stockDisplay.textContent =
                                    newQty > 0
                                        ? `${newQty} available`
                                        : 'Out of stock';
                            }


                            if (newQty <= 0) {

                                selectedSize.disabled =
                                    true;


                                selectedSize.classList.add(
                                    "sold-out"
                                );


                                selectedSize.classList.remove(
                                    "selected",
                                    "active"
                                );


                                if (
                                    sizeVariantInput
                                ) {

                                    sizeVariantInput.value =
                                        "";
                                }


                                autoSelectFirstSize(
                                    slide
                                );
                            }


                            if (quantityInput) {

                                quantityInput.max =
                                    String(
                                        newQty
                                    );

                                quantityInput.dataset.defaultMax =
                                    String(
                                        newQty
                                    );
                            }


                        } else {

                            /* For non-sized items */
                            const stockDisplay =
                                slide.querySelector(
                                    ".stock-display"
                                );


                            if (stockDisplay) {

                                const currentStock =
                                    parseInt(
                                        stockDisplay.dataset.stock,
                                        10
                                    ) || 0;


                                const newStock =
                                    Math.max(
                                        0,
                                        currentStock -
                                        quantity
                                    );


                                stockDisplay.dataset.stock =
                                    newStock;


                                const stockStrong =
                                    stockDisplay.querySelector(
                                        "strong"
                                    );


                                if (stockStrong) {

                                    if (
                                        newStock > 0
                                    ) {

                                        stockStrong.nextSibling.textContent =
                                            ` ${newStock} available`;

                                    } else {

                                        stockStrong.nextSibling.textContent =
                                            " Out of stock";
                                    }
                                }


                                if (quantityInput) {

                                    quantityInput.max =
                                        String(
                                            newStock
                                        );

                                    quantityInput.dataset.defaultMax =
                                        String(
                                            newStock
                                        );

                                    quantityInput.disabled =
                                        newStock <= 0;
                                }
                            }
                        }


                        /* Reset quantity */
                        if (quantityInput) {

                            quantityInput.value =
                                "1";
                        }


                    } catch (error) {

                        console.error(
                            "Add to cart error:",
                            error
                        );


                        showTemporaryMessage(
                            error.message ||
                            "Something went wrong.",
                            "error"
                        );


                        button.innerHTML =
                            originalHTML;


                    } finally {

                        setTimeout(
                            () => {

                                button.disabled =
                                    false;


                                button.dataset.busy =
                                    "false";


                                button.innerHTML =
                                    originalHTML;


                                button.classList.remove(
                                    "cart-added"
                                );

                            },
                            1500
                        );
                    }
                }
            );
        }
    );


  function sizeInfoForSlide(slide) {
    if (!slide) {
        return null;
    }
    return slide.querySelector(".size-stock-display .stock-text");
}


    /* =====================================================
       16. UPDATE CART COUNT
    ===================================================== */

    function updateCartCount(
        serverCount = null
    ) {

        const cartCounts =
            document.querySelectorAll(
                ".cart-count"
            );


        if (
            serverCount !== null &&
            serverCount !== undefined
        ) {

            cartCounts.forEach(
                (countElement) => {

                    countElement.textContent =
                        serverCount;


                    countElement.classList.remove(
                        "cart-pop"
                    );


                    void countElement.offsetWidth;


                    countElement.classList.add(
                        "cart-pop"
                    );
                }
            );

            return;
        }


        fetch(
            "/cart/count/",
            {
                method: "GET",

                headers: {
                    "X-Requested-With":
                        "XMLHttpRequest",

                    "Accept":
                        "application/json"
                },

                credentials:
                    "same-origin"
            }
        )
        .then(
            (response) => {

                if (!response.ok) {

                    throw new Error(
                        "Cart count request failed."
                    );
                }

                return response.json();
            }
        )
        .then(
            (data) => {

                if (
                    data &&
                    data.cart_count !== undefined
                ) {

                    updateCartCount(
                        data.cart_count
                    );
                }
            }
        )
        .catch(
            (error) => {

                console.error(
                    "Cart count error:",
                    error
                );
            }
        );
    }


    /* =====================================================
       17. CART ANIMATION
    ===================================================== */

    function animateCart() {

        const cartLink =
            document.querySelector(
                ".cart-link"
            );


        if (!cartLink) {
            return;
        }


        cartLink.classList.remove(
            "shake"
        );


        void cartLink.offsetWidth;


        cartLink.classList.add(
            "shake"
        );


        setTimeout(() => {

            cartLink.classList.remove(
                "shake"
            );

        }, 600);
    }


    /* =====================================================
       18. CART TOAST
    ===================================================== */

    function showCartToast(
        message
    ) {

        const toast =
            document.getElementById(
                "cartToast"
            );


        if (!toast) {

            showTemporaryMessage(
                message,
                "success"
            );

            return;
        }


        const toastText =
            toast.querySelector(
                ".toast-message"
            );


        if (toastText) {

            toastText.textContent =
                message;

        } else {

            toast.textContent =
                message;
        }


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


    /* =====================================================
       19. IMAGE SLIDER
    ===================================================== */

    const sliderIntervals =
        new WeakMap();

    const sliderIndexes =
        new WeakMap();


    function getSliderImages(
        slider
    ) {

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
            index %
            images.length;


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
    }


    function startSlide(
        slider
    ) {

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


    function stopSlide(
        slider
    ) {

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


        changeSliderImage(
            slider,
            0
        );
    }


    window.startSlide =
        startSlide;

    window.stopSlide =
        stopSlide;


    document
        .querySelectorAll(
            ".post-image-slider"
        )
        .forEach(
            (slider) => {

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
            }
        );


    /* =====================================================
       20. DETAIL BUTTON
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
                                    easing:
                                        "ease-out"
                                }
                            );
                        }
                    }
                );
            }
        );


    /* =====================================================
       21. SCROLL REVEAL
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
       22. FLOATING MARKET PARTICLES
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
       23. MOUSE GLOW
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


        function animateGlow() {

            glowX +=
                (
                    targetX -
                    glowX
                ) * 0.12;


            glowY +=
                (
                    targetY -
                    glowY
                ) * 0.12;


            mouseGlow.style.left =
                `${glowX}px`;


            mouseGlow.style.top =
                `${glowY}px`;


            requestAnimationFrame(
                animateGlow
            );
        }


        animateGlow();
    }


    /* =====================================================
       24. ESCAPE KEY
    ===================================================== */

    document.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key !==
                "Escape"
            ) {
                return;
            }


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


            const lightbox =
                document.getElementById(
                    "trustyshopImageLightbox"
                );


            if (lightbox) {
                return;
            }


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
       25. PREVENT IMAGE DRAGGING
    ===================================================== */

    document
        .querySelectorAll(
            "img"
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
       26. REDUCED MOTION
    ===================================================== */

    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        );


    function applyReducedMotion() {

        document.documentElement.classList.toggle(
            "reduce-motion",
            reducedMotion.matches
        );
    }


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
       27. RESIZE CLEANUP
    ===================================================== */

    window.addEventListener(
        "resize",
        () => {

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
        },
        {
            passive: true
        }
    );


    /* =====================================================
       28. WISHLIST TOGGLE
       -----------------------------------------------------
       Uses the newer adminAuthenticate wishlist
       button implementation.
    ===================================================== */

    const wishlistButton =
        document.getElementById(
            "wishlistBtn"
        );


    const wishlistIcon =
        document.getElementById(
            "wishlistIcon"
        );


    if (
        wishlistButton &&
        wishlistIcon
    ) {

        wishlistButton.addEventListener(
            "click",
            async () => {

                if (
                    wishlistButton.dataset.busy ===
                    "true"
                ) {
                    return;
                }


                wishlistButton.dataset.busy =
                    "true";


                const isWishlisted =
                    wishlistButton.dataset.wishlisted ===
                    "true";


                const url =
                    isWishlisted
                        ? wishlistButton.dataset.removeUrl
                        : wishlistButton.dataset.addUrl;


                if (!url) {

                    console.error(
                        "Wishlist URL is missing."
                    );


                    wishlistButton.dataset.busy =
                        "false";

                    return;
                }


                try {

                    const response =
                        await fetch(
                            url,
                            {
                                method: "GET",

                                headers: {
                                    "X-Requested-With":
                                        "XMLHttpRequest"
                                },

                                credentials:
                                    "same-origin"
                            }
                        );


                    if (!response.ok) {

                        throw new Error(
                            "Wishlist request failed."
                        );
                    }


                    const data =
                        await response.json();


                    if (!data.success) {

                        throw new Error(
                            data.message ||
                            "Wishlist update failed."
                        );
                    }


                    const newState =
                        Boolean(
                            data.wishlisted
                        );


                    wishlistButton.dataset.wishlisted =
                        newState
                            ? "true"
                            : "false";


                    wishlistButton.classList.toggle(
                        "liked",
                        newState
                    );


                    wishlistIcon.classList.toggle(
                        "fa-solid",
                        newState
                    );


                    wishlistIcon.classList.toggle(
                        "fa-regular",
                        !newState
                    );


                    wishlistIcon.classList.remove(
                        "wishlist-heart-pop"
                    );


                    void wishlistIcon.offsetWidth;


                    wishlistIcon.classList.add(
                        "wishlist-heart-pop"
                    );


                } catch (error) {

                    console.error(
                        "Wishlist error:",
                        error
                    );


                    showTemporaryMessage(
                        error.message ||
                        "Wishlist update failed.",
                        "error"
                    );


                } finally {

                    wishlistButton.dataset.busy =
                        "false";
                }
            }
        );
    }


    /* =====================================================
       29. INITIAL CART COUNT
    ===================================================== */

    if (
        document.querySelector(
            ".cart-count"
        )
    ) {

        updateCartCount();
    }


    /* =====================================================
       30. PAGE READY
    ===================================================== */

    document.documentElement.classList.add(
        "trustyshop-js-ready"
    );

});
