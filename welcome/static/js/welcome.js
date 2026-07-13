/* =========================================
   TRUSTY SHOP - WELCOME PAGE JAVASCRIPT
========================================= */



/* =========================================
   DARK / LIGHT MODE
========================================= */


const themeButton = document.getElementById("themeToggle");


if(themeButton){

    themeButton.addEventListener(
        "click",
        function(){


            document.body.classList.toggle(
                "dark-mode"
            );


            if(
                document.body.classList.contains(
                    "dark-mode"
                )
            ){

                themeButton.innerHTML = "☀️";

                localStorage.setItem(
                    "theme",
                    "dark"
                );


            }

            else{


                themeButton.innerHTML = "🌙";

                localStorage.setItem(
                    "theme",
                    "light"
                );

            }


        }
    );

}





/* =========================================
   REMEMBER USER THEME
========================================= */


window.addEventListener(
    "load",
    function(){


        let savedTheme =
        localStorage.getItem(
            "theme"
        );


        if(savedTheme === "dark"){


            document.body.classList.add(
                "dark-mode"
            );


            if(themeButton){

                themeButton.innerHTML = "☀️";

            }


        }


    }
);






/* =========================================
   NAVBAR SHADOW WHEN SCROLL
========================================= */


window.addEventListener(
    "scroll",
    function(){


        const navbar =
        document.querySelector(
            ".navbar"
        );


        if(navbar){


            if(window.scrollY > 50){


                navbar.classList.add(
                    "shadow"
                );


            }

            else{


                navbar.classList.remove(
                    "shadow"
                );


            }

        }


    }
);







/* =========================================
   SMOOTH SCROLL FOR LINKS
========================================= */


document.querySelectorAll(
    'a[href^="#"]'
)
.forEach(
    link => {


        link.addEventListener(
            "click",
            function(event){


                let target =
                document.querySelector(
                    this.getAttribute("href")
                );


                if(target){


                    event.preventDefault();


                    target.scrollIntoView({

                        behavior:"smooth"

                    });


                }


            }
        );


    }
);








/* =========================================
   PRODUCT CARD HOVER EFFECT
========================================= */


const productCards =
document.querySelectorAll(
    ".product-card"
);



productCards.forEach(
    card => {


        card.addEventListener(
            "mouseenter",
            function(){


                this.style.cursor =
                "pointer";


            }
        );



        card.addEventListener(
            "mouseleave",
            function(){


                this.style.cursor =
                "default";


            }
        );


    }
);







/* =========================================
   BUTTON CLICK ANIMATION
========================================= */


const buttons =
document.querySelectorAll(
    ".btn"
);



buttons.forEach(
    button => {


        button.addEventListener(
            "click",
            function(){


                this.style.transform =
                "scale(0.95)";



                setTimeout(
                    () => {


                        this.style.transform =
                        "";


                    },
                    150
                );


            }
        );


    }
);







/* =========================================
   ANIMATE STATISTICS NUMBERS
========================================= */


const counters =
document.querySelectorAll(
    ".stats-section h1"
);



counters.forEach(
    counter => {


        let target =
        parseInt(
            counter.innerText
        );


        let count = 0;


        let speed =
        target / 80;



        let updateCounter =
        setInterval(
            function(){


                count += speed;



                if(count >= target){


                    counter.innerText =
                    target + "+";


                    clearInterval(
                        updateCounter
                    );


                }

                else{


                    counter.innerText =
                    Math.floor(count) + "+";


                }


            },
            30
        );


    }
);