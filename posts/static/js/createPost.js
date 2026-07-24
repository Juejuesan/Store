/*==================================================
                CREATE POST
==================================================*/

document.addEventListener("DOMContentLoaded", () => {

    initMouseGlow();

    initImagePreview();

    initQuantityButtons();

    initDragDrop();

    initSubmitButton();

});


/*==================================================
                MOUSE GLOW
==================================================*/

function initMouseGlow(){

    const glow = document.getElementById("mouseGlow");

    if(!glow) return;

    document.addEventListener("mousemove",(e)=>{

        glow.style.left = e.clientX + "px";

        glow.style.top = e.clientY + "px";

    });

}


/*==================================================
                IMAGE PREVIEW
==================================================*/

function initImagePreview(){

    const input = document.getElementById("image-input");

    const preview = document.getElementById("preview-container");

    if(!input || !preview) return;

    input.addEventListener("change",()=>{

        preview.innerHTML = "";

        const files = [...input.files];

        files.slice(0,5).forEach((file,index)=>{

    const reader = new FileReader();

    reader.onload = function(e){

        const card = document.createElement("div");

        card.className = "preview-card";

        card.innerHTML = `

            ${
                index === 0
                ?
                `<span class="cover-tag">
                    Cover
                </span>`
                :
                ""
            }

            <img src="${e.target.result}">

            <button
                type="button"
                class="remove-image">

                <i class="fa-solid fa-xmark"></i>

            </button>

        `;

                preview.appendChild(card);

                card.querySelector(".remove-image")
                .addEventListener("click",()=>{

                    card.remove();

                });

            }

            reader.readAsDataURL(file);

        });

    });

}


/*==================================================
                QUANTITY BUTTONS
==================================================*/

function initQuantityButtons(){

    const input = document.querySelector(
        'input[name="quantity"]'
    );

    const plus = document.getElementById("plusBtn");

    const minus = document.getElementById("minusBtn");

    if(!input || !plus || !minus) return;

    plus.addEventListener("click",()=>{

        let value = parseInt(input.value) || 1;

        input.value = value + 1;

    });

    minus.addEventListener("click",()=>{

        let value = parseInt(input.value) || 1;

        if(value > 1){

            input.value = value - 1;

        }

    });

}


/*==================================================
                DRAG & DROP
==================================================*/

function initDragDrop(){

    const uploadBox = document.getElementById("upload-box");

    const input = document.getElementById("image-input");

    if(!uploadBox || !input) return;

    ["dragenter","dragover"].forEach(event=>{

        uploadBox.addEventListener(event,(e)=>{

            e.preventDefault();

            uploadBox.classList.add("dragover");

        });

    });

    ["dragleave","drop"].forEach(event=>{

        uploadBox.addEventListener(event,(e)=>{

            e.preventDefault();

            uploadBox.classList.remove("dragover");

        });

    });

    uploadBox.addEventListener("drop",(e)=>{

        input.files = e.dataTransfer.files;

        input.dispatchEvent(new Event("change"));

    });

}


/*==================================================
                HOVER EFFECT
==================================================*/

const uploadBox = document.getElementById("upload-box");

if(uploadBox){

    uploadBox.addEventListener("mouseenter",()=>{

        uploadBox.style.transform="translateY(-8px)";

    });

    uploadBox.addEventListener("mouseleave",()=>{

        uploadBox.style.transform="translateY(0)";

    });

}

/*==================================================
                SUBMIT LOADING
==================================================*/


/*==================================================
                FORM VALIDATION
==================================================*/

const form = document.getElementById("createPostForm");

if(form){

    form.addEventListener("submit",function(e){

        const price = document.querySelector(
            'input[name="price"]'
        );

        const quantity = document.querySelector(
            'input[name="quantity"]'
        );

        const description = document.querySelector(
            'textarea[name="description"]'
        );

        if(price){

            if(price.value === "" || Number(price.value) <= 0){

                alert("Please enter a valid price.");

                price.focus();

                e.preventDefault();

                return;

            }

        }

        if(quantity){

            if(quantity.value === "" || Number(quantity.value) <= 0){

                alert("Quantity must be at least 1.");

                quantity.focus();

                e.preventDefault();

                return;

            }

        }

        if(description){

            if(description.value.trim().length < 20){

                alert("Description should contain at least 20 characters.");

                description.focus();

                e.preventDefault();

                return;

            }

        }

    });

}


/*==================================================
                AUTO HIDE ALERT
==================================================*/

const alerts = document.querySelectorAll(".custom-alert");

alerts.forEach(alert=>{

    setTimeout(()=>{

        alert.style.transition="all .5s ease";

        alert.style.opacity="0";

        alert.style.transform="translateY(-10px)";

        setTimeout(()=>{

            alert.remove();

        },500);

    },4000);

});


/*==================================================
                CARD ANIMATION
==================================================*/

const cards = document.querySelectorAll(

    ".input-card,.tip,.preview-card"

);

const observer = new IntersectionObserver(entries=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            entry.target.style.opacity="1";

            entry.target.style.transform="translateY(0)";

        }

    });

},{
    threshold:.15
});

cards.forEach(card=>{

    card.style.opacity="0";

    card.style.transform="translateY(35px)";

    card.style.transition="all .6s ease";

    observer.observe(card);

});


/*==================================================
                RIPPLE BUTTON
==================================================*/

const publishBtn = document.querySelector(".publish-btn");

if(publishBtn){

    publishBtn.addEventListener("click",function(e){

        const ripple = document.createElement("span");

        ripple.className = "ripple";

        const rect = this.getBoundingClientRect();

        ripple.style.left =

            (e.clientX - rect.left) + "px";

        ripple.style.top =

            (e.clientY - rect.top) + "px";

        this.appendChild(ripple);

        setTimeout(()=>{

            ripple.remove();

        },600);

    });

}


/*==================================================
                PAGE READY
==================================================*/

console.log(

    "Create Product Page Loaded Successfully."

);