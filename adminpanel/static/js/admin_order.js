// =========================================================
// TRUSTYSHOP ADMIN ORDER JAVASCRIPT
// CLEAN • STABLE • RESPONSIVE
// =========================================================

document.addEventListener("DOMContentLoaded", () => {

    /* ============ COUNTDOWN TIMERS ============ */
    function updateCountdowns() {
        const countdowns = document.querySelectorAll('.countdown-timer');

        countdowns.forEach(timer => {
            const autoReadyAt = timer.getAttribute('data-auto-ready-at');
            const cancelDeadline = timer.getAttribute('data-cancel-deadline');
            const now = new Date();

            let targetTime = null;
            if (autoReadyAt) {
                targetTime = new Date(autoReadyAt);
            } else if (cancelDeadline) {
                targetTime = new Date(cancelDeadline);
            }

            if (!targetTime) return;

            const timeLeft = targetTime - now;
            const countdownText = timer.querySelector('.countdown-text');

            if (timeLeft <= 0) {
                if (countdownText) {
                    countdownText.textContent = 'Ready!';
                }
                timer.classList.add('expired');

                // If auto-ready expired, reload page
                if (autoReadyAt) {
                    const orderId = timer.getAttribute('data-order-id');
                    if (orderId) {
                        updateOrderStatus(orderId);
                    }
                }
            } else {
                const hours = Math.floor(timeLeft / 3600000);
                const minutes = Math.floor((timeLeft % 3600000) / 60000);
                const seconds = Math.floor((timeLeft % 60000) / 1000);

                if (countdownText) {
                    countdownText.textContent = `${hours}h ${minutes}m ${seconds}s`;
                }
            }
        });
    }

    function updateOrderStatus(orderId) {
        fetch(`/admin/orders/${orderId}/auto-ready/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            }
        })
        .catch(error => {
            console.error('Error updating order:', error);
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Update countdowns immediately
    updateCountdowns();

    // Update every second
    setInterval(updateCountdowns, 1000);

    /* ============ FILTER TABS - FIXED ============ */
    // Don't add click handlers to filter tabs
    // Let the links work normally with page reload
    // The active class is already set by Django template

    /* ============ CONFIRM ACTIONS ============ */
    document.querySelectorAll('.confirm-action').forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm-message') || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
                return;
            }

            // Show loading state
            const originalText = this.innerHTML;
            this.disabled = true;
            this.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
        });
    });

    /* ============ TABLE ROW CLICK ============ */
    const tableRows = document.querySelectorAll('.orders-table tbody tr');

    tableRows.forEach(row => {
        const viewButton = row.querySelector('.action-btn.view');
        if (viewButton) {
            row.addEventListener('click', function(e) {
                // Don't trigger if clicking on button itself
                if (e.target.closest('.action-btn')) return;
                window.location.href = viewButton.href;
            });
            row.style.cursor = 'pointer';
        }
    });

    /* ============ TOAST NOTIFICATIONS ============ */
    function showToast(message, type = 'success') {
        let toastContainer = document.getElementById('adminToastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'adminToastContainer';
            toastContainer.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 99999;
            `;
            document.body.appendChild(toastContainer);
        }

        const toast = document.createElement('div');
        toast.style.cssText = `
            padding: 15px 20px;
            margin-bottom: 10px;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            font-size: 14px;
            animation: adminSlideIn 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            gap: 10px;
            ${type === 'success' ? 'background: #10b981;' : 'background: #ef4444;'}
        `;
        toast.innerHTML = `
            <i class="fa-solid ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
            <span>${message}</span>
        `;

        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'adminSlideOut 0.3s ease';
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3000);
    }

    // Add toast animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes adminSlideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes adminSlideOut {
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