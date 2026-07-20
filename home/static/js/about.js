/**
 * ==========================================================================
 * Trusty Shop - Premium About Page Interactive Engine
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", () => {

    // 1. DYNAMIC CURSOR GLOW EFFECT (DESKTOP ONLY)
    const cursorGlow = document.querySelector(".cursor-glow");
    if (cursorGlow) {
        window.addEventListener("mousemove", (e) => {
            cursorGlow.style.left = `${e.clientX}px`;
            cursorGlow.style.top = `${e.clientY}px`;
        });
    }

    // 2. SCROLL PROGRESS & TIMELINE LINE FILL TRACKER
    const progressBar = document.getElementById("progressBar");
    const timelineFill = document.getElementById("timelineFill");

    window.addEventListener("scroll", () => {
        const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = height > 0 ? (winScroll / height) * 100 : 0;

        // Update top global reading bar
        if (progressBar) progressBar.style.width = `${scrolled}%`;

        // Update vertical timeline progression track
        if (timelineFill) {
            const timelineSection = document.getElementById("how-it-works");
            if (timelineSection) {
                const sectionTop = timelineSection.offsetTop;
                const sectionHeight = timelineSection.offsetHeight;
                const scrollPositionWithinSection = (winScroll + window.innerHeight / 2) - sectionTop;

                let timelineProgress = (scrollPositionWithinSection / sectionHeight) * 100;
                timelineProgress = Math.max(0, Math.min(timelineProgress, 100)); // Clamp between 0-100%
                timelineFill.style.height = `${timelineProgress}%`;
            }
        }
    });

    // 3. REVEAL-ON-SCROLL & ANIMATED COUNTERS ENGINE (INTERSECTION OBSERVER)
    const revealElements = document.querySelectorAll(".reveal-on-scroll");

    const countUp = (counterNode) => {
        const target = parseInt(counterNode.getAttribute("data-target"), 10);
        const duration = 2000; // 2 seconds execution
        const frameRate = 1000 / 60; // 60 FPS
        const totalFrames = Math.round(duration / frameRate);
        let currentFrame = 0;

        const animate = () => {
            currentFrame++;
            const progress = currentFrame / totalFrames;
            // Ease-out quad equation for cleaner scaling transitions
            const easeProgress = progress * (2 - progress);
            const currentValue = Math.round(easeProgress * target);

            counterNode.innerText = currentValue.toLocaleString();

            if (currentFrame < totalFrames) {
                requestAnimationFrame(animate);
            } else {
                counterNode.innerText = target.toLocaleString();
            }
        };
        requestAnimationFrame(animate);
    };

    const intersectionObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add the CSS engine class to transition visibility elements
                entry.target.classList.add("revealed");

                // If the dynamic container item is a timeline node, trigger active state
                if (entry.target.classList.contains("timeline-item")) {
                    entry.target.classList.add("item-active");
                }

                // Fire counting mechanics if nested stat counters are located
                const counters = entry.target.querySelectorAll(".counter-number");
                counters.forEach(counter => {
                    if (!counter.classList.contains("counted")) {
                        counter.classList.add("counted");
                        countUp(counter);
                    }
                });

                // Unobserve clean static elements once fully animated to save process cycles
                if (!entry.target.classList.contains("timeline-item") && counters.length === 0) {
                    observer.unobserve(entry.target);
                }
            }
        });
    }, { threshold: 0.15 });

    revealElements.forEach(el => intersectionObserver.observe(el));

    // 4. PREMIUM USER TESTIMONIAL CAROUSEL SLIDER ENGINE
    const slider = document.getElementById("testimonialSlider");
    const prevBtn = document.getElementById("sliderPrev");
    const nextBtn = document.getElementById("sliderNext");

    if (slider && prevBtn && nextBtn) {
        let currentIndex = 0;

        const getVisibleCards = () => {
            if (window.innerWidth <= 768) return 1;
            if (window.innerWidth <= 992) return 2;
            return 3;
        };

        const updateSliderPosition = () => {
            const cards = slider.querySelectorAll(".testimonial-card");
            const visibleCards = getVisibleCards();
            const totalCards = cards.length;

            // Limit limits boundaries cleanly
            if (currentIndex > totalCards - visibleCards) {
                currentIndex = totalCards - visibleCards;
            }
            if (currentIndex < 0) currentIndex = 0;

            const cardWidth = cards[0].offsetWidth;
            const gap = parseFloat(window.getComputedStyle(slider).gap) || 0;

            // Compute translate vector
            const translateValue = currentIndex * (cardWidth + gap);
            slider.style.transform = `translateX(-${translateValue}px)`;
        };

        nextBtn.addEventListener("click", () => {
            const cards = slider.querySelectorAll(".testimonial-card");
            if (currentIndex < cards.length - getVisibleCards()) {
                currentIndex++;
                updateSliderPosition();
            }
        });

        prevBtn.addEventListener("click", () => {
            if (currentIndex > 0) {
                currentIndex--;
                updateSliderPosition();
            }
        });

        window.addEventListener("resize", updateSliderPosition);
    }

    // 5. PREMIUM FAQ SMOOTH SMOOTH COLLAPSE ACCORDION TRACKER
    const faqItems = document.querySelectorAll(".faq-item");

    faqItems.forEach(item => {
        const trigger = item.querySelector(".faq-trigger");
        const body = item.querySelector(".faq-body");

        // Set initial heights for active elements
        if (item.classList.contains("active") && body) {
            body.style.maxHeight = `${body.scrollHeight}px`;
        }

        trigger.addEventListener("click", () => {
            const isActive = item.classList.contains("active");

            // Close all open panels clean (Accordion Style rule execution)
            faqItems.forEach(innerItem => {
                innerItem.classList.remove("active");
                const innerBody = innerItem.querySelector(".faq-body");
                if (innerBody) innerBody.style.maxHeight = null;
            });

            // Toggle target element state
            if (!isActive) {
                item.classList.add("active");
                body.style.maxHeight = `${body.scrollHeight}px`;
            }
        });
    });

    // 6. FLOATING BACK-TO-TOP CONTROL TOGGLE NODE
    const backToTopBtn = document.getElementById("backToTop");
    if (backToTopBtn) {
        window.addEventListener("scroll", () => {
            if (window.scrollY > 500) {
                backToTopBtn.classList.add("btn-visible");
            } else {
                backToTopBtn.classList.remove("btn-visible");
            }
        });

        backToTopBtn.addEventListener("click", () => {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }
});