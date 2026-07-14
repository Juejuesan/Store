// =======================================================
// Trusty Shop JavaScript
// =======================================================



// =======================================================
// 1. PRODUCT SEARCH FUNCTION
// =======================================================

const searchInput = document.getElementById("searchInput");


if(searchInput){

    searchInput.addEventListener("keyup",function(){

        let keyword = this.value.toLowerCase();


        const products = document.querySelectorAll(".product-card");


        products.forEach(product=>{


            let productText = product.innerText.toLowerCase();


            if(productText.includes(keyword)){


                product.parentElement.style.display="block";


            }else{


                product.parentElement.style.display="none";


            }


        });


    });


}





// =======================================================
// 2. ADD TO CART FUNCTION
// =======================================================


const cartButtons = document.querySelectorAll(".buy-btn");

const cartCount = document.querySelector(".cart-count");


let cartNumber = 3;



cartButtons.forEach(button=>{


    button.addEventListener("click",()=>{


        cartNumber++;


        cartCount.textContent = cartNumber;



        // Cart counter animation

        cartCount.style.transform="scale(1.5)";

        cartCount.style.background="#00C853";



        setTimeout(()=>{


            cartCount.style.transform="scale(1)";

            cartCount.style.background="#ff4081";


        },500);




        // Change button status

        button.innerHTML =
        '<i class="fa-solid fa-check"></i> Added';



        button.style.background="#00C853";




        setTimeout(()=>{


            button.innerHTML =
            '<i class="fa-solid fa-cart-shopping"></i> Add To Cart';



            button.style.background="#1565C0";



        },1500);



        // Cart bounce animation

        cartCount.style.animation="none";


        setTimeout(()=>{


            cartCount.style.animation="bounce 2s infinite";


        },10);



    });



});






// =======================================================
// 3. NAVBAR SCROLL EFFECT
// =======================================================


const navbar = document.querySelector(".cute-navbar");



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
// 6. PRODUCT REVEAL ANIMATION
// =======================================================


const products =
document.querySelectorAll(".product-card");



const productObserver =
new IntersectionObserver((entries)=>{


    entries.forEach((entry,index)=>{


        if(entry.isIntersecting){


            setTimeout(()=>{


                entry.target.style.opacity="1";


                entry.target.style.transform=
                "translateY(0)";



            },index * 150);



            productObserver.unobserve(entry.target);



        }


    });



},{

    threshold:0.2

});





products.forEach(product=>{


    product.style.opacity="0";


    product.style.transform=
    "translateY(50px)";


    product.style.transition=
    "0.7s ease";



    productObserver.observe(product);



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
// 10. PRODUCT IMAGE LOADING EFFECT
// =======================================================


const images =
document.querySelectorAll(".product-image img");



images.forEach(img=>{


    img.addEventListener("load",()=>{


        img.style.opacity="1";


    });


});







// =======================================================
// 11. PRODUCT BACKGROUND FLOATING MOVEMENT
// =======================================================


const productIcons =
document.querySelectorAll(".product-bg-icon");



document.addEventListener("mousemove",(e)=>{


    let x =
    (e.clientX / window.innerWidth - 0.5) * 30;



    let y =
    (e.clientY / window.innerHeight - 0.5) * 30;



    productIcons.forEach(icon=>{


        icon.style.transform =
        `translate(${x}px,${y}px)`;


    });



});







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
    "a, button, .product-card, .nav-link"
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
