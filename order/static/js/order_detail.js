// =========================================================
// ORDER DETAIL JAVASCRIPT
// =========================================================

document.addEventListener('DOMContentLoaded', function () {

    // =====================================================
    // 1. MESSAGE ALERT
    // MODERN • CENTERED • CLICK OK TO CLOSE
    // =====================================================

    const messageOverlay =
        document.getElementById('messageOverlay');

    const messageOkBtn =
        document.getElementById('messageOkBtn');


    // -----------------------------------------------------
    // CLOSE MESSAGE FUNCTION
    // -----------------------------------------------------

    function closeMessageAlert() {

        if (!messageOverlay) {
            return;
        }

        // Prevent multiple clicks
        if (
            messageOverlay.classList.contains(
                'message-closing'
            )
        ) {
            return;
        }

        // Start closing animation
        messageOverlay.classList.add(
            'message-closing'
        );

        // Remove after animation
        setTimeout(function () {

            if (
                messageOverlay &&
                document.body.contains(
                    messageOverlay
                )
            ) {
                messageOverlay.remove();
            }

        }, 350);
    }


    // -----------------------------------------------------
    // SHOW MESSAGE
    // -----------------------------------------------------

    if (messageOverlay) {

        messageOverlay.style.display = 'flex';
        messageOverlay.style.opacity = '1';


        // -------------------------------------------------
        // OK BUTTON
        // -------------------------------------------------

        if (messageOkBtn) {

            messageOkBtn.addEventListener(
                'click',
                function () {

                    closeMessageAlert();

                }
            );

        }


        // -------------------------------------------------
        // CLICK OUTSIDE BOX TO CLOSE
        // -------------------------------------------------

        messageOverlay.addEventListener(
            'click',
            function (event) {

                if (
                    event.target ===
                    messageOverlay
                ) {

                    closeMessageAlert();

                }

            }
        );


        // -------------------------------------------------
        // ESC KEY TO CLOSE
        // -------------------------------------------------

        document.addEventListener(
            'keydown',
            function (event) {

                if (
                    event.key === 'Escape'
                ) {

                    closeMessageAlert();

                }

            }
        );

    }


    // =====================================================
    // 2. COUNTDOWN TIMER FOR CANCELLATION
    // =====================================================

    const countdownElement =
        document.querySelector(
            '.countdown-timer'
        );


    if (countdownElement) {

        const deadline =
            new Date(
                countdownElement.getAttribute(
                    'data-cancel-deadline'
                )
            );


        const countdownText =
            countdownElement.querySelector(
                '.countdown-text'
            );


        const cancelForm =
            document.getElementById(
                'cancelOrderForm'
            );


        const cancelBtn =
            document.getElementById(
                'cancelOrderBtn'
            );


        const warningBox =
            document.querySelector(
                '.cancellation-warning'
            );


        // -------------------------------------------------
        // UPDATE COUNTDOWN
        // -------------------------------------------------

        function updateCountdown() {

            const now =
                new Date();


            const timeLeft =
                deadline - now;


            // ---------------------------------------------
            // COUNTDOWN FINISHED
            // ---------------------------------------------

            if (timeLeft <= 0) {

                if (countdownText) {

                    countdownText.textContent =
                        'Cancellation window expired';

                }


                countdownElement.classList.add(
                    'expired'
                );


                // Hide cancel form

                if (cancelForm) {

                    cancelForm.style.display =
                        'none';

                }


                // Disable cancel button

                if (cancelBtn) {

                    cancelBtn.disabled = true;

                }


                // Replace warning box

                if (warningBox) {

                    warningBox.innerHTML = `

                        <div class="cancellation-expired">

                            <i class="fa-solid fa-lock"></i>

                            <div>

                                <strong>
                                    Cancellation Window Expired
                                </strong>

                                <p>
                                    You can no longer cancel this order.
                                    Our team will process your order soon.
                                </p>

                            </div>

                        </div>

                    `;

                }


                return;

            }


            // ---------------------------------------------
            // CALCULATE TIME
            // ---------------------------------------------

            const hours =
                Math.floor(
                    timeLeft /
                    3600000
                );


            const minutes =
                Math.floor(
                    (
                        timeLeft %
                        3600000
                    ) /
                    60000
                );


            const seconds =
                Math.floor(
                    (
                        timeLeft %
                        60000
                    ) /
                    1000
                );


            // ---------------------------------------------
            // DISPLAY COUNTDOWN
            // ---------------------------------------------

            if (countdownText) {

                if (hours > 0) {

                    countdownText.textContent =
                        `${hours}h ${minutes}m ${seconds}s remaining`;

                }

                else if (minutes > 0) {

                    countdownText.textContent =
                        `${minutes}m ${seconds}s remaining`;

                }

                else {

                    countdownText.textContent =
                        `${seconds}s remaining`;

                }

            }

        }


        // -------------------------------------------------
        // RUN IMMEDIATELY
        // -------------------------------------------------

        updateCountdown();


        // -------------------------------------------------
        // UPDATE EVERY SECOND
        // -------------------------------------------------

        const countdownInterval =
            setInterval(
                updateCountdown,
                1000
            );


        // -------------------------------------------------
        // STOP INTERVAL WHEN PAGE IS LEFT
        // -------------------------------------------------

        window.addEventListener(
            'beforeunload',
            function () {

                clearInterval(
                    countdownInterval
                );

            }
        );

    }


    // =====================================================
    // 3. CUSTOM CANCEL CONFIRMATION MODAL
    // =====================================================

    const cancelForm =
        document.querySelector(
            '.cancel-form'
        );


    if (cancelForm) {

        cancelForm.addEventListener(
            'submit',
            function (e) {

                // Prevent normal submit first
                e.preventDefault();

                // Show custom confirmation modal
                showCancelConfirmModal(
                    cancelForm
                );

            }
        );

    }


    // =====================================================
    // 4. CUSTOM CONFIRMATION MODAL
    // =====================================================

    function showCancelConfirmModal(form) {

        // Check if modal already exists
        let modal =
            document.getElementById(
                'cancelConfirmModal'
            );


        if (modal) {
            return;
        }


        // -------------------------------------------------
        // CREATE MODAL
        // -------------------------------------------------

        modal =
            document.createElement(
                'div'
            );


        modal.id =
            'cancelConfirmModal';


        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 99999;
        `;


        // -------------------------------------------------
        // MODAL HTML
        // -------------------------------------------------

        modal.innerHTML = `

            <div style="
                background: white;
                border-radius: 12px;
                padding: 25px;
                max-width: 400px;
                width: 90%;
                text-align: center;
            ">

                <i
                    class="fa-solid fa-triangle-exclamation"
                    style="
                        font-size: 40px;
                        color: #f59e0b;
                        margin-bottom: 15px;
                    "
                ></i>


                <h4 style="
                    margin-bottom: 10px;
                    color: #172033;
                ">
                    Cancel Order?
                </h4>


                <p style="
                    color: #64748b;
                    margin-bottom: 20px;
                ">
                    Are you sure you want to cancel this order?
                    This action cannot be undone.
                </p>


                <div style="
                    display: flex;
                    gap: 10px;
                    justify-content: center;
                ">

                    <button
                        type="button"
                        id="cancelConfirmNo"
                        style="
                            padding: 10px 20px;
                            border: 1px solid #cbd5e1;
                            background: white;
                            border-radius: 8px;
                            cursor: pointer;
                            font-weight: 600;
                        "
                    >
                        Keep Order
                    </button>


                    <button
                        type="button"
                        id="cancelConfirmYes"
                        style="
                            padding: 10px 20px;
                            border: none;
                            background: #ef4444;
                            color: white;
                            border-radius: 8px;
                            cursor: pointer;
                            font-weight: 600;
                        "
                    >
                        Yes, Cancel Order
                    </button>

                </div>

            </div>

        `;


        // -------------------------------------------------
        // ADD MODAL TO PAGE
        // -------------------------------------------------

        document.body.appendChild(
            modal
        );


        // -------------------------------------------------
        // KEEP ORDER BUTTON
        // -------------------------------------------------

        const noButton =
            document.getElementById(
                'cancelConfirmNo'
            );


        if (noButton) {

            noButton.addEventListener(
                'click',
                function () {

                    modal.remove();

                }
            );

        }


        // -------------------------------------------------
        // YES, CANCEL ORDER BUTTON
        // -------------------------------------------------

        const yesButton =
            document.getElementById(
                'cancelConfirmYes'
            );


        if (yesButton) {

            yesButton.addEventListener(
                'click',
                function () {

                    // Remove confirmation modal
                    modal.remove();


                    // Show loading state
                    const submitBtn =
                        form.querySelector(
                            '.btn-cancel'
                        );


                    if (submitBtn) {

                        submitBtn.disabled =
                            true;


                        submitBtn.innerHTML =
                            '<i class="fa-solid fa-spinner fa-spin"></i> Cancelling...';

                    }


                    // Submit the form
                    form.submit();

                }
            );

        }


        // -------------------------------------------------
        // CLICK OUTSIDE MODAL
        // -------------------------------------------------

        modal.addEventListener(
            'click',
            function (event) {

                if (
                    event.target === modal
                ) {

                    modal.remove();

                }

            }
        );

    }

});