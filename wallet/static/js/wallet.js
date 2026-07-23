/*
=========================================
Trusty Wallet
wallet.js
=========================================
*/

document.addEventListener("DOMContentLoaded", function () {

    animateBalance();

    initializeTiltCards();

    animateOnScroll();

    buttonRippleEffect();

    floatingAnimation();

    counterCards();

});


/*=========================================
BALANCE COUNTER
=========================================*/

function animateBalance() {

    const balance = document.getElementById("balanceCounter");

    if (!balance) return;

    const finalValue = parseFloat(balance.dataset.balance);

    let current = 0;

    const duration = 1800;

    const increment = finalValue / (duration / 20);

    const timer = setInterval(function () {

        current += increment;

        if (current >= finalValue) {

            current = finalValue;

            clearInterval(timer);

        }

        balance.innerText = current.toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });

    }, 20);

}


/*=========================================
CARD HOVER
=========================================*/

function initializeTiltCards() {

    const cards = document.querySelectorAll(

        ".action-card,.overview-card,.tip-card,.wallet-card,.trust-banner"

    );

    cards.forEach(card => {

        card.addEventListener("mousemove", function (e) {

            const rect = card.getBoundingClientRect();

            const x = e.clientX - rect.left;

            const y = e.clientY - rect.top;

            const rotateY = ((x / rect.width) - .5) * 12;

            const rotateX = ((y / rect.height) - .5) * -12;

            card.style.transform =
                `perspective(800px)
                 rotateX(${rotateX}deg)
                 rotateY(${rotateY}deg)
                 translateY(-8px)`;

        });

        card.addEventListener("mouseleave", function () {

            card.style.transform =
                "perspective(800px) rotateX(0) rotateY(0) translateY(0)";

        });

    });

}


/*=========================================
SCROLL ANIMATION
=========================================*/

function animateOnScroll() {

    const items = document.querySelectorAll(

        ".overview-card,.action-card,.tip-card,.activity-item,.trust-banner,.wallet-card"

    );

    const observer = new IntersectionObserver(function (entries) {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("show");

            }

        });

    }, {

        threshold: .15

    });

    items.forEach(item => {

        item.classList.add("hidden");

        observer.observe(item);

    });

}


/*=========================================
BUTTON RIPPLE
=========================================*/

function buttonRippleEffect() {

    const buttons = document.querySelectorAll(

        ".action-card,.deposit-btn,.withdraw-btn"

    );

    buttons.forEach(button => {

        button.addEventListener("click", function (e) {

            const ripple = document.createElement("span");

            ripple.className = "ripple";

            const rect = button.getBoundingClientRect();

            ripple.style.left = (e.clientX - rect.left) + "px";

            ripple.style.top = (e.clientY - rect.top) + "px";

            button.appendChild(ripple);

            setTimeout(function () {

                ripple.remove();

            }, 600);

        });

    });

}


/*=========================================
FLOATING ICONS
=========================================*/

function floatingAnimation() {

    const icons = document.querySelectorAll(

        ".wallet-logo,.trust-badge,.overview-icon"

    );

    icons.forEach((icon, index) => {

        let direction = 1;

        let pos = 0;

        setInterval(function () {

            pos += direction;

            icon.style.transform = `translateY(${pos}px)`;

            if (pos >= 8 || pos <= -8) {

                direction *= -1;

            }

        }, 45 + index * 5);

    });

}


/*=========================================
COUNTER CARDS
=========================================*/

function counterCards() {

    const numbers = document.querySelectorAll(".overview-card h3");

    numbers.forEach(number => {

        const text = number.innerText.replace(/,/g, '');

        const value = parseFloat(text);

        if (isNaN(value)) return;

        let start = 0;

        const speed = value / 80;

        const timer = setInterval(function () {

            start += speed;

            if (start >= value) {

                start = value;

                clearInterval(timer);

            }

            number.innerText = Math.floor(start).toLocaleString();

        }, 20);

    });

}


/*=========================================
SMOOTH SCROLL
=========================================*/

document.querySelectorAll("a[href^='#']").forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        e.preventDefault();

        document.querySelector(this.getAttribute("href"))

            .scrollIntoView({

                behavior: "smooth"

            });

    });

});


/*=========================================
HEADER SHADOW
=========================================*/

window.addEventListener("scroll", function () {

    const navbar = document.querySelector("nav");

    if (!navbar) return;

    if (window.scrollY > 30) {

        navbar.classList.add("nav-shadow");

    } else {

        navbar.classList.remove("nav-shadow");

    }

});