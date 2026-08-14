// order.js - Handles order list and detail functionality

document.addEventListener('DOMContentLoaded', function() {

    // ============ ORDER LIST PAGE ============

    // Filter buttons (optional - for AJAX filtering without reload)
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // If you want AJAX filtering, implement here
            // Otherwise, let the link work normally
        });
    });

    // Confirm forms for seller actions
    document.querySelectorAll('.confirm-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const message = form.getAttribute('data-confirm-message') || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
                return;
            }

            // Show loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
            }
        });
    });

    // ============ ORDER DETAIL PAGE ============

    // Countdown timer for cancellation window
    const cancelDeadline = document.querySelector('[data-cancel-deadline]');
    if (cancelDeadline) {
        const deadline = new Date(cancelDeadline.getAttribute('data-cancel-deadline'));

        function updateCountdown() {
            const now = new Date();
            const timeLeft = deadline - now;

            if (timeLeft <= 0) {
                cancelDeadline.textContent = 'Cancellation window has expired';
                cancelDeadline.classList.add('expired');

                // Disable cancel button
                const cancelBtn = document.getElementById('cancelOrderBtn');
                if (cancelBtn) {
                    cancelBtn.disabled = true;
                    cancelBtn.textContent = 'Cancellation Expired';
                }
                return;
            }

            const minutes = Math.floor(timeLeft / 60000);
            const seconds = Math.floor((timeLeft % 60000) / 1000);

            cancelDeadline.textContent = `Time left to cancel: ${minutes}m ${seconds}s`;
        }

        updateCountdown();
        setInterval(updateCountdown, 1000);
    }

    // Cancel order form
    const cancelForm = document.getElementById('cancelOrderForm');
    if (cancelForm) {
        cancelForm.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to cancel this order? This cannot be undone.')) {
                e.preventDefault();
                return;
            }

            const submitBtn = cancelForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Cancelling...';
            }
        });
    }

    // Progress tracker animation
    animateProgressTracker();

    function animateProgressTracker() {
        const steps = document.querySelectorAll('.progress-step.completed');
        const lines = document.querySelectorAll('.progress-line.completed');

        steps.forEach((step, index) => {
            setTimeout(() => {
                step.style.opacity = '1';
                step.style.transform = 'scale(1)';
            }, index * 200);
        });

        lines.forEach((line, index) => {
            setTimeout(() => {
                line.style.width = '100%';
            }, index * 200 + 100);
        });
    }

    // ============ HELPER FUNCTIONS ============

    function showToast(message, type) {
        let toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toastContainer';
            toastContainer.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
            `;
            document.body.appendChild(toastContainer);
        }

        const toast = document.createElement('div');
        toast.style.cssText = `
            padding: 15px 20px;
            margin-bottom: 10px;
            border-radius: 5px;
            color: white;
            font-weight: 500;
            animation: slideIn 0.3s ease;
            ${type === 'success' ? 'background: #28a745;' : 'background: #dc3545;'}
        `;
        toast.textContent = message;

        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3000);
    }

    // Add toast animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});