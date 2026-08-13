// viewdetail.js - Complete with AJAX Add to Cart

let currentItemIndex = 0;
const totalItems = document.querySelectorAll('.item-slide').length;

document.addEventListener('click', function(e) {
    var t = e.target;

    // Thumbnail click
    if (t.classList.contains('thumbnail')) {
        var s = t.closest('.item-slide'),
            i = s.querySelector('.main-image');
        i.style.opacity = '0';
        setTimeout(function() { i.src = t.src; i.style.opacity = '1'; }, 150);
        s.querySelectorAll('.thumbnail').forEach(function(el) { el.classList.remove('active'); });
        t.classList.add('active');
    }

    // Size button click
    if (t.classList.contains('size-btn') && !t.classList.contains('sold-out')) {
        var s = t.closest('.item-slide');
        var slideIndex = s.id.replace('itemSlide', '');

        s.querySelectorAll('.size-btn').forEach(function(el) { el.classList.remove('active'); });
        t.classList.add('active');

        var price = t.dataset.price;
        var size = t.dataset.size;
        var stock = parseInt(t.dataset.quantity);
        var variantId = t.dataset.variantId;

        var priceEl = s.querySelector('.item-price');
        var infoEl = s.querySelector('.size-info');
        var qtyInput = s.querySelector('.qty-input');
        var hiddenInput = document.getElementById('sizeVariantId' + slideIndex);

        if (priceEl) priceEl.textContent = price + ' MMK';
        if (infoEl) infoEl.innerHTML = 'Size: <strong>' + size + '</strong> | Price: <strong>' + price + ' MMK</strong> | Stock: <strong>' + stock + '</strong>';

        // Set hidden input value
        if (hiddenInput) hiddenInput.value = variantId;

        // Reset quantity and set max to available stock
        if (qtyInput) {
            qtyInput.value = 1;
            qtyInput.max = stock;
            qtyInput.disabled = false;
        }
    }

    // Navigation
    if (t.closest('#prevBtn')) navigateItem(-1);
    if (t.closest('#nextBtn')) navigateItem(1);

    // Wishlist
    if (t.closest('.wishlist-btn')) {
        var b = t.closest('.wishlist-btn');
        b.classList.toggle('liked');
        var ic = b.querySelector('i'),
            sp = b.querySelector('span');
        if (b.classList.contains('liked')) { ic.className = 'fa-solid fa-heart'; sp.textContent = 'Saved'; }
        else { ic.className = 'fa-regular fa-heart'; sp.textContent = 'Wishlist'; }
    }

    // Quantity buttons
    if (t.classList.contains('qty-btn')) {
        var s = t.closest('.item-slide');
        var inp = s.querySelector('.qty-input');
        var d = t.classList.contains('qty-plus') ? 1 : -1;

        var maxStock = parseInt(inp.max);

        if (isNaN(maxStock) || maxStock <= 0) {
            inp.value = 1;
            return;
        }

        var v = parseInt(inp.value) + d;
        if (v < 1) v = 1;
        if (v > maxStock) v = maxStock;
        inp.value = v;
    }

    // Add to cart - AJAX VERSION
    if (t.closest('.add-cart-btn')) {
        e.preventDefault();

        var btn = t.closest('.add-cart-btn');
        var s = btn.closest('.item-slide');
        var slideIndex = s.id.replace('itemSlide', '');
        var itemId = btn.dataset.itemId;
        var qtyInput = s.querySelector('.qty-input');
        var qty = parseInt(qtyInput.value);
        var name = s.querySelector('.item-title').textContent;

        // Get selected size
        var sz = s.querySelector('.size-btn.active');
        var hiddenInput = document.getElementById('sizeVariantId' + slideIndex);
        var sizeVariantId = hiddenInput ? hiddenInput.value : null;

        var maxStock = parseInt(qtyInput.max) || 0;

        // Check if product is in stock
        if (maxStock <= 0) {
            alert('This item is out of stock!');
            return;
        }

        // Check if size is required but not selected
        var hasSizeButtons = s.querySelectorAll('.size-btn').length > 0;
        if (hasSizeButtons && !sz) {
            alert('Please select a size first!');
            return;
        }

        // Disable button and show loading
        var originalText = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Adding...';

        // Prepare data
        var formData = new FormData();
        formData.append('quantity', qty);
        if (sizeVariantId) {
            formData.append('size_variant_id', sizeVariantId);
        }

        // Get CSRF token
        var csrftoken = getCookie('csrftoken');

        // Send AJAX request
        fetch('/cart/add/' + itemId + '/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            body: formData,
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            if (data.success) {
                alert(data.message);

                // Update cart badge
                if (data.cart_count !== undefined) {
                    updateCartBadge(data.cart_count);
                }

                // Update stock display
                if (sizeVariantId && sz) {
                    var currentQty = parseInt(sz.dataset.quantity);
                    var newQty = currentQty - qty;
                    sz.dataset.quantity = newQty;

                    // Update size info
                    var infoEl = s.querySelector('.size-info');
                    if (infoEl) {
                        if (newQty > 0) {
                            infoEl.innerHTML = 'Size: <strong>' + sz.dataset.size + '</strong> | Price: <strong>' + sz.dataset.price + ' MMK</strong> | Stock: <strong>' + newQty + '</strong>';
                        } else {
                            infoEl.textContent = 'Size ' + sz.dataset.size + ': Out of stock';
                        }
                    }

                    // Disable if out of stock
                    if (newQty <= 0) {
                        sz.disabled = true;
                        sz.classList.add('sold-out');
                        sz.classList.remove('active');
                    }

                    // Reset size selection
                    if (hiddenInput) hiddenInput.value = '';
                    s.querySelectorAll('.size-btn').forEach(function(el) { el.classList.remove('active'); });
                    btn.disabled = true;

                } else {
                    // For non-sized items
                    var stockDisplay = s.querySelector('.stock-display');
                    if (stockDisplay) {
                        var currentStock = parseInt(stockDisplay.dataset.stock);
                        var newStock = currentStock - qty;
                        stockDisplay.dataset.stock = newStock;

                        var stockStrong = stockDisplay.querySelector('strong');
                        if (stockStrong) {
                            if (newStock > 0) {
                                stockStrong.nextSibling.textContent = ' ' + newStock + ' available';
                            } else {
                                stockStrong.nextSibling.textContent = ' Out of stock';
                                btn.disabled = true;
                                btn.innerHTML = '<i class="fa-solid fa-cart-shopping"></i> Out of Stock';
                            }
                        }

                        // Update max quantity
                        if (qtyInput) {
                            qtyInput.max = newStock;
                            qtyInput.dataset.defaultMax = newStock;
                        }
                    }
                }

                // Reset quantity to 1
                if (qtyInput) {
                    qtyInput.value = 1;
                }

            } else {
                alert(data.message);
            }
        })
        .catch(function(error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        })
        .finally(function() {
            // Restore button
            btn.disabled = false;
            btn.innerHTML = originalText;
        });
    }
});

// Check max when typing quantity
document.addEventListener('input', function(e) {
    if (e.target.classList.contains('qty-input')) {
        var maxStock = parseInt(e.target.max);

        if (isNaN(maxStock) || maxStock <= 0) {
            e.target.value = 1;
            return;
        }

        var v = parseInt(e.target.value);
        if (isNaN(v) || v < 1) e.target.value = 1;
        if (v > maxStock) e.target.value = maxStock;
    }
});

function navigateItem(d) {
    var n = currentItemIndex + d;
    if (n < 0 || n >= totalItems) return;
    document.getElementById('itemSlide' + currentItemIndex).style.display = 'none';
    document.getElementById('itemSlide' + n).style.display = 'block';
    currentItemIndex = n;
    updateNav();
    autoSelectFirstSize(document.getElementById('itemSlide' + n));
}

function updateNav() {
    document.getElementById('prevBtn').disabled = currentItemIndex === 0;
    document.getElementById('nextBtn').disabled = currentItemIndex === totalItems - 1;
    document.getElementById('itemCounter').textContent = 'Item ' + (currentItemIndex + 1) + ' of ' + totalItems;
}

function autoSelectFirstSize(slide) {
    if (!slide) return;

    var availableSizes = slide.querySelectorAll('.size-btn:not(.sold-out)');

    var sizesWithStock = Array.from(availableSizes).filter(function(btn) {
        return parseInt(btn.dataset.quantity) > 0;
    });

    if (sizesWithStock.length > 0) {
        sizesWithStock[0].click();
    } else {
        var qtyInput = slide.querySelector('.qty-input');
        if (qtyInput) {
            var hasSizeButtons = slide.querySelectorAll('.size-btn').length > 0;

            if (hasSizeButtons) {
                qtyInput.value = 1;
                qtyInput.max = 0;
                qtyInput.disabled = true;
            } else {
                var defaultMax = parseInt(qtyInput.dataset.defaultMax) ||
                               parseInt(slide.dataset.maxQuantity) || 0;
                qtyInput.value = 1;
                qtyInput.max = defaultMax;

                if (defaultMax <= 0) {
                    qtyInput.value = 1;
                    qtyInput.disabled = true;
                } else {
                    qtyInput.disabled = false;
                }
            }
        }
    }
}

function initializeAllSlides() {
    document.querySelectorAll('.item-slide').forEach(function(slide) {
        autoSelectFirstSize(slide);
    });
}

// Helper functions
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateCartBadge(count) {
    var cartBadge = document.getElementById('cartBadge');
    if (cartBadge) {
        cartBadge.textContent = count;
        if (count > 0) {
            cartBadge.style.display = 'inline-block';
        } else {
            cartBadge.style.display = 'none';
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    updateNav();
    initializeAllSlides();
});

