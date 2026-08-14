// cart.js - Handles both Add to Cart and Cart View functionality

document.addEventListener('DOMContentLoaded', function() {

    // ============ ADD TO CART FUNCTIONALITY (Item Detail Page) ============

    // Item Navigation
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

    if (prevBtn && nextBtn && totalSlides > 0) {
        prevBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (currentSlide > 0) showSlide(currentSlide - 1);
        });

        nextBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (currentSlide < totalSlides - 1) showSlide(currentSlide + 1);
        });

        // Initialize first slide
        showSlide(0);
    }

    // Size Selection
    document.querySelectorAll('.size-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            const slide = this.closest('.item-slide');
            if (!slide) return;

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
            slide.querySelectorAll('.size-btn').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Enable add to cart
            const addBtn = slide.querySelector('.add-to-cart-btn');
            if (addBtn) {
                addBtn.disabled = false;
            }
        });
    });

    // Quantity Selector
    document.querySelectorAll('.qty-selector').forEach(selector => {
        const input = selector.querySelector('.qty-input');
        const minusBtn = selector.querySelector('.qty-minus');
        const plusBtn = selector.querySelector('.qty-plus');

        if (minusBtn && input) {
            minusBtn.addEventListener('click', function(e) {
                e.preventDefault();
                let value = parseInt(input.value);
                if (value > 1) input.value = value - 1;
            });
        }

        if (plusBtn && input) {
            plusBtn.addEventListener('click', function(e) {
                e.preventDefault();
                let value = parseInt(input.value);
                let max = parseInt(input.dataset.defaultMax || input.max || 99);
                if (value < max) input.value = value + 1;
            });
        }
    });

    // Add to Cart AJAX
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            const slideIndex = this.dataset.slideIndex;
            const itemId = this.dataset.itemId;
            const slide = document.getElementById('itemSlide' + slideIndex);

            if (!slide) return;

            // Get selected size variant
            let sizeVariantId = null;
            const sizeVariantInput = document.getElementById('sizeVariantId' + slideIndex);

            if (sizeVariantInput) {
                sizeVariantId = sizeVariantInput.value;

                if (!sizeVariantId) {
                    showToast('Please select a size first', 'error');
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
                    showToast(data.message, 'success');

                    // Update cart badge
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

                            const sizeInfo = document.getElementById('sizeInfo' + slideIndex);
                            if (sizeInfo) {
                                if (newQty > 0) {
                                    sizeInfo.textContent = `Size ${selectedSizeBtn.dataset.size}: ${selectedSizeBtn.dataset.price} MMK (${newQty} available)`;
                                } else {
                                    sizeInfo.textContent = `Size ${selectedSizeBtn.dataset.size}: Out of stock`;
                                }
                            }

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
                        // For non-sized items
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

                            if (quantityInput) {
                                quantityInput.max = newStock;
                                quantityInput.dataset.defaultMax = newStock;
                            }
                        }
                    }

                    // Reset quantity
                    if (quantityInput) {
                        quantityInput.value = 1;
                    }

                } else {
                    showToast(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('An error occurred. Please try again.', 'error');
            })
            .finally(() => {
                if (!this.innerHTML.includes('Out of Stock')) {
                    this.disabled = false;
                    this.innerHTML = originalText;
                }
            });
        });
    });

    // Thumbnail Handling
    document.querySelectorAll('.thumbnail').forEach(thumb => {
        thumb.addEventListener('click', function() {
            const slide = this.closest('.item-slide');
            if (!slide) return;

            const mainImage = slide.querySelector('.main-image');
            if (mainImage) {
                mainImage.src = this.src;
                slide.querySelectorAll('.thumbnail').forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });

    // ============ CART VIEW FUNCTIONALITY (Cart Page) ============

    // Quantity Controls (Increase/Decrease)
    // Quantity Controls (Increase/Decrease) - UPDATED
document.querySelectorAll('.qty-btn').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();

        const form = this.closest('.qty-form');
        if (!form) return;

        const url = form.action;
        const csrftoken = getCookie('csrftoken');
        const row = this.closest('.cart-item-row'); // ADD THIS LINE

        // Show loading state
        const originalText = this.innerHTML;
        this.disabled = true;
        this.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

        // Submit form via AJAX
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json', // ADD THIS LINE
            },
            body: new FormData(form),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // ALWAYS expect JSON
        })
        .then(data => {
            if (data.success) {
                updateCartUI(data, row); // CHANGE: Use updateCartUI instead of updateCartItemRow
            } else {
                showToast(data.message || 'Error updating quantity', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('An error occurred. Please try again.', 'error');
        })
        .finally(() => {
            this.disabled = false;
            this.innerHTML = originalText;
        });
    });
});

    // Remove Item
    // Remove Item - UPDATED FOR AJAX
document.querySelectorAll('.remove-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // ADD: Prevent default form submission

        if (!confirm('Remove this item from cart?')) {
            return;
        }

        const url = form.action;
        const csrftoken = getCookie('csrftoken');
        const row = this.closest('.cart-item-row');
        const removeBtn = form.querySelector('.remove-btn');

        // Show loading state
        if (removeBtn) {
            removeBtn.disabled = true;
            removeBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
        }

        // Submit via AJAX
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json',
            },
            body: new FormData(form),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Remove row from UI
                if (row) {
                    row.remove();
                }

                // Update cart total
                if (data.cart_total !== undefined) {
                    updateCartTotal(data.cart_total);
                }

                // Update remaining balance
                if (data.remaining_balance !== undefined) {
                    updateRemainingBalance(data.remaining_balance);
                }

                // Update cart count badge
                if (data.cart_count !== undefined) {
                    updateCartBadge(data.cart_count);
                }

                showToast(data.message || 'Item removed', 'success');

                // Check if cart is empty
                const remainingRows = document.querySelectorAll('.cart-item-row');
                if (remainingRows.length === 0) {
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                }
            } else {
                showToast(data.message || 'Error removing item', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('An error occurred. Please try again.', 'error');
        })
        .finally(() => {
            if (removeBtn) {
                removeBtn.disabled = false;
                removeBtn.innerHTML = '<i class="fa-solid fa-trash"></i>';
            }
        });
    });
});

    // Purchase Button
    const purchaseBtn = document.getElementById('purchaseBtn');
    const purchaseModal = document.getElementById('purchaseModal');

    if (purchaseBtn && purchaseModal) {
        purchaseBtn.addEventListener('click', function(e) {
            e.preventDefault();

            if (checkForExpiredHolds()) {
                alert('Some items in your cart have expired. Refreshing cart...');
                window.location.reload();
                return;
            }

            const modal = new bootstrap.Modal(purchaseModal);
            modal.show();
        });
    }

    // Confirm Purchase
    const purchaseForm = document.getElementById('purchaseForm');
    const confirmPurchaseBtn = document.getElementById('confirmPurchaseBtn');

    if (purchaseForm && confirmPurchaseBtn) {
        purchaseForm.addEventListener('submit', function(e) {
            confirmPurchaseBtn.disabled = true;
            confirmPurchaseBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
            showLoadingOverlay('Processing your purchase...');
        });
    }

    // Hold Timers
    updateHoldTimers();
    setInterval(updateHoldTimers, 1000);

    function updateHoldTimers() {
        const holdTimers = document.querySelectorAll('.hold-timer');

        holdTimers.forEach(timer => {
            const expiresAt = new Date(timer.getAttribute('data-expires'));
            const now = new Date();
            const timeLeft = expiresAt - now;

            if (timeLeft <= 0) {
                timer.innerHTML = '<span class="text-danger">Expired</span>';
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
                return;
            }

            const countdownSpan = timer.querySelector('.countdown');
            if (countdownSpan) {
                countdownSpan.textContent = formatTimeLeft(timeLeft);
            }
        });
    }

    function formatTimeLeft(milliseconds) {
        const seconds = Math.floor(milliseconds / 1000);
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;

        if (minutes > 0) {
            return `${minutes}m ${remainingSeconds}s`;
        }
        return `${remainingSeconds}s`;
    }

    function checkForExpiredHolds() {
        let hasExpired = false;
        const holdTimers = document.querySelectorAll('.hold-timer');

        holdTimers.forEach(timer => {
            const expiresAt = new Date(timer.getAttribute('data-expires'));
            const now = new Date();

            if (expiresAt <= now) {
                hasExpired = true;
            }
        });

        return hasExpired;
    }

    // Auto-refresh for expired holds
    setInterval(function() {
        if (checkForExpiredHolds()) {
            window.location.reload();
        }
    }, 30000);

    // Update Cart UI - ENHANCED VERSION
function updateCartUI(data, row) {
    if (!row) return;

    // If item was removed
    if (data.removed) {
        row.remove();

        // Check if cart is empty
        const remainingRows = document.querySelectorAll('.cart-item-row');
        if (remainingRows.length === 0) {
            // Reload to show empty cart message
            window.location.reload();
        }
    } else {
        // Update quantity display
        const quantityDisplay = row.querySelector('.quantity-display');
        if (quantityDisplay && data.new_quantity !== undefined) {
            quantityDisplay.textContent = data.new_quantity;
        }

        // Update subtotal
        const subtotalElement = row.querySelector('.subtotal');
        if (subtotalElement && data.new_subtotal !== undefined) {
            subtotalElement.textContent = data.new_subtotal + ' MMK';
        }
    }

    // Update cart total everywhere
    if (data.cart_total !== undefined) {
        updateCartTotal(data.cart_total);
    }

    // Update remaining balance
    if (data.remaining_balance !== undefined) {
        updateRemainingBalance(data.remaining_balance);
    }

    // Update cart count badge
    if (data.cart_count !== undefined) {
        updateCartBadge(data.cart_count);
    }

    // Show success message
    if (data.message) {
        showToast(data.message, 'success');
    }
}

// ADD THESE NEW FUNCTIONS
function updateCartTotal(cartTotal) {
    // Update all cart total elements
    const cartTotalElements = document.querySelectorAll('.cart-total');
    cartTotalElements.forEach(el => {
        el.textContent = cartTotal + ' MMK';
    });

    // Update purchase button text
    const purchaseBtn = document.getElementById('purchaseBtn');
    if (purchaseBtn) {
        purchaseBtn.innerHTML = `<i class="fa-solid fa-lock"></i> Purchase (${cartTotal} MMK)`;
    }

    // Update wallet display cart total if exists
    const walletCartTotal = document.querySelector('.wallet-cart-total');
    if (walletCartTotal) {
        walletCartTotal.textContent = cartTotal + ' MMK';
    }
}

function updateRemainingBalance(remainingBalance) {
    const remainingElements = document.querySelectorAll('.remaining-balance');
    remainingElements.forEach(el => {
        el.textContent = remainingBalance + ' MMK';

        // Update color based on balance
        if (remainingBalance >= 0) {
            el.classList.remove('text-danger');
            el.classList.add('text-success');
        } else {
            el.classList.remove('text-success');
            el.classList.add('text-danger');
        }
    });

    // Update purchase button state
    const purchaseBtn = document.getElementById('purchaseBtn');
    if (purchaseBtn) {
        if (remainingBalance < 0) {
            purchaseBtn.disabled = true;
        } else {
            purchaseBtn.disabled = false;
        }
    }
}

    // ============ HELPER FUNCTIONS ============

    function showLoadingOverlay(message) {
        let overlay = document.getElementById('loadingOverlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'loadingOverlay';
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 9999;
            `;
            document.body.appendChild(overlay);
        }

        overlay.innerHTML = `
            <div style="background: white; padding: 30px; border-radius: 10px; text-align: center;">
                <i class="fa-solid fa-spinner fa-spin fa-3x" style="color: #007bff;"></i>
                <p style="margin-top: 15px; font-size: 16px;">${message}</p>
            </div>
        `;
        overlay.style.display = 'flex';
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

    // Add toast animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});

// Load cart count on page load
function loadCartCount() {
    fetch('/cart/count/')
    .then(response => response.json())
    .then(data => {
        const cartBadge = document.getElementById('cartBadge');
        if (cartBadge) {
            cartBadge.textContent = data.cart_count;
            if (data.cart_count > 0) {
                cartBadge.style.display = 'inline-block';
            } else {
                cartBadge.style.display = 'none';
            }
        }
    })
    .catch(error => {
        console.error('Error loading cart count:', error);
    });
}

// Call on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCartCount();
});