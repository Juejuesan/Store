// viewdetail.js - Handles item viewer, size selection, and add to cart

document.addEventListener('DOMContentLoaded', function() {
    // ============ ITEM NAVIGATION ============
    let currentSlide = 0;
    const slides = document.querySelectorAll('.item-slide');
    const totalSlides = slides.length;
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const itemCounter = document.getElementById('itemCounter');

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.style.display = i === index ? 'block' : 'none';
        });

        if (itemCounter) {
            itemCounter.textContent = `Item ${index + 1} of ${totalSlides}`;
        }

        if (prevBtn) prevBtn.disabled = index === 0;
        if (nextBtn) nextBtn.disabled = index === totalSlides - 1;

        currentSlide = index;
    }

    if (prevBtn && nextBtn) {
        prevBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (currentSlide > 0) showSlide(currentSlide - 1);
        });

        nextBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (currentSlide < totalSlides - 1) showSlide(currentSlide + 1);
        });
    }

    // ============ SIZE SELECTION ============
    document.querySelectorAll('.size-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            const slide = this.closest('.item-slide');
            const slideIndex = slide.id.replace('itemSlide', '');

            // Update hidden input
            const variantInput = document.getElementById('sizeVariantId' + slideIndex);
            if (variantInput) {
                variantInput.value = this.dataset.variantId;
            }

            // Update price
            const priceDisplay = document.getElementById('itemPrice' + slideIndex);
            if (priceDisplay) {
                priceDisplay.textContent = this.dataset.price + ' MMK';
            }

            // Update size info
            const sizeInfo = document.getElementById('sizeInfo' + slideIndex);
            if (sizeInfo) {
                sizeInfo.textContent = `Size ${this.dataset.size}: ${this.dataset.price} MMK (${this.dataset.quantity} available)`;
            }

            // Highlight selected - use 'active' class to match your HTML
            slide.querySelectorAll('.size-btn').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Enable add to cart
            const addBtn = slide.querySelector('.add-to-cart-btn');
            if (addBtn) {
                addBtn.disabled = false;
            }
        });
    });

    // ============ QUANTITY SELECTOR ============
    document.querySelectorAll('.qty-selector').forEach(selector => {
        const input = selector.querySelector('.qty-input');
        const minusBtn = selector.querySelector('.qty-minus');
        const plusBtn = selector.querySelector('.qty-plus');

        if (minusBtn) {
            minusBtn.addEventListener('click', function(e) {
                e.preventDefault();
                let value = parseInt(input.value);
                if (value > 1) input.value = value - 1;
            });
        }

        if (plusBtn) {
            plusBtn.addEventListener('click', function(e) {
                e.preventDefault();
                let value = parseInt(input.value);
                let max = parseInt(input.dataset.defaultMax);
                if (value < max) input.value = value + 1;
            });
        }
    });

    // ============ ADD TO CART (AJAX) ============
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            const slideIndex = this.dataset.slideIndex;
            const itemId = this.dataset.itemId;
            const slide = document.getElementById('itemSlide' + slideIndex);

            // Get selected size variant
            let sizeVariantId = null;
            const sizeVariantInput = document.getElementById('sizeVariantId' + slideIndex);

            if (sizeVariantInput) {
                sizeVariantId = sizeVariantInput.value;

                if (!sizeVariantId) {
                    alert('Please select a size first');
                    return;
                }
            }

            // Get quantity
            const quantityInput = document.getElementById('qty' + slideIndex);
            const quantity = quantityInput ? parseInt(quantityInput.value) : 1;

            // Disable button and show loading
            const originalText = this.innerHTML;
            this.disabled = true;
            this.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Adding...';

            // Prepare data
            const formData = new FormData();
            formData.append('quantity', quantity);
            if (sizeVariantId) {
                formData.append('size_variant_id', sizeVariantId);
            }

            // Get CSRF token
            const csrftoken = getCookie('csrftoken');

            // Send AJAX request
            fetch(`/cart/add/${itemId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);

                    // Update cart badge if exists
                    if (data.cart_count !== undefined) {
                        updateCartBadge(data.cart_count);
                    }

                    // Update stock display
                    if (sizeVariantInput && sizeVariantId) {
                        // For sized items
                        const selectedSizeBtn = slide.querySelector(`.size-btn[data-variant-id="${sizeVariantId}"]`);
                        if (selectedSizeBtn) {
                            const currentQty = parseInt(selectedSizeBtn.dataset.quantity);
                            const newQty = currentQty - quantity;
                            selectedSizeBtn.dataset.quantity = newQty;

                            // Update size info
                            const sizeInfo = document.getElementById('sizeInfo' + slideIndex);
                            if (sizeInfo) {
                                if (newQty > 0) {
                                    sizeInfo.textContent = `Size ${selectedSizeBtn.dataset.size}: ${selectedSizeBtn.dataset.price} MMK (${newQty} available)`;
                                } else {
                                    sizeInfo.textContent = `Size ${selectedSizeBtn.dataset.size}: Out of stock`;
                                }
                            }

                            // Disable if out of stock
                            if (newQty <= 0) {
                                selectedSizeBtn.disabled = true;
                                selectedSizeBtn.classList.add('sold-out');
                                selectedSizeBtn.classList.remove('active');
                            }
                        }

                        // Reset size selection
                        sizeVariantInput.value = '';
                        slide.querySelectorAll('.size-btn').forEach(btn => btn.classList.remove('active'));
                        this.disabled = true;

                    } else {
                        // For non-sized items - update simple quantity display
                        const stockDisplay = slide.querySelector('.stock-display');
                        if (stockDisplay) {
                            const currentStock = parseInt(stockDisplay.dataset.stock);
                            const newStock = currentStock - quantity;
                            stockDisplay.dataset.stock = newStock;

                            const stockStrong = stockDisplay.querySelector('strong');
                            if (stockStrong) {
                                if (newStock > 0) {
                                    stockStrong.nextSibling.textContent = ` ${newStock} available`;
                                } else {
                                    stockStrong.nextSibling.textContent = ` Out of stock`;
                                    this.disabled = true;
                                    this.innerHTML = '<i class="fa-solid fa-cart-shopping"></i> Out of Stock';
                                }
                            }

                            // Update max quantity
                            if (quantityInput) {
                                quantityInput.max = newStock;
                                quantityInput.dataset.defaultMax = newStock;
                            }
                        }
                    }

                    // Reset quantity to 1
                    if (quantityInput) {
                        quantityInput.value = 1;
                    }

                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            })
            .finally(() => {
                // Restore button
                if (!this.innerHTML.includes('Out of Stock')) {
                    this.disabled = false;
                    this.innerHTML = originalText;
                }
            });
        });
    });

    // ============ THUMBNAIL HANDLING ============
    document.querySelectorAll('.thumbnail').forEach(thumb => {
        thumb.addEventListener('click', function() {
            const slide = this.closest('.item-slide');
            const mainImage = slide.querySelector('.main-image');

            if (mainImage) {
                mainImage.src = this.src;
                slide.querySelectorAll('.thumbnail').forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });

    // ============ HELPER FUNCTIONS ============
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function updateCartBadge(count) {
        const cartBadge = document.getElementById('cartBadge');
        if (cartBadge) {
            cartBadge.textContent = count;
            if (count > 0) {
                cartBadge.style.display = 'inline-block';
            } else {
                cartBadge.style.display = 'none';
            }
        }
    }
});

// Function to load cart count on page load
function loadCartCount() {
    fetch('/cart/count/')  // You need to create this endpoint
    .then(response => response.json())
    .then(data => {
        updateCartBadge(data.cart_count);
    })
    .catch(error => {
        console.error('Error loading cart count:', error);
    });
}

// Call on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCartCount();
});

