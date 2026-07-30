/* =========================================
   TRUSTY SHOP PREMIUM JAVASCRIPT
========================================= */


// =======================================================
// TRUSTY SHOP NAVBAR JAVASCRIPT
// =======================================================


// =======================================================
// 1. NAVBAR SCROLL EFFECT
// =======================================================

const navbar = document.querySelector(".cute-navbar");


if(navbar){

    window.addEventListener("scroll",()=>{


        if(window.scrollY > 50){


            navbar.classList.add("scrolled");


        }else{


            navbar.classList.remove("scrolled");


        }


    });


}





// =======================================================
// 3. LOGO CLICK ANIMATION
// =======================================================


const logo = document.querySelector(".logo-circle");


if(logo){


    logo.addEventListener("click",()=>{


        logo.classList.add("logo-click");



        setTimeout(()=>{


            logo.classList.remove("logo-click");


        },500);



    });


}


/* =========================================
   START AOS SCROLL ANIMATION
========================================= */


AOS.init({

    duration:1000,

    once:true,

    offset:120

});

















/* =========================================
   NUMBER COUNTER ANIMATION
========================================= */


const counters =
document.querySelectorAll(
    ".counter"
);



let started=false;



window.addEventListener(
    "scroll",
    ()=>{


        let section =
        document.querySelector(
            ".stats"
        );



        if(!section) return;



        let position =
        section.getBoundingClientRect()
        .top;



        if(
            position <
            window.innerHeight
            &&
            !started
        ){


            counters.forEach(
                counter=>{


                    let target =
                    Number(
                        counter.innerText
                    );



                    let count=0;



                    let speed =
                    target/100;



                    let timer =
                    setInterval(
                        ()=>{


                            count += speed;



                            if(count>=target){


                                counter.innerText =
                                target+"+";


                                clearInterval(
                                    timer
                                );


                            }

                            else{


                                counter.innerText =
                                Math.floor(count);


                            }



                        },
                        20
                    );


                }
            );



            started=true;


        }



    }
);










/* =========================================
   HERO IMAGE 3D MOVEMENT
========================================= */


const heroImage =
document.querySelector(
".hero-circle"
);



if(heroImage){


document.addEventListener(
"mousemove",
(e)=>{


    let x =
    (window.innerWidth/2-e.clientX)/40;



    let y =
    (window.innerHeight/2-e.clientY)/40;



    heroImage.style.transform =
    `
    rotateY(${x}deg)
    rotateX(${y}deg)
    `;



}
);



}








/* =========================================
   BUTTON RIPPLE EFFECT
========================================= */


const buttons =
document.querySelectorAll(
"button,.primary-btn,.secondary-btn"
);



buttons.forEach(
button=>{


    button.addEventListener(
        "click",
        function(){


            this.style.transform =
            "scale(.92)";



            setTimeout(
                ()=>{


                    this.style.transform="";


                },
                150
            );


        }
    );


});









/* =========================================
   PRODUCT CARD TILT EFFECT
========================================= */


const cards =
document.querySelectorAll(
".product-card,.feature-box"
);



cards.forEach(
card=>{


card.addEventListener(
"mousemove",
(e)=>{


    let rect =
    card.getBoundingClientRect();



    let x =
    e.clientX-rect.left;



    let y =
    e.clientY-rect.top;



    let rotateX =
    (y-rect.height/2)/15;



    let rotateY =
    (rect.width/2-x)/15;



    card.style.transform =
    `
    perspective(1000px)
    rotateX(${rotateX}deg)
    rotateY(${rotateY}deg)
    translateY(-10px)
    `;



});





card.addEventListener(
"mouseleave",
()=>{


    card.style.transform="";


});


});







/* =========================================
   ADD FLOATING PARTICLES/ITEMS
========================================= */

// Define the different types of items
const itemTypes = [
    { type: 'icon', class: 'bi-box-seam' },
    { type: 'icon', class: 'bi-shield-check' },
    { type: 'icon', class: 'bi-cart' },
    { type: 'icon', class: 'bi-currency-dollar' },
    { type: 'icon', class: 'bi-patch-check' },
    { type: 'shape', class: 'circle' },
    { type: 'shape', class: 'square' },
    { type: 'shape', class: 'triangle' }
];

function createFloatingItem() {
    // 1. Create the container element
    const item = document.createElement("span");
    item.className = "floating-item"; // Base class

    // 2. Randomly select an item type
    const selectedItem = itemTypes[Math.floor(Math.random() * itemTypes.length)];

    // 3. Configure the element based on the selected type
    if (selectedItem.type === 'icon') {
        item.classList.add('icon', 'bi', selectedItem.class); // Add icon classes
    } else {
        item.classList.add('shape', selectedItem.class); // Add shape classes
    }

    // 4. Set random position and duration (reusing original logic)
    item.style.left = Math.random() * 100 + "%";
    item.style.animationDuration = (Math.random() * 5 + 5) + "s";

    // 5. Add to the document and schedule removal (reusing original logic)
    document.body.appendChild(item);

    setTimeout(() => {
        item.remove();
    }, 10000);
}

// Start creating items (reusing original interval)
setInterval(createFloatingItem, 500);


/* =======================================================
   TRUSTY SHOP HEADER & FOOTER JAVASCRIPT
======================================================= */




/* =======================================================
   CART BADGE ANIMATION (HEADER)
======================================================= */


const cartBadge = document.querySelector(".cart-count");


const cartLink = document.querySelector(".cart-link");



function updateCart(count){


    if(cartBadge){


        cartBadge.innerText=count;


        cartBadge.classList.add("cart-pop");


    }


    if(cartLink){


        cartLink.classList.add("shake");

    }



    setTimeout(()=>{


        if(cartBadge){

            cartBadge.classList.remove("cart-pop");

        }


        if(cartLink){

            cartLink.classList.remove("shake");

        }


    },500);



}




/* =======================================================
   SCROLL TO TOP BUTTON
======================================================= */


const topButton = document.createElement("button");


topButton.className="top-btn";


topButton.innerHTML=
`
<i class="fa-solid fa-arrow-up"></i>
`;



document.body.appendChild(topButton);




window.addEventListener("scroll",()=>{


    if(window.scrollY > 500){


        topButton.style.display="flex";


    }
    else{


        topButton.style.display="none";


    }


});




topButton.addEventListener("click",()=>{


    window.scrollTo({

        top:0,

        behavior:"smooth"

    });


});







/* =======================================================
   FOOTER CURRENT YEAR
======================================================= */


const year = document.querySelector("#currentYear");


if(year){


    year.innerHTML = new Date().getFullYear();


}




/* =======================================================
   FOOTER LINK SMOOTH SCROLL
======================================================= */


const footerLinks =
document.querySelectorAll("footer a[href^='#']");



footerLinks.forEach(link=>{


    link.addEventListener("click",function(e){


        const target =
        document.querySelector(this.getAttribute("href"));



        if(target){


            e.preventDefault();


            target.scrollIntoView({

                behavior:"smooth"

            });


        }


    });


});





/* =======================================================
   FOOTER SOCIAL ICON HOVER
======================================================= */


const socialIcons =
document.querySelectorAll(".social-icons a");



socialIcons.forEach(icon=>{


    icon.addEventListener("mouseenter",()=>{


        icon.style.transform="translateY(-5px)";


    });



    icon.addEventListener("mouseleave",()=>{


        icon.style.transform="translateY(0)";


    });



});
window.addEventListener("pageshow", function (event) {

    if (event.persisted) {

        // Remove focus from the active element
        if (document.activeElement) {
            document.activeElement.blur();
        }

        // Remove Bootstrap/browser focus
        document.querySelectorAll(".nav-link").forEach(link => {
            link.blur();
        });

    }

});

/* ================= END ================= */
