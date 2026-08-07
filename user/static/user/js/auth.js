/*=========================================================
        TRUSTYSHOP PREMIUM AUTH JAVASCRIPT
            PART 1 - UNIVERSE ENGINE
=========================================================*/

document.addEventListener("DOMContentLoaded", () => {

    /*====================================================
                    ELEMENTS
    ====================================================*/

    const body = document.body;

    const particles =
        document.getElementById("particles");

    const stars =
        document.getElementById("stars");

    const registerCard =
        document.querySelector(".register-card");



    /*====================================================
                    RANDOM NUMBER
    ====================================================*/

    function random(min, max){

        return Math.random() * (max - min) + min;

    }



    /*====================================================
                FLOATING PARTICLES
    ====================================================*/

    if(particles){

        for(let i = 0; i < 120; i++){

            const particle =
                document.createElement("span");

            const size =
                random(2,6);

            particle.style.width =
                size + "px";

            particle.style.height =
                size + "px";

            particle.style.left =
                random(0,100) + "%";

            particle.style.top =
                random(0,100) + "%";

            particle.style.opacity =
                random(.2,.9);

            particle.style.animationDuration =
                random(8,20) + "s";

            particle.style.animationDelay =
                random(0,8) + "s";

            particles.appendChild(particle);

        }

    }



    /*====================================================
                    TWINKLING STARS
    ====================================================*/

    if(stars){

        setInterval(()=>{

            stars.style.opacity =
                random(.45,.85);

        },900);

    }



    /*====================================================
                    SHOOTING STAR
    ====================================================*/

    function createShootingStar(){

        const star =
            document.createElement("div");

        star.className =
            "shooting-star";

        star.style.top =
            random(0,40) + "%";

        star.style.left =
            "-150px";

        star.style.animationDuration =
            random(2,3.5) + "s";

        body.appendChild(star);

        setTimeout(()=>{

            star.remove();

        },4000);

    }

    setInterval(

        createShootingStar,

        3500

    );



    /*====================================================
                    MOUSE GLOW
    ====================================================*/

    const glow =
        document.createElement("div");

    glow.className =
        "cursor-glow";

    body.appendChild(glow);

    document.addEventListener(

        "mousemove",

        (e)=>{

            glow.style.left =
                e.clientX + "px";

            glow.style.top =
                e.clientY + "px";

        }

    );



    /*====================================================
                CARD PARALLAX EFFECT
    ====================================================*/

    if(registerCard){

        registerCard.addEventListener(

            "mousemove",

            (e)=>{

                const rect =
                    registerCard.getBoundingClientRect();

                const x =
                    e.clientX - rect.left;

                const y =
                    e.clientY - rect.top;

                const rotateY =
                    ((x / rect.width) - .5) * 10;

                const rotateX =
                    ((y / rect.height) - .5) * -10;

                registerCard.style.transform =

                    `
                    perspective(1200px)
                    rotateX(${rotateX}deg)
                    rotateY(${rotateY}deg)
                    scale(1.02)
                    `;

            }

        );

        registerCard.addEventListener(

            "mouseleave",

            ()=>{

                registerCard.style.transform =

                `
                perspective(1200px)
                rotateX(0)
                rotateY(0)
                scale(1)
                `;

            }

        );

    }



    /*====================================================
            FLOATING PLANET MOVEMENT
    ====================================================*/

    const planets =
        document.querySelectorAll(".planet");

    planets.forEach((planet,index)=>{

        let angle = index * 100;

        setInterval(()=>{

            angle += .5;

            planet.style.transform =

                `
                translateY(${Math.sin(angle/20)*12}px)
                translateX(${Math.cos(angle/30)*8}px)
                `;

        },30);

    });



    /*====================================================
                LOGO GLOW PULSE
    ====================================================*/

    const logo =
        document.querySelector(".logo-circle");

    if(logo){

        setInterval(()=>{

            logo.animate(

                [

                    {

                        transform:"scale(1)",

                        boxShadow:

                        "0 0 25px #0ea5ff"

                    },

                    {

                        transform:"scale(1.08)",

                        boxShadow:

                        "0 0 60px #38bdf8"

                    },

                    {

                        transform:"scale(1)",

                        boxShadow:

                        "0 0 25px #0ea5ff"

                    }

                ],

                {

                    duration:2500

                }

            );

        },2600);

    }



    /*====================================================
                CARD FADE IN
    ====================================================*/

    if(registerCard){

        registerCard.animate(

            [

                {

                    opacity:0,

                    transform:

                    "translateY(80px) scale(.9)"

                },

                {

                    opacity:1,

                    transform:

                    "translateY(0) scale(1)"

                }

            ],

            {

                duration:1000,

                easing:"ease"

            }

        );

    }

});

    /*====================================================
                PROFILE IMAGE PREVIEW
    ====================================================*/

    const profileInput =
        document.querySelector("#id_profile_pic");

    const previewImage =
        document.querySelector("#previewImage");

    if(profileInput && previewImage){

        profileInput.addEventListener("change",(e)=>{

            const file = e.target.files[0];

            if(!file) return;

            previewImage.style.opacity = ".3";
            previewImage.style.transform = "scale(.8)";

            const reader = new FileReader();

            reader.onload = function(event){

                previewImage.src = event.target.result;

                setTimeout(()=>{

                    previewImage.style.opacity = "1";
                    previewImage.style.transform = "scale(1)";

                },150);

            };

            reader.readAsDataURL(file);

        });

    }



    /*====================================================
                FLOATING LABELS
    ====================================================*/

    const allInputs =
        document.querySelectorAll(

            ".input-box input, .password-box input, textarea"

        );

    allInputs.forEach(input=>{

        if(input.value !== ""){

            input.parentElement.classList.add("filled");

        }

        input.addEventListener("focus",()=>{

            input.parentElement.classList.add("focused");

        });

        input.addEventListener("blur",()=>{

            input.parentElement.classList.remove("focused");

            if(input.value !== ""){

                input.parentElement.classList.add("filled");

            }else{

                input.parentElement.classList.remove("filled");

            }

        });

    });



    /*====================================================
                PASSWORD SHOW / HIDE
    ====================================================*/

    const toggleButtons =
        document.querySelectorAll(".toggle-password");

    toggleButtons.forEach(button=>{

        button.addEventListener("click",()=>{

            const box =
                button.closest(".password-box");

            const input =
                box.querySelector("input");

            const icon =
                button.querySelector("i");

            if(input.type === "password"){

                input.type = "text";

                icon.classList.remove("fa-eye-slash");
                icon.classList.add("fa-eye");

                button.animate(

                    [

                        {

                            transform:

                            "translateY(-50%) scale(.8)"

                        },

                        {

                            transform:

                            "translateY(-50%) scale(1.2)"

                        },

                        {

                            transform:

                            "translateY(-50%) scale(1)"

                        }

                    ],

                    {

                        duration:300

                    }

                );

            }else{

                input.type = "password";

                icon.classList.remove("fa-eye");
                icon.classList.add("fa-eye-slash");

            }

        });

    });



    /*====================================================
            PASSWORD STRENGTH METER
    ====================================================*/

    const password =
        document.querySelector("#id_password");

    const fill =
        document.querySelector("#strengthFill");

    const text =
        document.querySelector("#strengthText");

    if(password){

        password.addEventListener("input",()=>{

            const value =
                password.value;

            let score = 0;

            if(value.length >= 8) score++;

            if(/[A-Z]/.test(value)) score++;

            if(/[a-z]/.test(value)) score++;

            if(/[0-9]/.test(value)) score++;

            if(/[!@#$%^&*(),.?":{}|<>]/.test(value)) score++;

            const percent =
                score * 20;

            fill.style.width =
                percent + "%";

            switch(score){

                case 0:

                case 1:

                    fill.style.background =
                    "#ef4444";

                    text.innerHTML =
                    "Weak Password";

                    break;

                case 2:

                    fill.style.background =
                    "#f97316";

                    text.innerHTML =
                    "Fair Password";

                    break;

                case 3:

                    fill.style.background =
                    "#facc15";

                    text.innerHTML =
                    "Good Password";

                    break;

                case 4:

                    fill.style.background =
                    "#38bdf8";

                    text.innerHTML =
                    "Strong Password";

                    break;

                case 5:

                    fill.style.background =
                    "#22c55e";

                    text.innerHTML =
                    "Excellent Password 🔥";

                    break;

            }

        });

    }



    /*====================================================
            CONFIRM PASSWORD CHECK
    ====================================================*/

    const confirmPassword =
        document.querySelector("#id_confirm_password");

    if(password && confirmPassword){

        function checkPassword(){

            if(confirmPassword.value === ""){

                confirmPassword.style.borderColor =
                    "";

                return;

            }

            if(password.value === confirmPassword.value){

                confirmPassword.style.borderColor =
                    "#22c55e";

                confirmPassword.style.boxShadow =
                    "0 0 20px rgba(34,197,94,.35)";

            }else{

                confirmPassword.style.borderColor =
                    "#ef4444";

                confirmPassword.style.boxShadow =
                    "0 0 20px rgba(239,68,68,.35)";

            }

        }

        password.addEventListener("input",checkPassword);

        confirmPassword.addEventListener("input",checkPassword);

    }



    /*====================================================
                INPUT HOVER GLOW
    ====================================================*/

    allInputs.forEach(input=>{

        input.addEventListener("mouseenter",()=>{

            input.animate(

                [

                    {

                        transform:"translateY(0)"

                    },

                    {

                        transform:"translateY(-2px)"

                    },

                    {

                        transform:"translateY(0)"

                    }

                ],

                {

                    duration:300

                }

            );

        });

    });



    /*====================================================
                AUTO FOCUS FIRST FIELD
    ====================================================*/

    const firstInput =
        document.querySelector(

            ".input-box input"

        );

    if(firstInput){

        setTimeout(()=>{

            firstInput.focus();

        },700);

    }

        /*====================================================
                BUTTON RIPPLE EFFECT
    ====================================================*/

    const authButtons =
        document.querySelectorAll(".auth-btn");

    authButtons.forEach(button=>{

        button.addEventListener("click",(e)=>{

            const ripple =
                document.createElement("span");

            ripple.className =
                "ripple";

            const rect =
                button.getBoundingClientRect();

            const size =
                Math.max(rect.width, rect.height);

            ripple.style.width =
                size + "px";

            ripple.style.height =
                size + "px";

            ripple.style.left =
                (e.clientX - rect.left - size/2) + "px";

            ripple.style.top =
                (e.clientY - rect.top - size/2) + "px";

            button.appendChild(ripple);

            setTimeout(()=>{

                ripple.remove();

            },700);

        });

    });



    /*====================================================
                REGISTER BUTTON LOADING
    ====================================================*/

    const registerForm =
        document.querySelector("form");

    if(registerForm){

        registerForm.addEventListener("submit",(e)=>{

            const btn =
                registerForm.querySelector(".auth-btn");

            if(!btn) return;

            btn.disabled = true;

            const original =
                btn.innerHTML;

            btn.innerHTML = `

                <i class="fa-solid fa-spinner fa-spin"></i>

                <span>Creating Account...</span>

            `;

            setTimeout(()=>{

                btn.innerHTML =
                    original;

                btn.disabled = false;

            },2500);

        });

    }



    /*====================================================
                STAGGER ANIMATION
    ====================================================*/

    const animatedItems =
        document.querySelectorAll(

            ".profile-upload,\
             .form-row,\
             .input-box,\
             .password-box,\
             .gender-box,\
             .password-strength,\
             .remember-box,\
             .auth-btn,\
             .divider,\
             .social-login,\
             .bottom-text"

        );

    animatedItems.forEach((item,index)=>{

        item.animate(

            [

                {

                    opacity:0,

                    transform:
                    "translateY(40px)"

                },

                {

                    opacity:1,

                    transform:
                    "translateY(0)"

                }

            ],

            {

                duration:700,

                delay:index*80,

                fill:"forwards",

                easing:"ease"

            }

        );

    });



    /*====================================================
                AUTO HIDE ALERTS
    ====================================================*/

    const alerts =
        document.querySelectorAll(".alert");

    alerts.forEach(alert=>{

        setTimeout(()=>{

            alert.style.transition =
                ".5s";

            alert.style.opacity =
                "0";

            alert.style.transform =
                "translateY(-20px)";

            setTimeout(()=>{

                alert.remove();

            },500);

        },4000);

    });



    /*====================================================
                INPUT SHINE EFFECT
    ====================================================*/

    const boxes =
        document.querySelectorAll(

            ".input-box,.password-box"

        );

    boxes.forEach(box=>{

        box.addEventListener("mouseenter",()=>{

            box.classList.add("shine");

        });

        box.addEventListener("mouseleave",()=>{

            box.classList.remove("shine");

        });

    });



    /*====================================================
                TYPING GLOW
    ====================================================*/

    allInputs.forEach(input=>{

        input.addEventListener("input",()=>{

            input.parentElement.animate(

                [

                    {

                        boxShadow:

                        "0 0 0 rgba(0,0,0,0)"

                    },

                    {

                        boxShadow:

                        "0 0 25px rgba(56,189,248,.25)"

                    },

                    {

                        boxShadow:

                        "0 0 0 rgba(0,0,0,0)"

                    }

                ],

                {

                    duration:350

                }

            );

        });

    });



    /*====================================================
                SOCIAL BUTTON EFFECT
    ====================================================*/

    const socials =
        document.querySelectorAll(

            ".social-login button"

        );

    socials.forEach(button=>{

        button.addEventListener("mouseenter",()=>{

            button.animate(

                [

                    {

                        transform:
                        "translateY(0) rotate(0)"

                    },

                    {

                        transform:
                        "translateY(-8px) rotate(12deg)"

                    },

                    {

                        transform:
                        "translateY(-5px) rotate(6deg)"

                    }

                ],

                {

                    duration:350,

                    fill:"forwards"

                }

            );

        });

        button.addEventListener("mouseleave",()=>{

            button.style.transform="";

        });

    });



    /*====================================================
                PARALLAX GLOW
    ====================================================*/

    document.addEventListener("mousemove",(e)=>{

        document.documentElement.style.setProperty(

            "--mouse-x",

            e.clientX + "px"

        );

        document.documentElement.style.setProperty(

            "--mouse-y",

            e.clientY + "px"

        );

    });


