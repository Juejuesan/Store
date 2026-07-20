document.addEventListener("DOMContentLoaded",()=>{

    const image=document.querySelector(".main-image");

    if(image){

        image.addEventListener("mousemove",(e)=>{

            image.style.transform="scale(1.04)";

        });

        image.addEventListener("mouseleave",()=>{

            image.style.transform="scale(1)";

        });

    }

    document.querySelectorAll(".approve-btn,.reject-btn").forEach(btn=>{

        btn.addEventListener("mouseenter",()=>{

            btn.style.transform="translateY(-5px)";

        });

        btn.addEventListener("mouseleave",()=>{

            btn.style.transform="translateY(0px)";

        });

    });

});