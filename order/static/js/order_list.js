// =========================================================
// ORDER LIST JAVASCRIPT
// =========================================================

document.addEventListener('DOMContentLoaded', function() {

    // Add hover animation to order cards
    const orderCards = document.querySelectorAll('.order-card');

    orderCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
            this.style.transform = 'translateY(-2px)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Make entire card clickable (except buttons)
    orderCards.forEach(card => {
        const viewBtn = card.querySelector('.view-btn');

        if (viewBtn) {
            card.addEventListener('click', function(e) {
                // Don't trigger if clicking on the button itself
                if (e.target.closest('.view-btn')) return;

                // Navigate to order detail
                window.location.href = viewBtn.href;
            });

            card.style.cursor = 'pointer';
        }
    });

});