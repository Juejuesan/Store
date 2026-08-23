/*=====================================================
    TRUSTY SHOP ABOUT PAGE
======================================================*/

document.addEventListener("DOMContentLoaded", function () {

    /*=====================================================
        CURSOR GLOW
    ======================================================*/

    const cursor = document.querySelector(".cursor-glow");

    if(cursor){

        document.addEventListener("mousemove",(e)=>{

            cursor.style.left = e.clientX + "px";
            cursor.style.top = e.clientY + "px";

        });

    }


    /*=====================================================
        NAVBAR SCROLL
    ======================================================*/

    const navbar = document.querySelector(".cute-navbar");

    function navbarScroll(){

        if(window.scrollY>50){

            navbar.classList.add("scrolled");

        }
        else{

            navbar.classList.remove("scrolled");

        }

    }

    navbarScroll();

    window.addEventListener("scroll",navbarScroll);


    /*=====================================================
        SCROLL PROGRESS
    ======================================================*/

    const progressBar=document.getElementById("progressBar");

    function progress(){

        const scrollTop=window.scrollY;

        const height=document.documentElement.scrollHeight-window.innerHeight;

        const percent=(scrollTop/height)*100;

        if(progressBar){

            progressBar.style.width=percent+"%";

        }

    }

    progress();

    window.addEventListener("scroll",progress);



    /*=====================================================
        REVEAL ON SCROLL
    ======================================================*/

    const reveals=document.querySelectorAll(".reveal-on-scroll");

    const revealObserver=new IntersectionObserver((entries)=>{

        entries.forEach(entry=>{

            if(entry.isIntersecting){

                entry.target.classList.add("revealed");

            }

        });

    },{

        threshold:.18

    });

    reveals.forEach(item=>{

        revealObserver.observe(item);

    });



    /*=====================================================
        COUNTER
    ======================================================*/

    const counters=document.querySelectorAll(".counter-number");

    let counted=false;

    function runCounter(){

        if(counted) return;

        const trigger=document.querySelector(".stats-section");

        if(!trigger) return;

        const top=trigger.getBoundingClientRect().top;

        if(top<window.innerHeight-120){

            counted=true;

            counters.forEach(counter=>{

                const target=+counter.dataset.target;

                let count=0;

                const increment=target/120;

                function update(){

                    count+=increment;

                    if(count<target){

                        counter.innerText=Math.floor(count).toLocaleString();

                        requestAnimationFrame(update);

                    }

                    else{

                        counter.innerText=target.toLocaleString();

                    }

                }

                update();

            });

        }

    }

    runCounter();

    window.addEventListener("scroll",runCounter);



    /*=====================================================
        TIMELINE FILL
    ======================================================*/

    const fill=document.getElementById("timelineFill");

    const timeline=document.querySelector(".timeline-wrapper");

    function timelineAnimation(){

        if(!fill || !timeline) return;

        const rect=timeline.getBoundingClientRect();

        const total=timeline.offsetHeight;

        const visible=window.innerHeight-rect.top;

        let percent=(visible/total)*100;

        percent=Math.max(0,Math.min(percent,100));

        fill.style.height=percent+"%";

    }

    timelineAnimation();

    window.addEventListener("scroll",timelineAnimation);



    /*=====================================================
        FAQ
    ======================================================*/

    const faq=document.querySelectorAll(".faq-item");

    faq.forEach(item=>{

        const trigger=item.querySelector(".faq-trigger");

        trigger.addEventListener("click",()=>{

            faq.forEach(i=>{

                if(i!==item){

                    i.classList.remove("active");

                }

            });

            item.classList.toggle("active");

        });

    });



    /*=====================================================
        BACK TO TOP
    ======================================================*/

    const topBtn=document.getElementById("backToTop");

    function topButton(){

        if(!topBtn) return;

        if(window.scrollY>500){

            topBtn.classList.add("btn-visible");

        }

        else{

            topBtn.classList.remove("btn-visible");

        }

    }

    topButton();

    window.addEventListener("scroll",topButton);

    if(topBtn){

        topBtn.addEventListener("click",()=>{

            window.scrollTo({

                top:0,

                behavior:"smooth"

            });

        });

    }



    /*=====================================================
        HERO TYPE EFFECT
    ======================================================*/

    const typing=document.querySelector(".type-effect");

    if(typing){

        const words=[

            "Buyers & Sellers",

            "Safe Transactions",

            "Secure Shopping",

            "Trusted Marketplace"

        ];

        let wordIndex=0;

        let charIndex=0;

        let deleting=false;

        function type(){

            const current=words[wordIndex];

            if(!deleting){

                typing.textContent=current.substring(0,charIndex);

                charIndex++;

                if(charIndex>current.length){

                    deleting=true;

                    setTimeout(type,1800);

                    return;

                }

            }

            else{

                typing.textContent=current.substring(0,charIndex);

                charIndex--;

                if(charIndex===0){

                    deleting=false;

                    wordIndex++;

                    if(wordIndex>=words.length){

                        wordIndex=0;

                    }

                }

            }

            setTimeout(type,deleting?60:120);

        }

        type();

    }



    /*=====================================================
        FLOATING CARDS
    ======================================================*/

    const cards=document.querySelectorAll(".glass-card");

    cards.forEach(card=>{

        card.addEventListener("mousemove",(e)=>{

            const rect=card.getBoundingClientRect();

            const x=e.clientX-rect.left;

            const y=e.clientY-rect.top;

            const rotateY=((x/rect.width)-0.5)*8;

            const rotateX=((rect.height/2-y)/rect.height)*8;

            card.style.transform=

                `perspective(900px)
                 rotateX(${rotateX}deg)
                 rotateY(${rotateY}deg)
                 translateY(-8px)`;

        });

        card.addEventListener("mouseleave",()=>{

            card.style.transform="";

        });

    });



    /*=====================================================
        SMOOTH SCROLL
    ======================================================*/

    document.querySelectorAll('a[href^="#"]').forEach(anchor=>{

        anchor.addEventListener("click",function(e){

            const id=this.getAttribute("href");

            if(id==="#" || id==="") return;

            const target=document.querySelector(id);

            if(target){

                e.preventDefault();

                window.scrollTo({

                    top:target.offsetTop-90,

                    behavior:"smooth"

                });

            }

        });

    });


    /*=====================================================
        CART COUNT - HIDE BADGE WHEN 0
    ======================================================*/

    function loadCartCount() {

        fetch(
            "/cart/count/",
            {
                method: "GET",
                credentials: "same-origin",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            }
        )

        .then(function (response) {

            if (!response.ok) {
                throw new Error("Cart count request failed.");
            }

            return response.json();

        })

        .then(function (data) {

            const cartBadge = document.getElementById("cartBadge");

            if (!cartBadge) {
                return;
            }

            const count = Number(data.cart_count || 0);

            if (count > 0) {
                cartBadge.textContent = count;
                cartBadge.style.display = "inline-block";
            } else {
                cartBadge.textContent = "";
                cartBadge.style.display = "none";
            }

        })

        .catch(function (error) {
            console.error("Cart count error:", error);
        });

    }


    /*=====================================================
        NOTIFICATION COUNT - HIDE BADGE WHEN 0
    ======================================================*/

    function loadNotificationCount() {

        fetch(
            "/notifications/count/",
            {
                method: "GET",
                credentials: "same-origin",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            }
        )

        .then(function (response) {

            if (!response.ok) {
                throw new Error("Notification count request failed.");
            }

            return response.json();

        })

        .then(function (data) {

            const badge = document.getElementById("notificationBadge");

            if (!badge) {
                return;
            }

            const count = Number(data.count || 0);

            if (count > 0) {
                badge.textContent = count;
                badge.style.display = "flex";
            } else {
                badge.textContent = "";
                badge.style.display = "none";
            }

        })

        .catch(function (error) {
            console.error("Notification count error:", error);
        });

    }


    /*=====================================================
        INITIAL LOAD + AUTO REFRESH
    ======================================================*/

    loadCartCount();
    loadNotificationCount();

    window.cartCountInterval = setInterval(loadCartCount, 5000);
    window.notificationCountInterval = setInterval(loadNotificationCount, 5000);

});