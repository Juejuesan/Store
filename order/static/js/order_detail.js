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

    // Cancel form confirmation
    const cancelForm = document.querySelector('.cancel-form');

    if (cancelForm) {
        cancelForm.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to cancel this order?')) {
                e.preventDefault();
                return;
            }

            const submitBtn = cancelForm.querySelector('.btn-cancel');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Cancelling...';
            }
        });
    }

});