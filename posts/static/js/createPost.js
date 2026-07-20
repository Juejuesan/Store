/**
 * Trusty Shop Marketplace - Product Creation Interactive Systems
 * Handles: Facebook-style Multi-Image Previews, File Tracking, & Quantity Stepper
 */
document.addEventListener('DOMContentLoaded', () => {
    // Elements Selector
    const imageInput = document.getElementById('image-input');
    const previewContainer = document.getElementById('preview-container');
    const uploadBox = document.getElementById('upload-box');

    // Django form fields usually fallback to either 'id_quantity' or input[name="quantity"]
    const qtyInput = document.querySelector('input[name="quantity"]') || document.getElementById('id_quantity');
    const minusBtn = document.getElementById('minusBtn');
    const plusBtn = document.getElementById('plusBtn');

    // Array to hold current file objects (Facebook-style data management)
    let selectedFiles = [];

    /* ==========================================================================
       1. FACEBOOK-STYLE IMAGE UPLOADER & PREVIEW
       ========================================================================== */
    if (imageInput && previewContainer) {
        imageInput.addEventListener('change', (e) => {
            const files = Array.from(e.target.files);

            // Check for strict 5 images maximum limit across additions
            if (selectedFiles.length + files.length > 5) {
                alert("You can only upload a maximum of 5 photos.");
                // Reset native value so the user can re-trigger selection if needed
                imageInput.value = "";
                return;
            }

            files.forEach(file => {
                // Ensure only images are processed
                if (!file.type.startsWith('image/')) return;

                selectedFiles.push(file);

                const reader = new FileReader();
                reader.onload = (event) => {
                    const previewWrapper = document.createElement('div');
                    previewWrapper.classList.add('preview-img-box');

                    // Generate UI card elements
                    previewWrapper.innerHTML = `
                        <img src="${event.target.result}" alt="Product Preview Image">
                        <button type="button" class="remove-img-btn" title="Remove image">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    `;

                    // Remove Image Logic
                    previewWrapper.querySelector('.remove-img-btn').addEventListener('click', () => {
                        const index = selectedFiles.indexOf(file);
                        if (index > -1) {
                            selectedFiles.splice(index, 1);
                        }
                        previewWrapper.remove();

                        // Recalculate badge locations & synchronize backend data transfer
                        updateCoverBadge();
                        syncFilesToHiddenInput();
                        toggleUploadBoxState();
                    });

                    previewContainer.appendChild(previewWrapper);
                    updateCoverBadge();
                    toggleUploadBoxState();
                };
                reader.readAsDataURL(file);
            });

            // Sync structural arrays with DOM input elements
            syncFilesToHiddenInput();
        });
    }

    /**
     * Re-allocates the primary "Cover" badge status to the first item in queue
     */
    function updateCoverBadge() {
        const structuralBoxes = previewContainer.querySelectorAll('.preview-img-box');
        structuralBoxes.forEach((box, idx) => {
            // Clear current designations
            box.classList.remove('cover-photo');
            const existingBadge = box.querySelector('.cover-badge');
            if (existingBadge) existingBadge.remove();

            // First card becomes the main cover image
            if (idx === 0) {
                box.classList.add('cover-photo');
                box.insertAdjacentHTML('beforeend', '<span class="cover-badge">Cover</span>');
            }
        });
    }

    /**
     * Synergizes JavaScript file arrays back into standard HTML file components
     * Ensures Django views can capture items sequentially via `request.FILES.getlist('images')`
     */
    function syncFilesToHiddenInput() {
        const dataTransferObj = new DataTransfer();
        selectedFiles.forEach(file => dataTransferObj.items.add(file));
        imageInput.files = dataTransferObj.files;
    }

    /**
     * Visual adjustment hiding the add button if the 5 image ceiling is hit
     */
    function toggleUploadBoxState() {
        if (selectedFiles.length >= 5) {
            uploadBox.style.display = 'none';
        } else {
            uploadBox.style.display = 'flex';
        }
    }

    /* ==========================================================================
       2. QUANTITY STEPPER CONTROLS
       ========================================================================== */
    if (qtyInput && minusBtn && plusBtn) {
        // Enforce basic fallback value if initial injection is missing/blank
        if (!qtyInput.value || isNaN(parseInt(qtyInput.value))) {
            qtyInput.value = 1;
        }

        // Increment Quantity
        plusBtn.addEventListener('click', () => {
            let currentVal = parseInt(qtyInput.value) || 1;
            qtyInput.value = currentVal + 1;
        });

        // Decrement Quantity (Clamped to a floor minimum of 1 item)
        minusBtn.addEventListener('click', () => {
            let currentVal = parseInt(qtyInput.value) || 1;
            if (currentVal > 1) {
                qtyInput.value = currentVal - 1;
            }
        });

        // Sanitize direct field manual entries
        qtyInput.addEventListener('change', () => {
            let enteredVal = parseInt(qtyInput.value);
            if (isNaN(enteredVal) || enteredVal < 1) {
                qtyInput.value = 1;
            }
        });
    }

    /* ==========================================================================
       3. INTERACTIVE MOUSE GLOW BACKGROUND EFFECT
       ========================================================================== */
    const mouseGlow = document.getElementById('mouseGlow');
    if (mouseGlow) {
        document.addEventListener('mousemove', (e) => {
            // Center glow asset to coordinates of current viewport pointer position
            mouseGlow.style.left = `${e.clientX}px`;
            mouseGlow.style.top = `${e.clientY}px`;
        });
    }
});