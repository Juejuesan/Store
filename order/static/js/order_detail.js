// =========================================================
// ORDER DETAIL JAVASCRIPT
// =========================================================

document.addEventListener('DOMContentLoaded', function() {

    // Countdown timer for cancellation
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
                // Countdown finished
                if (countdownText) {
                    countdownText.textContent = 'Cancellation window expired';
                }
                countdownElement.classList.add('expired');

                // Hide cancel form
                if (cancelForm) {
                    cancelForm.style.display = 'none';
                }

                // Replace warning box with expired message
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

            // Countdown still running
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

        // Run immediately
        updateCountdown();

        // Update every second
        setInterval(updateCountdown, 1000);
    }

    // Cancel form with CUSTOM CONFIRMATION (not blocking)
    const cancelForm = document.querySelector('.cancel-form');

    if (cancelForm) {
        cancelForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Always prevent default first

            // Show custom confirmation modal
            showCancelConfirmModal(cancelForm);
        });
    }

    // Custom confirmation modal
    function showCancelConfirmModal(form) {
        // Create modal if not exists
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

            // Close modal on "No"
            document.getElementById('cancelConfirmNo').addEventListener('click', function() {
                modal.remove();
            });

            // Submit form on "Yes"
            document.getElementById('cancelConfirmYes').addEventListener('click', function() {
                modal.remove();

                // Show loading on submit button
                const submitBtn = form.querySelector('.btn-cancel');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Cancelling...';
                }

                // Submit the form
                form.submit();
            });

            // Close modal if clicking outside
            modal.addEventListener('click', function(event) {
                if (event.target === modal) {
                    modal.remove();
                }
            });
        }
    }

});