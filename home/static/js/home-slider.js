function startSlide(element) {
    const images = element.querySelectorAll('img');
    if (images.length <= 1) return;

    let currentIndex = 0;
    element.slideInterval = setInterval(() => {
        currentIndex = (currentIndex + 1) % images.length;
        element.style.transform = `translateX(-${currentIndex * 100}%)`;
    }, 1000);
}

function stopSlide(element) {
    clearInterval(element.slideInterval);
    element.style.transform = 'translateX(0)';
}