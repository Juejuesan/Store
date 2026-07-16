/*=====================================================
        TRUSTY SHOP VIEW DETAIL
=====================================================*/

document.addEventListener("DOMContentLoaded",()=>{

/*=====================================================
        IMAGE GALLERY
=====================================================*/

const mainImage=document.getElementById("mainImage");

const thumbs=document.querySelectorAll(".thumbs img");

thumbs.forEach(img=>{

img.addEventListener("click",()=>{

mainImage.style.opacity="0";

setTimeout(()=>{

mainImage.src=img.src;

mainImage.style.opacity="1";

},200);

thumbs.forEach(item=>{

item.classList.remove("active");

});

img.classList.add("active");

});

});


/*=====================================================
        WISHLIST
=====================================================*/

const wishlist=document.querySelector(".wishlist-btn");

if(wishlist){

wishlist.addEventListener("click",function(){

this.classList.toggle("active");

if(this.classList.contains("active")){

this.innerHTML=
'<i class="fa-solid fa-heart"></i> Added to Wishlist';

}else{

this.innerHTML=
'<i class="fa-regular fa-heart"></i> Add to Wishlist';

}

});

}


/*=====================================================
        SHARE BUTTON
=====================================================*/

const share=document.querySelector(".share-btn");

if(share){

share.addEventListener("click",()=>{

navigator.clipboard.writeText(window.location.href);

share.innerHTML=
'<i class="fa-solid fa-check"></i> Link Copied';

setTimeout(()=>{

share.innerHTML=
'<i class="fa-solid fa-share-nodes"></i> Share';

},1800);

});

}


/*=====================================================
        BUY NOW
=====================================================*/

const buyBtn=document.querySelector(".buy-btn");

if(buyBtn){

buyBtn.addEventListener("click",function(){

const original=this.innerHTML;

this.innerHTML=
'<i class="fa-solid fa-circle-check"></i> Ordered';

this.style.background="#43A047";

this.disabled=true;

setTimeout(()=>{

this.innerHTML=original;

this.style.background="";

this.disabled=false;

},2200);

});

}


/*=====================================================
        ADD TO CART
=====================================================*/

const cart=document.querySelector(".cart-btn");

if(cart){

cart.addEventListener("click",function(){

const original=this.innerHTML;

this.innerHTML=
'<i class="fa-solid fa-cart-shopping"></i> Added';

this.style.background="#1565C0";

this.style.color="#fff";

setTimeout(()=>{

this.innerHTML=original;

this.style.background="";

this.style.color="";

},1800);

});

}


/*=====================================================
        RIPPLE
=====================================================*/

document.querySelectorAll("button,.view-btn")
.forEach(button=>{

button.addEventListener("click",function(e){

const ripple=document.createElement("span");

ripple.className="ripple";

const rect=this.getBoundingClientRect();

ripple.style.left=
e.clientX-rect.left+"px";

ripple.style.top=
e.clientY-rect.top+"px";

this.appendChild(ripple);

setTimeout(()=>{

ripple.remove();

},700);

});

});


/*=====================================================
        MOUSE GLOW
=====================================================*/

const glow=document.getElementById("mouseGlow");

document.addEventListener("mousemove",e=>{

glow.style.left=e.clientX+"px";

glow.style.top=e.clientY+"px";

});


/*=====================================================
        FLOATING PARTICLES
=====================================================*/

const bg=document.getElementById("particles");

for(let i=0;i<40;i++){

const circle=document.createElement("span");

circle.className="particle";

circle.style.left=Math.random()*100+"%";

circle.style.width=
8+Math.random()*18+"px";

circle.style.height=
circle.style.width;

circle.style.animationDuration=
8+Math.random()*8+"s";

circle.style.animationDelay=
Math.random()*5+"s";

bg.appendChild(circle);

}


/*=====================================================
        SCROLL REVEAL
=====================================================*/

const observer=new IntersectionObserver(entries=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

entry.target.classList.add("show");

}

});

},{
threshold:.15
});

document.querySelectorAll(

".similar-card,.wishlist-box,.product-hero"

).forEach(item=>{

item.classList.add("hidden");

observer.observe(item);

});


});

/*============================================
        LOADER
============================================*/

window.addEventListener("load",()=>{

document.querySelector(".loader-wrapper")
.classList.add("hide");

});


/*============================================
        IMAGE MODAL
============================================*/

const modal=document.getElementById("imageModal");

const modalImg=document.getElementById("modalImage");

const main=document.getElementById("mainImage");

const close=document.querySelector(".close-image");

if(main){

main.addEventListener("click",()=>{

modal.classList.add("show");

modalImg.src=main.src;

});

}

if(close){

close.onclick=()=>{

modal.classList.remove("show");

}

}

window.onclick=e=>{

if(e.target==modal){

modal.classList.remove("show");

}

}


/*============================================
        ORDER TOAST
============================================*/

const toast=document.getElementById("detailToast");

const buy=document.querySelector(".buy-btn");

if(buy){

buy.addEventListener("click",()=>{

toast.classList.add("show");

setTimeout(()=>{

toast.classList.remove("show");

},2200);

});

}