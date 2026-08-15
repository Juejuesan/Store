// =========================================================
// ORDER DETAIL JAVASCRIPT
// =========================================================

document.addEventListener('DOMContentLoaded', function() {

    // Countdown timer for cancellation
    const countdownElement = document.querySelector('.countdown-timer');

    if (countdownElement) {
        const deadline = new Date(countdownElement.getAttribute('data-cancel-deadline'));
        const countdownText = countdownElement.querySelector('.countdown-text');

        function updateCountdown() {
            const now = new Date();
            const timeLeft = deadline - now;

            if (timeLeft <= 0) {
                if (countdownText) {
                    countdownText.textContent = 'Cancellation window expired';
                }
                countdownElement.classList.add('expired');

                // Disable cancel button
                const cancelBtn = document.querySelector('.btn-cancel');
                if (cancelBtn) {
                    cancelBtn.disabled = true;
                    cancelBtn.style.opacity = '0.5';
                    cancelBtn.style.cursor = 'not-allowed';
                }
                return;
            }

            const hours = Math.floor(timeLeft / 3600000);
            const minutes = Math.floor((timeLeft % 3600000) / 60000);
            const seconds = Math.floor((timeLeft % 60000) / 1000);

            if (countdownText) {
                countdownText.textContent = `${hours}h ${minutes}m ${seconds}s remaining`;
            }
        }

        updateCountdown();
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