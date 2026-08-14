/* =========================================================
   TRUSTY SHOP - PRODUCT IMAGE HOVER SLIDER
   ========================================================= */

function startSlide(slider) {

    const images = slider.querySelectorAll("img");

    // Image တစ်ပုံတည်းဆို slider မလုပ်
    if (images.length <= 1) {
        return;
    }

    // အရင် interval ရှိရင် ဖျက်
    stopSlide(slider, false);

    let currentIndex = 0;

    // Hover ဝင်တဲ့အချိန် Photo 1 ကနေ စ
    slider.scrollLeft = 0;

    slider.slideInterval = setInterval(function () {

        currentIndex++;

        // နောက်ဆုံးပုံရောက်ရင် Photo 1 ပြန်
        if (currentIndex >= images.length) {
            currentIndex = 0;
        }

        slider.scrollTo({
            left: currentIndex * slider.clientWidth,
            behavior: "smooth"
        });

    }, 1000);
}


function stopSlide(slider, reset = true) {

    if (slider.slideInterval) {

        clearInterval(slider.slideInterval);

        slider.slideInterval = null;
    }

    // Mouse ထွက်ရင် Photo 1 ပြန်
    if (reset) {

        slider.scrollTo({
            left: 0,
            behavior: "smooth"
        });
    }
}


/* =========================================================
   SAFETY - PAGE LOAD
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const sliders =
        document.querySelectorAll(".post-image-slider");

    sliders.forEach(function (slider) {

        slider.addEventListener("mouseenter", function () {
            startSlide(slider);
        });

        slider.addEventListener("mouseleave", function () {
            stopSlide(slider);
        });

    });

});