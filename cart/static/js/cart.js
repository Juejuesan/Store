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
        prevBtn.addEventListener('click', () => {
            if (currentSlide > 0) showSlide(currentSlide - 1);
        });

        nextBtn.addEventListener('click', () => {
            if (currentSlide < totalSlides - 1) showSlide(currentSlide + 1);
        });
    }

    // ============ SIZE SELECTION ============
    document.querySelectorAll('.size-btn').forEach(button => {
        button.addEventListener('click', function() {
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

            // Highlight selected
            slide.querySelectorAll('.size-btn').forEach(btn => btn.classList.remove('selected'));
            this.classList.add('selected');

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
            minusBtn.addEventListener('click', function() {
                let value = parseInt(input.value);
                if (value > 1) input.value = value - 1;
            });
        }

        if (plusBtn) {
            plusBtn.addEventListener('click', function() {
                let value = parseInt(input.value);
                let max = parseInt(input.dataset.defaultMax);
                if (value < max) input.value = value + 1;
            });
        }
    });

    // ============ ADD TO CART (AJAX) ============
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function() {
            const slideIndex = this.dataset.slideIndex;
            const itemId = this.dataset.itemId;
            const slide = document.getElementById('itemSlide' + slideIndex);

            // Get selected size variant
            let sizeVariantId = null;
            const sizeVariantInput = document.getElementById('sizeVariantId' + slideIndex);

            if (sizeVariantInput) {
                sizeVariantId = sizeVariantInput.value;

                if (!sizeVariantId) {
                    toastr.warning('Please select a size first');
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
                    toastr.success(data.message);

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
                            }
                        }

                        // Reset size selection
                        sizeVariantInput.value = '';
                        slide.querySelectorAll('.size-btn').forEach(btn => btn.classList.remove('selected'));

                        // Disable add to cart button
                        this.disabled = true;

                    } else {
                        // For non-sized items - update simple quantity display
                        const stockText = slide.querySelector('p strong');
                        if (stockText && stockText.textContent.includes('Stock:')) {
                            const currentStock = parseInt(stockText.nextSibling.textContent);
                            const newStock = currentStock - quantity;

                            if (newStock > 0) {
                                stockText.nextSibling.textContent = ` ${newStock} available`;
                            } else {
                                stockText.nextSibling.textContent = ` Out of stock`;
                                this.disabled = true;
                                this.innerHTML = '<i class="fa-solid fa-cart-shopping"></i> Out of Stock';
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
                    toastr.error(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                toastr.error('An error occurred. Please try again.');
            })
            .finally(() => {
                // Restore button if not disabled due to out of stock
                if (!this.disabled || this.innerHTML.includes('Out of Stock')) {
                    // Keep disabled if out of stock
                } else {
                    this.disabled = false;
                }
                this.innerHTML = originalText;
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