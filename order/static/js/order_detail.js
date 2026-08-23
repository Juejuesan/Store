// =========================================================
// ORDER DETAIL JAVASCRIPT
// CLEAN • STABLE • RESPONSIVE
// =========================================================

document.addEventListener('DOMContentLoaded', function() {

    /* =====================================================
       1. COUNTDOWN TIMER FOR CANCELLATION
    ===================================================== */

    const countdownElement = document.querySelector('.countdown-timer');

    if (countdownElement) {
        const deadline = new Date(countdownElement.getAttribute('data-cancel-deadline'));
        const countdownText = countdownElement.querySelector('.countdown-text');
        const cancelForm = document.getElementById('cancelOrderForm');
        const cancelBtn = document.getElementById('cancelOrderBtn');
        const warningBox = document.querySelector('.cancellation-warning');

        function updateCountdown() {
            const now = new Date();
            const timeLeft = deadline - now;

            if (timeLeft <= 0) {
                if (countdownText) {
                    countdownText.textContent = 'Cancellation window expired';
                }
                countdownElement.classList.add('expired');

                if (cancelForm) {
                    cancelForm.style.display = 'none';
                }

                if (warningBox) {
                    warningBox.innerHTML = `
                        <div class="cancellation-expired">
                            <i class="fa-solid fa-lock"></i>
                            <div>
                                <strong>Cancellation Window Expired</strong>
                                <p>You can no longer cancel this order. Our team will process your order soon.</p>
                            </div>
                        </div>
                    `;
                }
                return;
            }

            const hours = Math.floor(timeLeft / 3600000);
            const minutes = Math.floor((timeLeft % 3600000) / 60000);
            const seconds = Math.floor((timeLeft % 60000) / 1000);

            if (countdownText) {
                if (hours > 0) {
                    countdownText.textContent = `${hours}h ${minutes}m ${seconds}s remaining`;
                } else if (minutes > 0) {
                    countdownText.textContent = `${minutes}m ${seconds}s remaining`;
                } else {
                    countdownText.textContent = `${seconds}s remaining`;
                }
            }
        }

        updateCountdown();
        setInterval(updateCountdown, 1000);
    }

    /* =====================================================
       2. CANCEL FORM CONFIRMATION
    ===================================================== */

    const cancelForm = document.querySelector('.cancel-form');

    if (cancelForm) {
        cancelForm.addEventListener('submit', function(e) {
            e.preventDefault();

            showCancelConfirmModal(cancelForm);
        });
    }

    function showCancelConfirmModal(form) {
        let modal = document.getElementById('cancelConfirmModal');

        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'cancelConfirmModal';
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 99999;
            `;

            modal.innerHTML = `
                <div style="background: white; border-radius: 12px; padding: 25px; max-width: 400px; width: 90%; text-align: center;">
                    <i class="fa-solid fa-triangle-exclamation" style="font-size: 40px; color: #f59e0b; margin-bottom: 15px;"></i>
                    <h4 style="margin-bottom: 10px; color: #172033;">Cancel Order?</h4>
                    <p style="color: #64748b; margin-bottom: 20px;">Are you sure you want to cancel this order? This action cannot be undone.</p>
                    <div style="display: flex; gap: 10px; justify-content: center;">
                        <button id="cancelConfirmNo" style="padding: 10px 20px; border: 1px solid #cbd5e1; background: white; border-radius: 8px; cursor: pointer; font-weight: 600;">
                            Keep Order
                        </button>
                        <button id="cancelConfirmYes" style="padding: 10px 20px; border: none; background: #ef4444; color: white; border-radius: 8px; cursor: pointer; font-weight: 600;">
                            Yes, Cancel Order
                        </button>
                    </div>
                </div>
            `;

            document.body.appendChild(modal);

            document.getElementById('cancelConfirmNo').addEventListener('click', function() {
                modal.remove();
            });

            document.getElementById('cancelConfirmYes').addEventListener('click', function() {
                modal.remove();

                const submitBtn = form.querySelector('.btn-cancel');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Cancelling...';
                }

                form.submit();
            });

            modal.addEventListener('click', function(event) {
                if (event.target === modal) {
                    modal.remove();
                }
            });
        }
    }

    /* =====================================================
       3. IMAGE PREVIEW (LIGHTBOX)
    ===================================================== */

    function openLightbox(imageUrl) {
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
        document.body.style.overflow = 'hidden';

        let isClosing = false;

        function closeLightbox() {
            if (isClosing || !lightbox) return;

            isClosing = true;

            document.removeEventListener('keydown', handleEscape);

            lightbox.classList.add('closing');

            setTimeout(() => {
                if (lightbox && document.body.contains(lightbox)) {
                    lightbox.remove();
                }
                document.body.style.overflow = '';
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

    /* =====================================================
       4. AUTO INITIALIZE IMAGES WITH data-lightbox
    ===================================================== */

    document.querySelectorAll('[data-lightbox]').forEach(img => {
        img.style.cursor = 'pointer';

        img.addEventListener('click', function() {
            const imageUrl = this.getAttribute('data-lightbox');
            if (imageUrl) {
                openLightbox(imageUrl);
            }
        });
    });

    /* =====================================================
       5. MESSAGE OVERLAY AUTO CLOSE
    ===================================================== */

    const messageOverlay = document.getElementById('messageOverlay');
    const messageOkBtn = document.getElementById('messageOkBtn');

    if (messageOverlay) {
        // Close on OK button click
        if (messageOkBtn) {
            messageOkBtn.addEventListener('click', function() {
                closeMessageOverlay();
            });
        }

        // Close on overlay click
        messageOverlay.addEventListener('click', function(e) {
            if (e.target === messageOverlay) {
                closeMessageOverlay();
            }
        });

        // Auto close after 3 seconds
        setTimeout(closeMessageOverlay, 3000);

        // Close on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeMessageOverlay();
            }
        });
    }

    function closeMessageOverlay() {
        const overlay = document.getElementById('messageOverlay');
        if (overlay) {
            overlay.style.opacity = '0';
            overlay.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {
                overlay.remove();
            }, 300);
        }
    }

});