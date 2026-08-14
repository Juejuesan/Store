/* =========================================================
   TRUSTYSHOP
   TERMS & POLICY JAVASCRIPT
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       ELEMENTS
    ===================================================== */

    const sections = document.querySelectorAll(
        ".policy-section"
    );

    const nextButton = document.getElementById(
        "policyNext"
    );

    const backButton = document.getElementById(
        "policyBack"
    );

    const agreeButton = document.getElementById(
        "policyAgree"
    );

    const currentStepElement = document.getElementById(
        "currentPolicyStep"
    );

    const totalStepElement = document.getElementById(
        "totalPolicySteps"
    );

    const progressBar = document.getElementById(
        "policyProgressBar"
    );

    const progressSteps = document.querySelectorAll(
        ".policy-progress-step"
    );

    const policyContainer = document.querySelector(
        ".policy-container"
    );


    /* =====================================================
       SAFETY CHECK
    ===================================================== */

    if (!sections.length) {
        return;
    }


    /* =====================================================
       VARIABLES
    ===================================================== */

    let currentStep = 0;

    const totalSteps = sections.length;


    /* =====================================================
       TOTAL STEP
    ===================================================== */

    if (totalStepElement) {

        totalStepElement.textContent = totalSteps;

    }


    /* =====================================================
       SHOW SECTION
    ===================================================== */

    function showSection(index) {

        /* ---------------------------------------------
           LIMIT INDEX
        --------------------------------------------- */

        if (index < 0) {
            index = 0;
        }

        if (index >= totalSteps) {
            index = totalSteps - 1;
        }


        currentStep = index;


        /* ---------------------------------------------
           UPDATE SECTIONS
        --------------------------------------------- */

        sections.forEach(function (section, i) {

            section.classList.remove(
                "active"
            );

            if (i === currentStep) {

                section.classList.add(
                    "active"
                );

            }

        });


        /* ---------------------------------------------
           UPDATE STEP NUMBER
        --------------------------------------------- */

        if (currentStepElement) {

            currentStepElement.textContent =
                currentStep + 1;

        }


        /* ---------------------------------------------
           UPDATE PROGRESS BAR
        --------------------------------------------- */

        const progress =
            ((currentStep + 1) / totalSteps) * 100;


        if (progressBar) {

            progressBar.style.width =
                progress + "%";

        }


        /* ---------------------------------------------
           UPDATE PROGRESS STEPS
        --------------------------------------------- */

        progressSteps.forEach(function (step, i) {

            step.classList.remove(
                "active",
                "completed"
            );


            if (i === currentStep) {

                step.classList.add(
                    "active"
                );

            }


            if (i < currentStep) {

                step.classList.add(
                    "completed"
                );

            }

        });


        /* ---------------------------------------------
           BACK BUTTON
        --------------------------------------------- */

        if (backButton) {

            if (currentStep === 0) {

                backButton.disabled = true;

            } else {

                backButton.disabled = false;

            }

        }


        /* ---------------------------------------------
           NEXT / AGREE BUTTON
        --------------------------------------------- */

        if (currentStep === totalSteps - 1) {

            if (nextButton) {

                nextButton.style.display =
                    "none";

            }

            if (agreeButton) {

                agreeButton.style.display =
                    "flex";

            }

        } else {

            if (nextButton) {

                nextButton.style.display =
                    "flex";

            }

            if (agreeButton) {

                agreeButton.style.display =
                    "none";

            }

        }


        /* ---------------------------------------------
           SCROLL CONTENT TO TOP
        --------------------------------------------- */

        if (policyContainer) {

            policyContainer.scrollTo({
                top: 0,
                behavior: "smooth"
            });

        }

    }


    /* =====================================================
       NEXT BUTTON
    ===================================================== */

    if (nextButton) {

        nextButton.addEventListener(
            "click",
            function () {

                if (
                    currentStep <
                    totalSteps - 1
                ) {

                    showSection(
                        currentStep + 1
                    );

                }

            }
        );

    }


    /* =====================================================
       BACK BUTTON
    ===================================================== */

    if (backButton) {

        backButton.addEventListener(
            "click",
            function () {

                if (currentStep > 0) {

                    showSection(
                        currentStep - 1
                    );

                }

            }
        );

    }


    /* =====================================================
       AGREE BUTTON
    ===================================================== */

    if (agreeButton) {

        agreeButton.addEventListener(
            "click",
            function () {

                /*
                 * Prevent double click
                 */

                agreeButton.disabled = true;

                agreeButton.classList.add(
                    "loading"
                );


                /*
                 * Change button text
                 */

                const buttonText =
                    agreeButton.querySelector(
                        ".agree-text"
                    );

                if (buttonText) {

                    buttonText.textContent =
                        "Saving...";

                }


                /*
                 * Submit the hidden form
                 */

                const agreementForm =
                    document.getElementById(
                        "termsAgreementForm"
                    );


                if (agreementForm) {

                    agreementForm.submit();

                }

            }
        );

    }


    /* =====================================================
       KEYBOARD SUPPORT
    ===================================================== */

    document.addEventListener(
        "keydown",
        function (event) {

            /*
             * Arrow Right = Next
             */

            if (
                event.key === "ArrowRight" &&
                currentStep < totalSteps - 1
            ) {

                showSection(
                    currentStep + 1
                );

            }


            /*
             * Arrow Left = Back
             */

            if (
                event.key === "ArrowLeft" &&
                currentStep > 0
            ) {

                showSection(
                    currentStep - 1
                );

            }

        }
    );


    /* =====================================================
       INITIALIZE
    ===================================================== */

    showSection(0);

});