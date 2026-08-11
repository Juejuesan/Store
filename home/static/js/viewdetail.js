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
        var maxStock = parseInt(inp.max) || 99;
        var v = parseInt(inp.value) + d;
        if (v < 1) v = 1;
        if (v > maxStock) v = maxStock;
        inp.value = v;
    }

    // Add to cart
    if (t.closest('.add-cart-btn')) {
        var s = t.closest('.add-cart-btn').closest('.item-slide');
        var qty = s.querySelector('.qty-input').value;
        var name = s.querySelector('.item-title').textContent;
        var sz = s.querySelector('.size-btn.active');

        if (sz) {
            var stock = parseInt(sz.dataset.quantity);
            if (parseInt(qty) > stock) {
                alert('Only ' + stock + ' items available in size ' + sz.dataset.size + '!');
                return;
            }
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
        var maxStock = parseInt(e.target.max) || 99;
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
}

function updateNav() {
    document.getElementById('prevBtn').disabled = currentItemIndex === 0;
    document.getElementById('nextBtn').disabled = currentItemIndex === totalItems - 1;
    document.getElementById('itemCounter').textContent = 'Item ' + (currentItemIndex + 1) + ' of ' + totalItems;
}

document.addEventListener('DOMContentLoaded', function() { updateNav(); });