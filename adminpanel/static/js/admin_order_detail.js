// =========================================================
// ADMIN ORDER DETAIL JAVASCRIPT
// =========================================================

document.addEventListener('DOMContentLoaded', function() {

    /* =====================================================
       LIGHTBOX FOR IMAGES
    ===================================================== */

    function openLightbox(imageUrl) {
        const existingLightbox = document.querySelector('.admin-lightbox');
        if (existingLightbox) existingLightbox.remove();

        const lightbox = document.createElement('div');
        lightbox.className = 'admin-lightbox';

        const closeBtn = document.createElement('button');
        closeBtn.className = 'admin-lightbox-close';
        closeBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';

        const img = document.createElement('img');
        img.src = imageUrl;
        img.alt = 'Full size image';

        lightbox.appendChild(closeBtn);
        lightbox.appendChild(img);
        document.body.appendChild(lightbox);

        document.body.style.overflow = 'hidden';

        function closeLightbox() {
            lightbox.remove();
            document.body.style.overflow = '';
            document.removeEventListener('keydown', handleEscape);
        }

        closeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            closeLightbox();
        });

        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox) closeLightbox();
        });

        function handleEscape(e) {
            if (e.key === 'Escape') closeLightbox();
        }

        document.addEventListener('keydown', handleEscape);
    }

    /* =====================================================
       AUTO INITIALIZE IMAGES WITH data-lightbox
    ===================================================== */

    document.querySelectorAll('[data-lightbox]').forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
            const imageUrl = this.getAttribute('data-lightbox');
            if (imageUrl) openLightbox(imageUrl);
        });
    });

});