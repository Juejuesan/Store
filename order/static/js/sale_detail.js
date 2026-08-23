// =========================================================
// SALE DETAIL JAVASCRIPT
// =========================================================

document.addEventListener('DOMContentLoaded', function() {

    /* =====================================================
       CONFIRM PICKUP FORM VALIDATION
    ===================================================== */

    const confirmForm = document.getElementById('confirmPickupForm');
    const confirmBtn = document.getElementById('confirmBtn');

    if (confirmForm) {
        confirmForm.addEventListener('submit', function(e) {
            const phoneInput = document.getElementById('sellerPhone');
            const locationInput = document.getElementById('sellerLocation');

            // Validate phone
            if (phoneInput) {
                const phone = phoneInput.value.trim();

                if (!phone) {
                    e.preventDefault();
                    alert('Phone number is required.');
                    phoneInput.focus();
                    return;
                }

                if (!/^\d{10,11}$/.test(phone)) {
                    e.preventDefault();
                    alert('Phone number must be 10-11 digits.');
                    phoneInput.focus();
                    return;
                }
            }

            // Validate location
            if (locationInput && !locationInput.value.trim()) {
                e.preventDefault();
                alert('Pickup location is required.');
                locationInput.focus();
                return;
            }

            // Show loading state
            if (confirmBtn) {
                confirmBtn.disabled = true;
                confirmBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Confirming...';
            }
        });
    }

    /* =====================================================
       THUMBNAIL CLICK - OPEN FULL IMAGE
    ===================================================== */

    document.querySelectorAll('.thumb-image').forEach(img => {
        img.addEventListener('click', function() {
            openFullImage(this.src);
        });
    });

    function openFullImage(imageUrl) {
        // Create lightbox
        const lightbox = document.createElement('div');
        lightbox.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 999999;
            cursor: pointer;
        `;

        const img = document.createElement('img');
        img.src = imageUrl;
        img.style.cssText = `
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
            border-radius: 10px;
        `;

        lightbox.appendChild(img);
        document.body.appendChild(lightbox);

        lightbox.addEventListener('click', function() {
            lightbox.remove();
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                lightbox.remove();
            }
        });
    }

});

// Lightbox for item images
document.querySelectorAll('[data-lightbox]').forEach(img => {
    img.addEventListener('click', function() {
        const imageUrl = this.getAttribute('data-lightbox');
        if (!imageUrl) return;

        const lightbox = document.createElement('div');
        lightbox.className = 'admin-lightbox';

        const closeBtn = document.createElement('button');
        closeBtn.className = 'admin-lightbox-close';
        closeBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';

        const fullImg = document.createElement('img');
        fullImg.src = imageUrl;

        lightbox.appendChild(closeBtn);
        lightbox.appendChild(fullImg);
        document.body.appendChild(lightbox);

        document.body.style.overflow = 'hidden';

        function closeLightbox() {
            lightbox.remove();
            document.body.style.overflow = '';
        }

        closeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            closeLightbox();
        });

        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox) closeLightbox();
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') closeLightbox();
        });
    });
});

/* =====================================================
   SCROLL PROGRESS - STARTS BELOW HEADER
===================================================== */

function updateScrollProgress() {
    const progressBar = document.getElementById('progressBar');
    const headerHeight = 70; // Match your navbar height

    if (!progressBar) return;

    // Calculate scrollable area (excluding header)
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrolled = window.scrollY - headerHeight;

    // Calculate percentage
    let percent = 0;
    if (totalHeight > 0) {
        percent = (scrolled / totalHeight) * 100;
        percent = Math.max(0, Math.min(percent, 100));
    }

    progressBar.style.width = percent + '%';
}

window.addEventListener('scroll', updateScrollProgress);
updateScrollProgress();