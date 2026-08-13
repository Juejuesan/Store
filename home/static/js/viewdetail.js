/* =========================================================
   TRUSTYSHOP VIEW DETAIL JAVASCRIPT
   CLEAN • STABLE • RESPONSIVE

   FEATURES
   ---------------------------------------------------------
   1. Navbar scroll effect
   2. Search
   3. Scroll to top
   4. Logo click animation
   5. Custom cursor
   6. Message alert
   7. Seller card hover
   8. Button ripple
   9. Item navigation
   10. Size selection
   11. Quantity + / -
   12. Add to cart
   13. Cart count
   14. Cart toast
   15. Wishlist
   16. Image slider
   17. Escape key
   18. Image drag prevention
   19. Reduced motion
   20. Resize cleanup
========================================================= */


document.addEventListener("DOMContentLoaded", () => {


    /* =====================================================
       1. COMMON HELPERS
    ===================================================== */

    const finePointer = window.matchMedia(
        "(pointer:fine)"
    ).matches;


    function getCookie(name) {

        const cookies = document.cookie
            ? document.cookie.split(";")
            : [];

        for (const cookie of cookies) {

            const trimmedCookie = cookie.trim();

            if (
                trimmedCookie.startsWith(
                    `${name}=`
                )
            ) {

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


        messageBox.textContent = message;

        messageBox.style.background =
            type === "success"
                ? "#dcfce7"
                : "#fee2e2";

        messageBox.style.color =
            type === "success"
                ? "#166534"
                : "#991b1b";

        messageBox.style.opacity = "1";


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
       2. NAVBAR SCROLL EFFECT
    ===================================================== */

    const navbar =
        document.querySelector(
            ".cute-navbar"
        );


    const handleNavbarScroll = () => {

        if (!navbar) {
            return;
        }

        navbar.classList.toggle(
            "scrolled",
            window.scrollY > 50
        );
    };


    handleNavbarScroll();


    window.addEventListener(
        "scroll",
        handleNavbarScroll,
        {
            passive: true
        }
    );


    /* =====================================================
       3. SEARCH
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
       4. SCROLL TO TOP
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
       5. LOGO CLICK EFFECT
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
       6. CUSTOM CURSOR
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


        const animateFollower = () => {

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
        };


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
                ".add-to-cart-btn"
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
       7. MESSAGE ALERT
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


        if (!isPending) {

            setTimeout(() => {

                window.closeSuccessAlert();

            }, 2000);
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
       8. SELLER CARD 3D HOVER
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
       9. BUTTON RIPPLE
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
       10. ITEM VIEWER
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

        return itemSlides[
            currentItemIndex
        ] || null;
    }


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


        const sizeButtons =
            slide.querySelectorAll(
                ".size-btn"
            );


        const sizeVariantInput =
            slide.querySelector(
                'input[name="size_variant_id"]'
            );


        const sizeInfo =
            slide.querySelector(
                ".size-info"
            );


        const item =
            slide.dataset.itemId;


        if (quantityInput) {

            quantityInput.value = 1;

            quantityInput.max =
                quantityInput.dataset.defaultMax ||
                "1";
        }


        sizeButtons.forEach(
            (button) => {

                button.classList.remove(
                    "selected",
                    "active"
                );
            }
        );


        if (sizeVariantInput) {

            sizeVariantInput.value =
                "";
        }


        if (sizeInfo) {

            sizeInfo.textContent =
                "Select a size to see price and stock";
        }


        const originalPrice =
            slide.querySelector(
                ".item-price"
            );


        if (originalPrice) {

            const firstSize =
                slide.querySelector(
                    ".size-btn"
                );


            if (firstSize) {

                const basePrice =
                    firstSize.dataset.price;

                if (basePrice) {

                    originalPrice.dataset.originalPrice =
                        basePrice;
                }
            }
        }
    }


    function updateItemNavigation() {

        const total =
            itemSlides.length;


        if (itemCounter) {

            itemCounter.textContent =
                `Item ${currentItemIndex + 1} of ${total}`;
        }


        if (prevButton) {

            prevButton.disabled =
                currentItemIndex <= 0;
        }


        if (nextButton) {

            nextButton.disabled =
                currentItemIndex >= total - 1;
        }
    }


    function showItem(index) {

        if (!itemSlides.length) {
            return;
        }


        if (index < 0) {
            index = 0;
        }


        if (
            index >= itemSlides.length
        ) {
            index =
                itemSlides.length - 1;
        }


        itemSlides.forEach(
            (slide, slideIndex) => {

                slide.style.display =
                    slideIndex === index
                        ? "block"
                        : "none";
            }
        );


        currentItemIndex =
            index;


        resetCurrentItemControls();

        updateItemNavigation();

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
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
       11. SIZE SELECTION
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


                            /* ---------------------------------
                               Remove Previous Selection
                            --------------------------------- */

                            sizeButtons.forEach(
                                (button) => {

                                    button.classList.remove(
                                        "selected",
                                        "active"
                                    );
                                }
                            );


                            /* ---------------------------------
                               Select Current Size
                            --------------------------------- */

                            sizeButton.classList.add(
                                "selected",
                                "active"
                            );


                            /* ---------------------------------
                               Save Variant ID
                            --------------------------------- */

                            if (sizeVariantInput) {

                                sizeVariantInput.value =
                                    variantId;
                            }


                            /* ---------------------------------
                               Update Price
                            --------------------------------- */

                            if (priceElement) {

                                priceElement.textContent =
                                    `${price.toLocaleString()} MMK`;
                            }


                            /* ---------------------------------
                               Update Quantity Limit
                            --------------------------------- */

                            if (quantityInput) {

                                quantityInput.min =
                                    "1";

                                quantityInput.max =
                                    String(stock);


                                let quantity =
                                    parseInt(
                                        quantityInput.value,
                                        10
                                    ) || 1;


                                if (
                                    quantity > stock
                                ) {

                                    quantity =
                                        stock;
                                }


                                if (
                                    quantity < 1
                                ) {

                                    quantity = 1;
                                }


                                quantityInput.value =
                                    quantity;
                            }


                            /* ---------------------------------
                               Update Stock Information
                            --------------------------------- */

                            if (sizeInfo) {

                                sizeInfo.textContent =
                                    `${size} • ${price.toLocaleString()} MMK • ${stock} available`;
                            }
                        }
                    );
                }
            );
        }
    );


    /* =====================================================
       12. QUANTITY SELECTOR
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


            function setQuantity(value) {

                let quantity =
                    parseInt(
                        value,
                        10
                    );


                if (
                    Number.isNaN(quantity)
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


            /*
             * Keep this input readonly so
             * quantity can only be changed
             * using + / - buttons.
             */
            quantityInput.readOnly =
                true;
        }
    );


    /* =====================================================
       13. ADD TO CART
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
                            ".size-btn.selected"
                        );


                    /* -----------------------------------------
                       Quantity
                    ----------------------------------------- */

                    const quantity =
                        parseInt(
                            quantityInput?.value,
                            10
                        ) || 1;


                    /* -----------------------------------------
                       Size Validation
                    ----------------------------------------- */

                    let sizeVariantId = "";


                    if (sizeButtons.length > 0) {

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


                    /* -----------------------------------------
                       Quantity Validation
                    ----------------------------------------- */

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
                        quantity > maxQuantity
                    ) {

                        showTemporaryMessage(
                            `Only ${maxQuantity} item(s) available.`,
                            "error"
                        );

                        return;
                    }


                    /* -----------------------------------------
                       Button Loading State
                    ----------------------------------------- */

                    button.dataset.busy =
                        "true";


                    const originalHTML =
                        button.innerHTML;


                    button.disabled =
                        true;


                    button.innerHTML =
                        '<i class="fa-solid fa-spinner fa-spin"></i> Adding...';


                    /* -----------------------------------------
                       Create Form Data
                    ----------------------------------------- */

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


                    /* -----------------------------------------
                       Add to Cart URL

                       IMPORTANT:
                       cart/urls.py:
                       add/<int:item_id>/
                    ----------------------------------------- */

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


                        let data = null;


                        try {

                            data =
                                await response.json();

                        } catch (jsonError) {

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


                        /* -------------------------------------
                           Success
                        ------------------------------------- */

                        button.innerHTML =
                            '<i class="fa-solid fa-check"></i> Added';


                        button.classList.add(
                            "cart-added"
                        );


                        /* -------------------------------------
                           Update Navbar Cart Count
                        ------------------------------------- */

                        updateCartCount(
                            data.cart_count
                        );


                        /* -------------------------------------
                           Cart Animation
                        ------------------------------------- */

                        animateCart();


                        /* -------------------------------------
                           Toast
                        ------------------------------------- */

                        showCartToast(
                            data.message ||
                            "Added to cart successfully!"
                        );


                        /* -------------------------------------
                           Reset Quantity
                        ------------------------------------- */

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


    /* =====================================================
       14. UPDATE CART COUNT
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
       15. CART ANIMATION
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


        setTimeout(
            () => {

                cartLink.classList.remove(
                    "shake"
                );

            },
            600
        );
    }


    /* =====================================================
       16. CART TOAST
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
       17. DETAIL BUTTON
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
       18. SCROLL REVEAL
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
       19. MARKET FLOATING PARTICLES
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
       20. MOUSE GLOW
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
                (targetX - glowX) *
                0.12;


            glowY +=
                (targetY - glowY) *
                0.12;


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
       21. IMAGE SLIDER
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


        setTimeout(
            () => {

                imageElement.src =
                    images[index];

                imageElement.style.opacity =
                    "1";

            },
            150
        );


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

                const images =
                    getSliderImages(
                        slider
                    );


                const dots =
                    slider.querySelectorAll(
                        ".slider-dot"
                    );


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


                dots.forEach(
                    (dot, index) => {

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
                    }
                );

            }
        );


    /* =====================================================
       22. ESCAPE KEY
    ===================================================== */

    document.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key !== "Escape"
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
       23. PREVENT IMAGE DRAGGING
    ===================================================== */

    document
        .querySelectorAll(
            ".seller-profile, " +
            ".product-image, " +
            ".post-image-slider img, " +
            ".main-image, " +
            ".thumbnail"
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
       24. REDUCED MOTION
    ===================================================== */

    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        );


    const applyReducedMotion =
        () => {

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
       25. RESIZE CLEANUP
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
       26. WISHLIST TOGGLE
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
       27. INITIAL CART COUNT
    ===================================================== */

    if (
        document.querySelector(
            ".cart-count"
        )
    ) {

        updateCartCount();
    }


    /* =====================================================
       28. PAGE READY
    ===================================================== */

    document.documentElement.classList.add(
        "trustyshop-js-ready"
    );

});