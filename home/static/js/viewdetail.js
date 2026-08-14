/* =========================================================
   TRUSTYSHOP VIEW DETAIL JAVASCRIPT
   CLEAN • STABLE • RESPONSIVE
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* ============ COMMON HELPERS ============ */
    const finePointer = window.matchMedia("(pointer:fine)").matches;

    function getCookie(name) {
        const cookies = document.cookie ? document.cookie.split(";") : [];
        for (const cookie of cookies) {
            const trimmedCookie = cookie.trim();
            if (trimmedCookie.startsWith(`${name}=`)) {
                return decodeURIComponent(trimmedCookie.substring(name.length + 1));
            }
        }
        return null;
    }

    function getCSRFToken() {
        const cookieToken = getCookie("csrftoken");
        if (cookieToken) return cookieToken;
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        return csrfInput ? csrfInput.value : "";
    }

    function showTemporaryMessage(message, type = "error") {
        let messageBox = document.getElementById("viewDetailMessage");
        if (!messageBox) {
            messageBox = document.createElement("div");
            messageBox.id = "viewDetailMessage";
            messageBox.style.position = "fixed";
            messageBox.style.top = "90px";
            messageBox.style.right = "20px";
            messageBox.style.zIndex = "99999";
            messageBox.style.padding = "14px 20px";
            messageBox.style.borderRadius = "12px";
            messageBox.style.fontWeight = "600";
            messageBox.style.boxShadow = "0 10px 30px rgba(0,0,0,.15)";
            messageBox.style.transition = "all .3s ease";
            document.body.appendChild(messageBox);
        }

        messageBox.textContent = message;
        messageBox.style.background = type === "success" ? "#dcfce7" : "#fee2e2";
        messageBox.style.color = type === "success" ? "#166534" : "#991b1b";
        messageBox.style.opacity = "1";

        clearTimeout(messageBox._hideTimer);
        messageBox._hideTimer = setTimeout(() => {
            messageBox.style.opacity = "0";
        }, 2500);
    }

    /* ============ REFRESH ON BACK FROM CART ============ */
    const needsRefresh = sessionStorage.getItem('refreshItemDetail');
    if (needsRefresh === 'true') {
        sessionStorage.removeItem('refreshItemDetail');
        window.location.reload();
    }

    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            const refreshFlag = sessionStorage.getItem('refreshItemDetail');
            if (refreshFlag === 'true') {
                sessionStorage.removeItem('refreshItemDetail');
                window.location.reload();
            }
        }
    });

    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            const refreshFlag = sessionStorage.getItem('refreshItemDetail');
            if (refreshFlag === 'true') {
                sessionStorage.removeItem('refreshItemDetail');
                window.location.reload();
            }
        }
    });

    /* ============ NAVBAR SCROLL ============ */
    const navbar = document.querySelector(".cute-navbar");
    const handleNavbarScroll = () => {
        if (!navbar) return;
        navbar.classList.toggle("scrolled", window.scrollY > 50);
    };
    handleNavbarScroll();
    window.addEventListener("scroll", handleNavbarScroll, { passive: true });

    /* ============ SEARCH ============ */
    const searchInput = document.getElementById("searchInput");
    const searchForm = document.querySelector(".modern-search");
    const suggestionButtons = document.querySelectorAll(".search-suggestions button");

    suggestionButtons.forEach((button) => {
        button.addEventListener("click", () => {
            if (!searchInput) return;
            searchInput.value = button.textContent.trim();
            searchInput.focus();
        });
    });

    if (searchForm) {
        searchForm.addEventListener("submit", (event) => {
            if (!searchInput) return;
            const value = searchInput.value.trim();
            if (!value) {
                event.preventDefault();
                searchInput.focus();
                searchInput.classList.add("search-error");
                setTimeout(() => searchInput.classList.remove("search-error"), 700);
            }
        });
    }

    /* ============ SCROLL TO TOP ============ */
    let topButton = document.querySelector(".top-btn");
    if (!topButton) {
        topButton = document.createElement("button");
        topButton.className = "top-btn";
        topButton.type = "button";
        topButton.setAttribute("aria-label", "Scroll to top");
        topButton.innerHTML = '<i class="fa-solid fa-arrow-up"></i>';
        document.body.appendChild(topButton);
    }

    const handleTopButton = () => {
        topButton.style.display = window.scrollY > 500 ? "flex" : "none";
    };
    handleTopButton();
    window.addEventListener("scroll", handleTopButton, { passive: true });
    topButton.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    /* ============ CUSTOM CURSOR ============ */
    const cursor = document.querySelector(".cursor");
    const follower = document.querySelector(".cursor-follower");

    if (cursor && follower && finePointer) {
        let mouseX = 0, mouseY = 0, followerX = 0, followerY = 0;

        document.addEventListener("mousemove", (event) => {
            mouseX = event.clientX;
            mouseY = event.clientY;
            cursor.style.left = `${mouseX}px`;
            cursor.style.top = `${mouseY}px`;
        });

        const animateFollower = () => {
            followerX += (mouseX - followerX) * 0.15;
            followerY += (mouseY - followerY) * 0.15;
            follower.style.left = `${followerX}px`;
            follower.style.top = `${followerY}px`;
            requestAnimationFrame(animateFollower);
        };
        animateFollower();
    }

    /* ============ MESSAGE ALERT ============ */
    const messageOverlay = document.getElementById("messageOverlay");
    if (messageOverlay) {
        messageOverlay.style.display = "flex";
        messageOverlay.style.opacity = "1";
        const messageType = messageOverlay.getAttribute("data-message-type");
        const isPending = messageType === "pending";

        window.closeSuccessAlert = () => {
            if (!messageOverlay || !document.body.contains(messageOverlay)) return;
            if (messageOverlay.dataset.closing === "true") return;
            messageOverlay.dataset.closing = "true";
            messageOverlay.classList.add("message-closing");
            setTimeout(() => {
                if (messageOverlay && document.body.contains(messageOverlay)) {
                    messageOverlay.remove();
                }
            }, 300);
        };

        if (!isPending) {
            setTimeout(() => window.closeSuccessAlert(), 2000);
        }
    }

    /* ============ ITEM VIEWER ============ */
    const itemSlides = document.querySelectorAll(".item-slide");
    const prevButton = document.getElementById("prevBtn");
    const nextButton = document.getElementById("nextBtn");
    const itemCounter = document.getElementById("itemCounter");
    let currentItemIndex = 0;

    function getCurrentSlide() {
        return itemSlides[currentItemIndex] || null;
    }

    function updateItemNavigation() {
        const total = itemSlides.length;
        if (itemCounter) itemCounter.textContent = `Item ${currentItemIndex + 1} of ${total}`;
        if (prevButton) prevButton.disabled = currentItemIndex <= 0;
        if (nextButton) nextButton.disabled = currentItemIndex >= total - 1;
    }

    /* ============ AUTO SELECT FIRST SIZE ============ */
    function autoSelectFirstSize(slide) {
        if (!slide) return;

        const sizeButtons = slide.querySelectorAll(".size-btn");
        const quantityInput = slide.querySelector(".qty-input");

        if (!sizeButtons.length) {
            if (quantityInput) {
                const defaultMax = parseInt(quantityInput.dataset.defaultMax) || 0;
                quantityInput.value = 1;
                quantityInput.max = defaultMax;
                quantityInput.disabled = defaultMax <= 0;
            }
            return;
        }

        const availableSizes = Array.from(sizeButtons).filter(btn => {
            const stock = parseInt(btn.dataset.quantity) || 0;
            return stock > 0 && !btn.disabled;
        });

        if (availableSizes.length > 0) {
            availableSizes[0].click();
        } else {
            if (quantityInput) {
                quantityInput.value = 1;
                quantityInput.max = 0;
                quantityInput.disabled = true;
            }
        }
    }

    function showItem(index) {
        if (!itemSlides.length) return;
        if (index < 0) index = 0;
        if (index >= itemSlides.length) index = itemSlides.length - 1;

        itemSlides.forEach((slide, slideIndex) => {
            slide.style.display = slideIndex === index ? "block" : "none";
        });

        currentItemIndex = index;
        updateItemNavigation();

        autoSelectFirstSize(itemSlides[currentItemIndex]);

        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    if (prevButton) {
        prevButton.addEventListener("click", () => showItem(currentItemIndex - 1));
    }
    if (nextButton) {
        nextButton.addEventListener("click", () => showItem(currentItemIndex + 1));
    }
    updateItemNavigation();

    /* ============ SIZE SELECTION ============ */
    itemSlides.forEach((slide) => {
        const sizeButtons = slide.querySelectorAll(".size-btn");
        const quantityInput = slide.querySelector(".qty-input");
        const sizeVariantInput = slide.querySelector('input[name="size_variant_id"]');
        const sizeInfo = slide.querySelector(".size-info");
        const priceElement = slide.querySelector(".item-price");

        if (!sizeButtons.length) return;

        sizeButtons.forEach((sizeButton) => {
            sizeButton.addEventListener("click", () => {
                if (sizeButton.disabled) return;

                const size = sizeButton.dataset.size;
                const price = parseInt(sizeButton.dataset.price, 10) || 0;
                const stock = parseInt(sizeButton.dataset.quantity, 10) || 0;
                const variantId = sizeButton.dataset.variantId;

                sizeButtons.forEach((button) => button.classList.remove("selected", "active"));
                sizeButton.classList.add("selected", "active");

                if (sizeVariantInput) sizeVariantInput.value = variantId;
                if (priceElement) priceElement.textContent = `${price.toLocaleString()} MMK`;

                if (quantityInput) {
                    quantityInput.min = "1";
                    quantityInput.max = String(stock);
                    quantityInput.value = "1";
                    quantityInput.disabled = false;
                }

                if (sizeInfo) {
                    sizeInfo.textContent = `${size} • ${price.toLocaleString()} MMK • ${stock} available`;
                }
            });
        });
    });

    /* ============ INITIALIZE ALL SLIDES WITH AUTO SELECT ============ */
    itemSlides.forEach((slide) => {
        autoSelectFirstSize(slide);
    });

    /* ============ QUANTITY SELECTOR ============ */
    itemSlides.forEach((slide) => {
        const minusButton = slide.querySelector(".qty-minus");
        const plusButton = slide.querySelector(".qty-plus");
        const quantityInput = slide.querySelector(".qty-input");

        if (!quantityInput) return;

        function getMaxQuantity() {
            const max = parseInt(quantityInput.max, 10);
            if (Number.isFinite(max) && max > 0) return max;
            const defaultMax = parseInt(quantityInput.dataset.defaultMax, 10);
            return Number.isFinite(defaultMax) ? defaultMax : 1;
        }

        function setQuantity(value) {
            let quantity = parseInt(value, 10);
            if (Number.isNaN(quantity)) quantity = 1;
            const max = getMaxQuantity();
            quantity = Math.max(1, Math.min(quantity, max));
            quantityInput.value = quantity;
        }

        if (minusButton) {
            minusButton.addEventListener("click", (event) => {
                event.preventDefault();
                event.stopPropagation();
                const current = parseInt(quantityInput.value, 10) || 1;
                setQuantity(current - 1);
            });
        }

        if (plusButton) {
            plusButton.addEventListener("click", (event) => {
                event.preventDefault();
                event.stopPropagation();
                const current = parseInt(quantityInput.value, 10) || 1;
                setQuantity(current + 1);
            });
        }

        quantityInput.readOnly = true;
    });

    /* ============ ADD TO CART ============ */
    const addToCartButtons = document.querySelectorAll(".add-to-cart-btn");

    addToCartButtons.forEach((button) => {
        button.addEventListener("click", async (event) => {
            event.preventDefault();

            if (button.dataset.busy === "true") return;

            const slideIndex = parseInt(button.dataset.slideIndex, 10);
            const slide = itemSlides[slideIndex];

            if (!slide) {
                console.error("Item slide not found.");
                return;
            }

            const itemId = button.dataset.itemId;
            const quantityInput = slide.querySelector(".qty-input");
            const sizeVariantInput = slide.querySelector('input[name="size_variant_id"]');
            const sizeButtons = slide.querySelectorAll(".size-btn");
            const selectedSize = slide.querySelector(".size-btn.selected, .size-btn.active");

            const quantity = parseInt(quantityInput?.value, 10) || 1;

            let sizeVariantId = "";

            if (sizeButtons.length > 0) {
                if (!selectedSize) {
                    showTemporaryMessage("Please select a size first.", "error");
                    return;
                }
                sizeVariantId = sizeVariantInput?.value || selectedSize.dataset.variantId || "";
                if (!sizeVariantId) {
                    showTemporaryMessage("Selected size is invalid.", "error");
                    return;
                }
            }

            if (quantity < 1) {
                showTemporaryMessage("Quantity must be at least 1.", "error");
                return;
            }

            const maxQuantity = parseInt(quantityInput?.max, 10);
            if (Number.isFinite(maxQuantity) && quantity > maxQuantity) {
                showTemporaryMessage(`Only ${maxQuantity} item(s) available.`, "error");
                return;
            }

            button.dataset.busy = "true";
            const originalHTML = button.innerHTML;
            button.disabled = true;
            button.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Adding...';

            const formData = new FormData();
            formData.append("quantity", quantity);
            if (sizeVariantId) {
                formData.append("size_variant_id", sizeVariantId);
            }

            const addCartUrl = `/cart/add/${itemId}/`;

            try {
                const response = await fetch(addCartUrl, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                        "X-Requested-With": "XMLHttpRequest",
                        "Accept": "application/json"
                    },
                    credentials: "same-origin"
                });

                let data = null;
                try {
                    data = await response.json();
                } catch (jsonError) {
                    throw new Error("Invalid server response.");
                }

                if (!response.ok || !data.success) {
                    throw new Error(data.message || "Unable to add item to cart.");
                }

                button.innerHTML = '<i class="fa-solid fa-check"></i> Added';
                button.classList.add("cart-added");

                updateCartCount(data.cart_count);
                animateCart();
                showCartToast(data.message || "Added to cart successfully!");

                if (selectedSize && sizeVariantId) {
                    const currentQty = parseInt(selectedSize.dataset.quantity) || 0;
                    const newQty = currentQty - quantity;
                    selectedSize.dataset.quantity = newQty;

                    const sizeInfo = slide.querySelector(".size-info");
                    if (sizeInfo) {
                        if (newQty > 0) {
                            sizeInfo.textContent = `${selectedSize.dataset.size} • ${parseInt(selectedSize.dataset.price).toLocaleString()} MMK • ${newQty} available`;
                        } else {
                            sizeInfo.textContent = `${selectedSize.dataset.size} • Out of stock`;
                        }
                    }

                    if (newQty <= 0) {
                        selectedSize.disabled = true;
                        selectedSize.classList.add("sold-out");
                        selectedSize.classList.remove("selected", "active");
                    }

                    if (sizeVariantInput) sizeVariantInput.value = '';
                    slide.querySelectorAll(".size-btn").forEach(btn => btn.classList.remove("selected", "active"));

                    autoSelectFirstSize(slide);

                } else {
                    const stockDisplay = slide.querySelector(".stock-display");
                    if (stockDisplay) {
                        const currentStock = parseInt(stockDisplay.dataset.stock) || 0;
                        const newStock = currentStock - quantity;
                        stockDisplay.dataset.stock = newStock;

                        const stockStrong = stockDisplay.querySelector("strong");
                        if (stockStrong) {
                            if (newStock > 0) {
                                stockStrong.nextSibling.textContent = ` ${newStock} available`;
                            } else {
                                stockStrong.nextSibling.textContent = ' Out of stock';
                            }
                        }

                        if (quantityInput) {
                            quantityInput.max = newStock;
                            quantityInput.dataset.defaultMax = newStock;
                        }
                    }
                }

                if (quantityInput) {
                    quantityInput.value = '1';
                }

            } catch (error) {
                console.error("Add to cart error:", error);
                showTemporaryMessage(error.message || "Something went wrong.", "error");
                button.innerHTML = originalHTML;
            } finally {
                setTimeout(() => {
                    button.disabled = false;
                    button.dataset.busy = "false";
                    button.innerHTML = originalHTML;
                    button.classList.remove("cart-added");
                }, 1500);
            }
        });
    });

    /* ============ UPDATE CART COUNT ============ */
    function updateCartCount(serverCount = null) {
        const cartCounts = document.querySelectorAll(".cart-count");

        if (serverCount !== null && serverCount !== undefined) {
            cartCounts.forEach((countElement) => {
                countElement.textContent = serverCount;
                countElement.classList.remove("cart-pop");
                void countElement.offsetWidth;
                countElement.classList.add("cart-pop");
            });
            return;
        }

        fetch("/cart/count/", {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json"
            },
            credentials: "same-origin"
        })
        .then((response) => {
            if (!response.ok) throw new Error("Cart count request failed.");
            return response.json();
        })
        .then((data) => {
            if (data && data.cart_count !== undefined) {
                updateCartCount(data.cart_count);
            }
        })
        .catch((error) => {
            console.error("Cart count error:", error);
        });
    }

    /* ============ CART ANIMATION ============ */
    function animateCart() {
        const cartLink = document.querySelector(".cart-link");
        if (!cartLink) return;
        cartLink.classList.remove("shake");
        void cartLink.offsetWidth;
        cartLink.classList.add("shake");
        setTimeout(() => cartLink.classList.remove("shake"), 600);
    }

    /* ============ CART TOAST ============ */
    function showCartToast(message) {
        const toast = document.getElementById("cartToast");
        if (!toast) {
            showTemporaryMessage(message, "success");
            return;
        }
        const toastText = toast.querySelector(".toast-message");
        if (toastText) toastText.textContent = message;
        else toast.textContent = message;
        toast.classList.add("show");
        clearTimeout(toast._hideTimer);
        toast._hideTimer = setTimeout(() => toast.classList.remove("show"), 2200);
    }

    /* ============ IMAGE SLIDER ============ */
    const sliderIntervals = new WeakMap();
    const sliderIndexes = new WeakMap();

    function getSliderImages(slider) {
        if (!slider) return [];
        const data = slider.dataset.images;
        if (!data) return [];
        return data.split(",").map((image) => image.trim()).filter(Boolean);
    }

    function changeSliderImage(slider, index) {
        const images = getSliderImages(slider);
        if (!images.length) return;
        const imageElement = slider.querySelector("img");
        if (!imageElement) return;
        index = index % images.length;
        if (index < 0) index = images.length - 1;
        sliderIndexes.set(slider, index);
        imageElement.style.opacity = "0";
        setTimeout(() => {
            imageElement.src = images[index];
            imageElement.style.opacity = "1";
        }, 150);
    }

    function startSlide(slider) {
        if (!slider) return;
        const images = getSliderImages(slider);
        if (images.length <= 1) return;
        if (sliderIntervals.has(slider)) return;
        let index = sliderIndexes.get(slider) || 0;
        const interval = setInterval(() => {
            index = (index + 1) % images.length;
            changeSliderImage(slider, index);
        }, 1500);
        sliderIntervals.set(slider, interval);
    }

    function stopSlide(slider) {
        if (!slider) return;
        const interval = sliderIntervals.get(slider);
        if (interval) {
            clearInterval(interval);
            sliderIntervals.delete(slider);
        }
        changeSliderImage(slider, 0);
    }

    window.startSlide = startSlide;
    window.stopSlide = stopSlide;

    document.querySelectorAll(".post-image-slider").forEach((slider) => {
        slider.addEventListener("mouseenter", () => {
            if (finePointer) startSlide(slider);
        });
        slider.addEventListener("mouseleave", () => {
            if (finePointer) stopSlide(slider);
        });
    });

    /* ============ WISHLIST FUNCTIONALITY ============ */
    document.querySelectorAll('.wishlist-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            const postId = this.dataset.postId;
            const isWishlisted = this.classList.contains('wishlisted');

            if (isWishlisted) {
                removeFromWishlist(postId, this);
            } else {
                addToWishlist(postId, this);
            }
        });
    });

    function addToWishlist(postId, button) {
        const csrftoken = getCookie('csrftoken');
        const originalContent = button.innerHTML;
        button.disabled = true;
        button.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

        fetch(`/wishlist/add/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                button.classList.add('wishlisted');
                button.innerHTML = '<i class="fa-solid fa-heart"></i> Wishlisted';
                button.style.color = '#dc3545';
                button.style.borderColor = '#dc3545';
                showToast('Added to wishlist', 'success');
            } else {
                showToast(data.message || 'Error adding to wishlist', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('An error occurred. Please try again.', 'error');
        })
        .finally(() => {
            button.disabled = false;
        });
    }

    function removeFromWishlist(postId, button) {
        const csrftoken = getCookie('csrftoken');
        const originalContent = button.innerHTML;
        button.disabled = true;
        button.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

        fetch(`/wishlist/remove/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                button.classList.remove('wishlisted');
                button.innerHTML = '<i class="fa-regular fa-heart"></i> Wishlist';
                button.style.color = '';
                button.style.borderColor = '';
                showToast('Removed from wishlist', 'success');
            } else {
                showToast(data.message || 'Error removing from wishlist', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('An error occurred. Please try again.', 'error');
        })
        .finally(() => {
            button.disabled = false;
        });
    }

    function showToast(message, type) {
        let toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toastContainer';
            toastContainer.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
            `;
            document.body.appendChild(toastContainer);
        }

        const toast = document.createElement('div');
        toast.style.cssText = `
            padding: 15px 20px;
            margin-bottom: 10px;
            border-radius: 5px;
            color: white;
            font-weight: 500;
            animation: slideIn 0.3s ease;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            ${type === 'success' ? 'background: #28a745;' : 'background: #dc3545;'}
        `;
        toast.textContent = message;

        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3000);
    }

    /* ============ PREVENT IMAGE DRAGGING ============ */
    document.querySelectorAll("img").forEach((image) => {
        image.setAttribute("draggable", "false");
        image.addEventListener("dragstart", (event) => event.preventDefault());
    });

    /* ============ INITIAL CART COUNT ============ */
    if (document.querySelector(".cart-count")) {
        updateCartCount();
    }

    /* ============ PAGE READY ============ */
    document.documentElement.classList.add("trustyshop-js-ready");

});