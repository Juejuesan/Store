/* =======================================================
   TRUSTY SHOP HEADER & FOOTER JAVASCRIPT
======================================================= */


/* =======================================================
   NAVBAR SCROLL EFFECT
======================================================= */


const navbar = document.querySelector(".cute-navbar");


if(navbar){

    window.addEventListener("scroll",()=>{


        if(window.scrollY > 50){

            navbar.classList.add("scrolled");

        }
        else{

            navbar.classList.remove("scrolled");

        }


    });


}




/* =======================================================
   NAVBAR ACTIVE LINK ANIMATION
======================================================= */


const navLinks = document.querySelectorAll(".nav-link");


if(navLinks.length > 0){


    navLinks.forEach(link=>{


        link.addEventListener("click",()=>{


            navLinks.forEach(item=>{

                item.classList.remove("active");

            });


            link.classList.add("active");


        });


    });


}




/* =======================================================
   LOGO CLICK ANIMATION
======================================================= */


const logo = document.querySelector(".logo-circle");


if(logo){


    logo.addEventListener("click",()=>{


        logo.classList.add("logo-click");


        setTimeout(()=>{


            logo.classList.remove("logo-click");


        },500);


    });


}






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



/* ================= END ================= */