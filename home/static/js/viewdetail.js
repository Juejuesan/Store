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
        s.querySelectorAll('.size-btn').forEach(function(el) { el.classList.remove('active'); });
        t.classList.add('active');

        var price = t.dataset.price;
        var size = t.dataset.size;
        var stock = parseInt(t.dataset.quantity);

        var priceEl = s.querySelector('.item-price');
        var infoEl = s.querySelector('.size-info');
        var qtyInput = s.querySelector('.qty-input');

        if (priceEl) priceEl.textContent = price + ' MMK';
        if (infoEl) infoEl.innerHTML = 'Size: <strong>' + size + '</strong> | Price: <strong>' + price + ' MMK</strong> | Stock: <strong>' + stock + '</strong>';

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

        // Get max stock from input max attribute
        var maxStock = parseInt(inp.max);

        // If max is NaN or 0 or less, don't allow changes
        if (isNaN(maxStock) || maxStock <= 0) {
            inp.value = 1;
            return;
        }

        var v = parseInt(inp.value) + d;
        if (v < 1) v = 1;
        if (v > maxStock) v = maxStock;
        inp.value = v;
    }

    // Add to cart
    if (t.closest('.add-cart-btn')) {
        var s = t.closest('.add-cart-btn').closest('.item-slide');
        var qtyInput = s.querySelector('.qty-input');
        var qty = parseInt(qtyInput.value);
        var name = s.querySelector('.item-title').textContent;
        var sz = s.querySelector('.size-btn.active');

        var maxStock = parseInt(qtyInput.max) || 0;

        // Check if product is in stock
        if (maxStock <= 0) {
            alert('This item is out of stock!');
            return;
        }

        if (sz) {
            var stock = parseInt(sz.dataset.quantity);
            if (qty > stock) {
                alert('Only ' + stock + ' items available in size ' + sz.dataset.size + '!');
                return;
            }
        } else if (qty > maxStock) {
            alert('Only ' + maxStock + ' items available!');
            return;
        }

        // Check if size buttons exist but none selected
        var hasSizeButtons = s.querySelectorAll('.size-btn').length > 0;
        if (hasSizeButtons && !sz) {
            alert('Please select a size first!');
            return;
        }

        var msg = 'Added ' + qty + ' x ' + name;
        if (sz) msg += ' (Size: ' + sz.dataset.size + ')';
        msg += ' to cart!';
        alert(msg);
    }
});

// Check max when typing quantity
document.addEventListener('input', function(e) {
    if (e.target.classList.contains('qty-input')) {
        var maxStock = parseInt(e.target.max);

        // If no valid max, set to 1
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
    // Auto-select first available size for the new slide
    autoSelectFirstSize(document.getElementById('itemSlide' + n));
}

function updateNav() {
    document.getElementById('prevBtn').disabled = currentItemIndex === 0;
    document.getElementById('nextBtn').disabled = currentItemIndex === totalItems - 1;
    document.getElementById('itemCounter').textContent = 'Item ' + (currentItemIndex + 1) + ' of ' + totalItems;
}

// Auto-select first available size
function autoSelectFirstSize(slide) {
    if (!slide) return;

    // Find all size buttons that are NOT sold out and have quantity > 0
    var availableSizes = slide.querySelectorAll('.size-btn:not(.sold-out)');

    // Filter to only those with actual stock
    var sizesWithStock = Array.from(availableSizes).filter(function(btn) {
        return parseInt(btn.dataset.quantity) > 0;
    });

    if (sizesWithStock.length > 0) {
        // Has sizes - click the first available one
        sizesWithStock[0].click();
    } else {
        // No sizes available - set max from data attribute or default
        var qtyInput = slide.querySelector('.qty-input');
        if (qtyInput) {
            var hasSizeButtons = slide.querySelectorAll('.size-btn').length > 0;

            if (hasSizeButtons) {
                // Has size buttons but all sold out
                qtyInput.value = 1;
                qtyInput.max = 0;
                qtyInput.disabled = true;
            } else {
                // No size buttons - use default max from template
                var defaultMax = parseInt(qtyInput.dataset.defaultMax) ||
                               parseInt(slide.dataset.maxQuantity) || 0;
                qtyInput.value = 1;
                qtyInput.max = defaultMax;

                // If out of stock, disable quantity controls
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

// Initialize all slides with first available size selected
function initializeAllSlides() {
    document.querySelectorAll('.item-slide').forEach(function(slide) {
        autoSelectFirstSize(slide);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    updateNav();
    initializeAllSlides(); // Auto-select first available size on all slides
});