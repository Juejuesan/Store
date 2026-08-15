function filterSales(status) {
    // Update active tab
    document.querySelectorAll('.tab-btn').forEach(function(btn) {
        btn.classList.remove('active');
    });
    document.querySelector('.tab-btn[data-status="' + status + '"]').classList.add('active');

    // Filter sale cards
    const cards = document.querySelectorAll('.sale-card');
    cards.forEach(function(card) {
        if (status === 'all' || card.dataset.status === status) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}