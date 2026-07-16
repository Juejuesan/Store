// =======================================================
// Trusty Shop JavaScript
// =======================================================

// =======================================================
// 3. NAVBAR SCROLL EFFECT
// =======================================================


const navbar = document.querySelector(".cute-navbar");

const searchInput = document.getElementById("searchInput");

window.addEventListener("scroll",()=>{


    if(window.scrollY > 50){


        navbar.classList.add("scrolled");


    }else{


        navbar.classList.remove("scrolled");


    }


});






// =======================================================
// 4. NAVBAR ACTIVE LINK ANIMATION
// =======================================================


const navLinks =
document.querySelectorAll(".nav-link");



navLinks.forEach(link=>{


    link.addEventListener("click",()=>{


        navLinks.forEach(item=>{


            item.classList.remove("active");


        });



        link.classList.add("active");



    });


});






// =======================================================
// 5. TRENDING SEARCH BUTTON
// =======================================================


const suggestionButtons =
document.querySelectorAll(".search-suggestions button");



suggestionButtons.forEach(button=>{


    button.addEventListener("click",()=>{


        searchInput.value =
        button.innerText;



        searchInput.focus();



    });


});




// =======================================================
// 7. SEARCH BUTTON ACTION
// =======================================================


const searchButton =
document.querySelector(".modern-search button");



if(searchButton){


    searchButton.addEventListener("click",()=>{


        let value =
        searchInput.value.trim();



        if(value !== ""){


            alert("Searching for: " + value);



        }else{


            alert("Please enter product name");



        }



    });



}







// =======================================================
// 8. SCROLL TO TOP BUTTON
// =======================================================


const topButton =
document.createElement("button");



topButton.className="top-btn";



topButton.innerHTML =
'<i class="fa-solid fa-arrow-up"></i>';



document.body.appendChild(topButton);





window.addEventListener("scroll",()=>{


    if(window.scrollY > 500){


        topButton.style.display="flex";


    }else{


        topButton.style.display="none";


    }


});





topButton.addEventListener("click",()=>{


    window.scrollTo({

        top:0,

        behavior:"smooth"

    });



});







// =======================================================
// 9. LOGO CLICK ANIMATION
// =======================================================


const logo =
document.querySelector(".logo-circle");



if(logo){


    logo.addEventListener("click",()=>{


        logo.classList.add("logo-click");



        setTimeout(()=>{


            logo.classList.remove("logo-click");


        },500);



    });



}



// =======================================================
// 12. CUSTOM CURSOR ANIMATION
// =======================================================


const cursor =
document.querySelector(".cursor");


const follower =
document.querySelector(".cursor-follower");



if(cursor && follower){



    document.addEventListener("mousemove",e=>{


        cursor.style.left =
        e.clientX + "px";


        cursor.style.top =
        e.clientY + "px";



        setTimeout(()=>{


            follower.style.left =
            e.clientX + "px";



            follower.style.top =
            e.clientY + "px";



        },80);



    });







    const hoverElements =
    document.querySelectorAll(
    "a, button, .modern-product, .category-card, .nav-link"
    );



    hoverElements.forEach(element=>{


        element.addEventListener("mouseenter",()=>{


            follower.style.width="70px";

            follower.style.height="70px";

            follower.style.background=
            "rgba(13,110,253,0.2)";


        });




        element.addEventListener("mouseleave",()=>{


            follower.style.width="40px";

            follower.style.height="40px";

            follower.style.background="transparent";


        });



    });



}

/*Posts section js*/
/*=====================================================
            TRUSTY SHOP MARKETPLACE
======================================================*/

document.addEventListener("DOMContentLoaded", () => {

    /*==========================================
            SAVE POST
    ==========================================*/

    window.savePost = function(button){

        const box = button.nextElementSibling;

        document.querySelectorAll(".save-box").forEach(item=>{

            if(item!==box){
                item.classList.remove("active");
            }

        });

        box.classList.toggle("active");

    }

    document.addEventListener("click",(e)=>{

        if(!e.target.closest(".seller-right")){
            document.querySelectorAll(".save-box")
            .forEach(box=>box.classList.remove("active"));
        }

    });




    /*==========================================
              CARD HOVER FLOAT
    ==========================================*/

    document.querySelectorAll(".seller-card").forEach(card=>{

        card.addEventListener("mousemove",(e)=>{

            const rect=card.getBoundingClientRect();

            const x=e.clientX-rect.left;
            const y=e.clientY-rect.top;

            const rotateY=(x-rect.width/2)/18;
            const rotateX=(rect.height/2-y)/18;

            card.style.transform=
            `perspective(900px)
            rotateX(${rotateX}deg)
            rotateY(${rotateY}deg)
            translateY(-10px)`;

        });

        card.addEventListener("mouseleave",()=>{

            card.style.transform="";

        });

    });




    /*==========================================
            BUTTON RIPPLE
    ==========================================*/

    document.querySelectorAll(".cart-btn,.detail-btn")
    .forEach(button=>{

        button.addEventListener("click",function(e){

            const ripple=document.createElement("span");

            ripple.className="ripple";

            const rect=this.getBoundingClientRect();

            ripple.style.left=e.clientX-rect.left+"px";
            ripple.style.top=e.clientY-rect.top+"px";

            this.appendChild(ripple);

            setTimeout(()=>{

                ripple.remove();

            },700);

        });

    });




    /*==========================================
          ADD TO CART ANIMATION
    ==========================================*/
document.querySelectorAll(".cart-btn")
.forEach(btn=>{

    btn.addEventListener("click",function(){

        // Change button
        const original=this.innerHTML;

        this.innerHTML=
        `<i class="fa-solid fa-check"></i> Added`;

        this.style.background="#43A047";


        // -----------------------------
        // UPDATE CART BADGE
        // -----------------------------

        const cartCount=document.querySelector(".cart-count");
        const cartLink=document.querySelector(".cart-link");

        let count=parseInt(cartCount.textContent);

        count++;

        cartCount.textContent=count;

        cartCount.classList.add("cart-pop");
        cartLink.classList.add("shake");

        setTimeout(()=>{

            cartCount.classList.remove("cart-pop");
            cartLink.classList.remove("shake");

        },500);


        // -----------------------------
        // SHOW TOAST
        // -----------------------------

        const toast=document.getElementById("cartToast");

        toast.classList.add("show");

        setTimeout(()=>{

            toast.classList.remove("show");

        },2200);


        // -----------------------------
        // Restore Button
        // -----------------------------



            setTimeout(()=>{

                this.innerHTML=original;

                this.style.background="";

            },1800);

        });

    });




    /*==========================================
            VIEW DETAIL EFFECT
    ==========================================*/

    document.querySelectorAll(".detail-btn")
    .forEach(btn=>{

        btn.addEventListener("click",function(){

            const card=this.closest(".seller-card");

            card.animate([

                {transform:"scale(1)"},
                {transform:"scale(.97)"},
                {transform:"scale(1)"}

            ],{

                duration:350

            });

        });

    });




    /*==========================================
            SCROLL REVEAL
    ==========================================*/

    const observer=new IntersectionObserver(entries=>{

        entries.forEach(entry=>{

            if(entry.isIntersecting){

                entry.target.classList.add("show");

            }

        });

    },{

        threshold:.15

    });

    document.querySelectorAll(".seller-card")
    .forEach(card=>{

        card.classList.add("hidden");

        observer.observe(card);

    });




    /*==========================================
          FLOATING BACKGROUND
    ==========================================*/

    const bg=document.getElementById("marketParticles");

    for(let i=0;i<35;i++){

        const circle=document.createElement("span");

        circle.className="floating-circle";

        circle.style.left=Math.random()*100+"%";

        circle.style.animationDuration=
        8+Math.random()*8+"s";

        circle.style.animationDelay=
        Math.random()*5+"s";

        circle.style.width=
        8+Math.random()*20+"px";

        circle.style.height=
        circle.style.width;

        bg.appendChild(circle);

    }




    /*==========================================
            MOUSE GLOW
    ==========================================*/

    const glow=document.getElementById("mouseGlow");

    document.addEventListener("mousemove",(e)=>{

        glow.style.left=e.clientX+"px";

        glow.style.top=e.clientY+"px";

    });




    /*==========================================
            FLOATING CARDS
    ==========================================*/

    document.querySelectorAll(".seller-card")
    .forEach((card,index)=>{

        setInterval(()=>{

            card.animate([

                {transform:"translateY(0px)"},
                {transform:"translateY(-6px)"},
                {transform:"translateY(0px)"}

            ],{

                duration:4000+index*400,

                iterations:1

            });

        },4500+index*600);

    });

});
/*End*/