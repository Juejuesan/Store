// =========================================================
// ADMIN POST DETAIL JAVASCRIPT
// MERGED: Original + Thumbnail + Lightbox
// =========================================================

document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       1. MAIN IMAGE HOVER EFFECT (Original)
    ===================================================== */

    const image = document.querySelector(".main-image");

    if (image) {
        image.addEventListener("mousemove", (e) => {
            image.style.transform = "scale(1.04)";
        });

        image.addEventListener("mouseleave", () => {
            image.style.transform = "scale(1)";
        });
    }


    /* =====================================================
       2. APPROVE/REJECT BUTTON HOVER (Original)
    ===================================================== */

    document.querySelectorAll(".approve-btn, .reject-btn").forEach(btn => {
        btn.addEventListener("mouseenter", () => {
            btn.style.transform = "translateY(-5px)";
        });

        btn.addEventListener("mouseleave", () => {
            btn.style.transform = "translateY(0px)";
        });
    });


    /* =====================================================
       3. THUMBNAIL HANDLING (New)
    ===================================================== */

    document.querySelectorAll('.item-detail-card').forEach(function(card) {
        
        const mainImage = card.querySelector('.item-image-box img');
        const thumbnailWrappers = card.querySelectorAll('.thumbnail-wrapper');
        
        if (!mainImage || !thumbnailWrappers.length) return;
        
        thumbnailWrappers.forEach(function(wrapper) {
            wrapper.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const imageUrl = this.getAttribute('data-image-url');
                if (!imageUrl) return;
                
                // Update main image
                mainImage.src = imageUrl;
                mainImage.setAttribute('data-lightbox', imageUrl);
                
                // Update active state
                thumbnailWrappers.forEach(function(w) {
                    w.classList.remove('active');
                });
                this.classList.add('active');
            });
            
            // Double-click thumbnail to open full screen
            wrapper.addEventListener('dblclick', function(e) {
                e.preventDefault();
                const imageUrl = this.getAttribute('data-image-url');
                if (imageUrl && typeof openAdminLightbox === 'function') {
                    openAdminLightbox(imageUrl);
                }
            });
        });
    });


    /* =====================================================
       4. LIGHTBOX - Auto initialize (New)
    ===================================================== */

    document.querySelectorAll('[data-lightbox]').forEach(img => {
        img.style.cursor = 'pointer';
        
        img.addEventListener('click', function() {
            const imageUrl = this.getAttribute('data-lightbox');
            if (imageUrl) {
                openAdminLightbox(imageUrl);
            }
        });
    });

});


/* =========================================================
   LIGHTBOX FUNCTION (Global)
========================================================= */

function openAdminLightbox(imageUrl) {
    // Remove existing lightbox
    const existingLightbox = document.querySelector('.admin-lightbox');
    if (existingLightbox) {
        existingLightbox.remove();
    }
    
    // Create lightbox
    const lightbox = document.createElement('div');
    lightbox.className = 'admin-lightbox';
    lightbox.setAttribute('role', 'dialog');
    lightbox.setAttribute('aria-modal', 'true');
    lightbox.setAttribute('aria-label', 'Full screen image');
    
    // Create close button
    const closeBtn = document.createElement('button');
    closeBtn.className = 'admin-lightbox-close';
    closeBtn.setAttribute('aria-label', 'Close image viewer');
    closeBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';
    
    // Create image
    const img = document.createElement('img');
    img.src = imageUrl;
    img.alt = 'Full size image';
    img.draggable = false;
    
    // Add to lightbox
    lightbox.appendChild(closeBtn);
    lightbox.appendChild(img);
    document.body.appendChild(lightbox);
    
    // Prevent body scroll
    document.body.classList.add('lightbox-active');
    
    let isClosing = false;
    
    function closeLightbox() {
        if (isClosing || !lightbox) return;
        
        isClosing = true;
        
        // Remove event listeners
        document.removeEventListener('keydown', handleEscape);
        
        // Add closing animation
        lightbox.classList.add('closing');
        
        setTimeout(() => {
            if (lightbox && document.body.contains(lightbox)) {
                lightbox.remove();
            }
            document.body.classList.remove('lightbox-active');
        }, 300);
    }
    
    // Close on button click
    closeBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        closeLightbox();
    });
    
    // Close on lightbox click (click outside image)
    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });
    
    // Prevent image click from closing
    img.addEventListener('click', function(e) {
        e.stopPropagation();
    });
    
    // Close on Escape key
    function handleEscape(e) {
        if (e.key === 'Escape') {
            closeLightbox();
        }
    }
    
    document.addEventListener('keydown', handleEscape);
    
    // Focus close button
    setTimeout(() => closeBtn.focus(), 100);
}