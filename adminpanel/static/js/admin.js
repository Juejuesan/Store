/* ==========================================================
        TRUSTY SHOP ADMIN PANEL JAVASCRIPT
========================================================== */


document.addEventListener("DOMContentLoaded", () => {



    /* =====================================
            Loader
    ===================================== */


    const loader = document.getElementById("loader");


    if(loader){

        window.addEventListener("load",()=>{


            setTimeout(()=>{


                loader.style.opacity="0";

                loader.style.visibility="hidden";


            },1200);


        });

    }







    /* =====================================
            Live Clock
    ===================================== */


    const clock = document.getElementById("liveClock");


    function updateClock(){


        if(clock){


            const now = new Date();


            const options={

                hour:"2-digit",

                minute:"2-digit",

                second:"2-digit"

            };


            clock.innerHTML =
            now.toLocaleTimeString([],options);


        }


    }


    updateClock();


    setInterval(updateClock,1000);









    /* =====================================
            Theme Toggle
    ===================================== */


    const themeBtn =
    document.getElementById("themeToggle");



    if(themeBtn){


        themeBtn.addEventListener("click",()=>{


            document.body.classList.toggle("dark");



            if(document.body.classList.contains("dark")){


                themeBtn.innerHTML =
                '<i class="fa-solid fa-sun"></i>';


            }

            else{


                themeBtn.innerHTML =
                '<i class="fa-solid fa-moon"></i>';


            }



        });


    }









    /* =====================================
            Sidebar Toggle
    ===================================== */


    const sidebar =
    document.querySelector(".sidebar");


    const toggleBtn =
    document.getElementById("toggle-btn");



    if(toggleBtn && sidebar){


        toggleBtn.addEventListener("click",()=>{


            sidebar.classList.toggle("active");


        });


    }








/* =====================================
        Notification Panel
===================================== */


const bell =
document.getElementById("notificationBell");


const panel =
document.getElementById("notificationPanel");


const close =
document.getElementById("closeNotification");


if (bell && panel) {

    bell.addEventListener("click", () => {

        panel.classList.add("active");

    });

}


if (close && panel) {

    close.addEventListener("click", () => {

        panel.classList.remove("active");

    });

}
    /* =====================================
            Card Hover Animation
    ===================================== */


    const cards =
    document.querySelectorAll(".card");



    cards.forEach(card=>{


        card.addEventListener("mouseenter",()=>{


            card.style.transform =
            "translateY(-12px) scale(1.02)";


        });



        card.addEventListener("mouseleave",()=>{


            card.style.transform =
            "translateY(0px) scale(1)";


        });


    });









    /* =====================================
            Animated Counter
    ===================================== */


    const counters =
    document.querySelectorAll(".counter");



    counters.forEach(counter=>{


        counter.innerText="0";



        function updateCounter(){


            const target =
            +counter.getAttribute("data-target");



            const current =
            +counter.innerText;



            const increment =
            target / 80;



            if(current < target){


                counter.innerText =
                Math.ceil(current + increment);



                setTimeout(updateCounter,25);


            }


            else{


                counter.innerText = target;


            }


        }



        updateCounter();



    });









    /* =====================================
            Search Filter
    ===================================== */


    const search =
    document.querySelector(".search-box input");



    if(search){


        search.addEventListener("keyup",()=>{


            const value =
            search.value.toLowerCase();



            const rows =
            document.querySelectorAll("tbody tr");



            rows.forEach(row=>{


                row.style.display =

                row.innerText
                .toLowerCase()
                .includes(value)

                ? ""

                : "none";


            });


        });


    }









    /* =====================================
            Sidebar Menu
            Django controls navigation
    ===================================== */


    const menuLinks =
    document.querySelectorAll(".menu a");



    menuLinks.forEach(link=>{


        link.addEventListener("click",(e)=>{


            const url =
            link.getAttribute("href");



            if(url === "#"){


                e.preventDefault();


            }


        });


    });









    /* =====================================
            Floating Background
    ===================================== */


    document.addEventListener("mousemove",(e)=>{


        const circles =
        document.querySelectorAll(".circle");



        circles.forEach((circle,index)=>{


            let speed =
            (index+1)*0.01;



            let x =
            (window.innerWidth-e.pageX)*speed;



            let y =
            (window.innerHeight-e.pageY)*speed;



            circle.style.transform =
            `translate(${x}px,${y}px)`;


        });


    });









    /* =====================================
            Ripple Effect
    ===================================== */


    const buttons =
    document.querySelectorAll(".btn");



    buttons.forEach(btn=>{


        btn.addEventListener("click",function(e){



            let ripple =
            document.createElement("span");



            ripple.classList.add("ripple");



            this.appendChild(ripple);



            let x =
            e.clientX - this.offsetLeft;



            let y =
            e.clientY - this.offsetTop;



            ripple.style.left =
            x+"px";



            ripple.style.top =
            y+"px";



            setTimeout(()=>{


                ripple.remove();


            },600);



        });



    });



});
