document.addEventListener("DOMContentLoaded", function () {

    // =========================================================
    // ELEMENTS
    // =========================================================

    const notificationList =
        document.getElementById("notificationList");

    const normalHeader =
        document.getElementById("normalNotificationHeader");

    const selectModeHeader =
        document.getElementById("selectModeHeader");

    const clearAllBtn =
        document.getElementById("clearAllBtn");

    const selectAllBtn =
        document.getElementById("selectAllBtn");

    const deleteSelectedBtn =
        document.getElementById("deleteSelectedBtn");

    const selectedCount =
        document.getElementById("selectedCount");


    // =========================================================
    // STATE
    // =========================================================

    let selectMode = false;

    let longPressTimer = null;

    let longPressTriggered = false;

    const LONG_PRESS_TIME = 600;


    // =========================================================
    // CSRF TOKEN
    // =========================================================

    function getCookie(name) {

        let cookieValue = null;

        if (document.cookie && document.cookie !== "") {

            const cookies =
                document.cookie.split(";");

            for (let cookie of cookies) {

                cookie = cookie.trim();

                if (
                    cookie.substring(
                        0,
                        name.length + 1
                    ) === name + "="
                ) {

                    cookieValue =
                        decodeURIComponent(
                            cookie.substring(
                                name.length + 1
                            )
                        );

                    break;
                }
            }
        }

        return cookieValue;
    }


    const csrftoken =
        getCookie("csrftoken");


    // =========================================================
    // GET ALL NOTIFICATION CARDS
    // =========================================================

    function getCards() {

        return document.querySelectorAll(
            ".notification-card"
        );

    }


    // =========================================================
    // GET SELECTED NOTIFICATION CARDS
    // =========================================================

    function getSelectedCards() {

        return document.querySelectorAll(
            ".notification-card.selected"
        );

    }


    // =========================================================
    // ENTER SELECT MODE
    // =========================================================

    function enterSelectMode(card) {

        // Already in select mode
        if (selectMode) {
            return;
        }

        selectMode = true;


        // Add select mode class
        document.body.classList.add(
            "select-mode"
        );


        // Hide normal header
        if (normalHeader) {

            normalHeader.style.display =
                "none";

        }


        // Show select mode header
        if (selectModeHeader) {

            selectModeHeader.classList.add(
                "active"
            );

        }


        // Automatically select
        // the notification that triggered
        // select mode

        if (card) {

            selectCard(card);

        }


        updateSelectionUI();
    }


    // =========================================================
    // EXIT SELECT MODE
    // =========================================================

    function exitSelectMode() {

        selectMode = false;


        // Remove body select mode
        document.body.classList.remove(
            "select-mode"
        );


        // Show normal header
        if (normalHeader) {

            normalHeader.style.display =
                "flex";

        }


        // Hide select mode header
        if (selectModeHeader) {

            selectModeHeader.classList.remove(
                "active"
            );

        }


        // Clear all selected cards
        getCards().forEach(function (card) {

            card.classList.remove(
                "selected"
            );


            const checkbox =
                card.querySelector(
                    ".notification-checkbox"
                );


            if (checkbox) {

                checkbox.checked = false;

            }

        });


        // Reset UI
        if (selectedCount) {

            selectedCount.textContent =
                "0 selected";

        }


        if (deleteSelectedBtn) {

            deleteSelectedBtn.disabled =
                true;

        }


        if (selectAllBtn) {

            selectAllBtn.textContent =
                "Select All";

        }

    }


    // =========================================================
    // SELECT ONE CARD
    // =========================================================

    function selectCard(card) {

        if (!card) {
            return;
        }


        card.classList.add(
            "selected"
        );


        const checkbox =
            card.querySelector(
                ".notification-checkbox"
            );


        if (checkbox) {

            checkbox.checked = true;

        }

    }


    // =========================================================
    // UNSELECT ONE CARD
    // =========================================================

    function unselectCard(card) {

        if (!card) {
            return;
        }


        card.classList.remove(
            "selected"
        );


        const checkbox =
            card.querySelector(
                ".notification-checkbox"
            );


        if (checkbox) {

            checkbox.checked = false;

        }

    }


    // =========================================================
    // UPDATE SELECTION UI
    // =========================================================

    function updateSelectionUI() {

        const selected =
            getSelectedCards();

        const count =
            selected.length;

        const total =
            getCards().length;


        // =====================================================
        // SELECTED COUNT
        // =====================================================

        if (selectedCount) {

            selectedCount.textContent =
                count + " selected";

        }


        // =====================================================
        // DELETE BUTTON
        // =====================================================

        if (deleteSelectedBtn) {

            deleteSelectedBtn.disabled =
                count === 0;

        }


        // =====================================================
        // SELECT ALL BUTTON
        // =====================================================

        if (selectAllBtn) {

            if (
                total > 0 &&
                count === total
            ) {

                selectAllBtn.textContent =
                    "Unselect All";

            } else {

                selectAllBtn.textContent =
                    "Select All";

            }

        }


        // =====================================================
        // NOTHING SELECTED
        // RETURN TO ORIGINAL UI
        // =====================================================

        if (
            selectMode &&
            count === 0
        ) {

            exitSelectMode();

        }

    }


    // =========================================================
    // START MOBILE LONG PRESS
    // =========================================================

    function startLongPress(card) {

        if (selectMode) {
            return;
        }


        longPressTriggered = false;


        longPressTimer =
            setTimeout(function () {

                longPressTriggered = true;

                enterSelectMode(card);

            }, LONG_PRESS_TIME);

    }


    // =========================================================
    // CANCEL LONG PRESS
    // =========================================================

    function cancelLongPress() {

        if (longPressTimer) {

            clearTimeout(
                longPressTimer
            );

            longPressTimer = null;

        }

    }


    // =========================================================
    // ATTACH CARD EVENTS
    // =========================================================

    function attachCardEvents(card) {


        // =====================================================
        // DESKTOP RIGHT CLICK
        // Windows / MacBook
        // =====================================================

        card.addEventListener(
            "contextmenu",
            function (event) {

                // Stop browser right-click menu
                event.preventDefault();


                // Already select mode
                if (selectMode) {
                    return;
                }


                // Enter select mode
                enterSelectMode(card);

            }
        );


        // =====================================================
        // MOBILE LONG PRESS
        // Android / iPhone
        // =====================================================

        card.addEventListener(
            "touchstart",
            function () {

                if (selectMode) {
                    return;
                }


                startLongPress(card);

            },
            {
                passive: true
            }
        );


        card.addEventListener(
            "touchend",
            function () {

                cancelLongPress();

            }
        );


        card.addEventListener(
            "touchcancel",
            function () {

                cancelLongPress();

            }
        );


        card.addEventListener(
            "touchmove",
            function () {

                cancelLongPress();

            }
        );


        // =====================================================
        // NORMAL LEFT CLICK / TAP
        // =====================================================

        card.addEventListener(
            "click",
            function (event) {


                // =================================================
                // LONG PRESS ALREADY TRIGGERED
                // =================================================

                if (longPressTriggered) {

                    longPressTriggered = false;

                    event.preventDefault();

                    event.stopPropagation();

                    return;

                }


                // =================================================
                // CHECKBOX CLICK
                // =================================================

                if (
                    event.target.classList.contains(
                        "notification-checkbox"
                    )
                ) {

                    return;

                }


                // =================================================
                // SELECT MODE
                // =================================================

                if (selectMode) {


                    // Selected → Unselect
                    if (
                        card.classList.contains(
                            "selected"
                        )
                    ) {

                        unselectCard(card);

                    }


                    // Not selected → Select
                    else {

                        selectCard(card);

                    }


                    updateSelectionUI();

                    return;

                }


                // =================================================
                // NORMAL MODE
                // Mark notification as read
                // =================================================

                markNotificationAsRead(card);

            }
        );

    }


    // =========================================================
    // CHECKBOX EVENTS
    // =========================================================

    function attachCheckboxEvent(card) {

        const checkbox =
            card.querySelector(
                ".notification-checkbox"
            );


        if (!checkbox) {
            return;
        }


        // -----------------------------------------------------
        // Prevent card click
        // -----------------------------------------------------

        checkbox.addEventListener(
            "click",
            function (event) {

                event.stopPropagation();

            }
        );


        // -----------------------------------------------------
        // Checkbox changed
        // -----------------------------------------------------

        checkbox.addEventListener(
            "change",
            function () {

                if (!selectMode) {
                    return;
                }


                if (checkbox.checked) {

                    card.classList.add(
                        "selected"
                    );

                } else {

                    card.classList.remove(
                        "selected"
                    );

                }


                updateSelectionUI();

            }
        );

    }


    // =========================================================
    // MARK NOTIFICATION AS READ
    // =========================================================

    function markNotificationAsRead(card) {

        const id =
            card.dataset.id;


        if (!id) {
            return;
        }


        fetch(
            "/notifications/read/" +
            id +
            "/",
            {

                method: "POST",

                headers: {

                    "X-CSRFToken":
                        csrftoken,

                    "X-Requested-With":
                        "XMLHttpRequest"

                },

                credentials:
                    "same-origin"

            }
        )
        .then(function (response) {

            if (!response.ok) {

                throw new Error(
                    "Failed to mark notification as read."
                );

            }

            return response.json();

        })
        .then(function (data) {

            if (!data.success) {
                return;
            }


            // Remove unread styling
            card.classList.remove(
                "unread"
            );


            // Remove unread dot
            const dot =
                card.querySelector(
                    ".unread-dot"
                );


            if (dot) {

                dot.remove();

            }


            // Update navbar bell count
            updateNavbarCount();

        })
        .catch(function (error) {

            console.error(
                "Read notification error:",
                error
            );

        });

    }


    // =========================================================
    // SELECT ALL / UNSELECT ALL
    // =========================================================

    if (selectAllBtn) {

        selectAllBtn.addEventListener(
            "click",
            function () {

                const cards =
                    getCards();

                const selected =
                    getSelectedCards();


                // =================================================
                // ALL SELECTED
                // → UNSELECT ALL
                // =================================================

                if (
                    cards.length > 0 &&
                    selected.length === cards.length
                ) {

                    cards.forEach(
                        function (card) {

                            unselectCard(card);

                        }
                    );

                }


                // =================================================
                // NOT ALL SELECTED
                // → SELECT ALL
                // =================================================

                else {

                    cards.forEach(
                        function (card) {

                            selectCard(card);

                        }
                    );

                }


                updateSelectionUI();

            }
        );

    }


    // =========================================================
    // DELETE SELECTED
    // =========================================================

    if (deleteSelectedBtn) {

        deleteSelectedBtn.addEventListener(
            "click",
            function () {

                const selected =
                    getSelectedCards();


                // Nothing selected
                if (
                    selected.length === 0
                ) {

                    return;

                }


                // Confirmation
                const confirmed =
                    confirm(
                        "Delete " +
                        selected.length +
                        " selected notification(s)?"
                    );


                if (!confirmed) {
                    return;
                }


                // Create form data
                const formData =
                    new FormData();


                selected.forEach(
                    function (card) {

                        formData.append(
                            "notification_ids[]",
                            card.dataset.id
                        );

                    }
                );


                // Send delete request
                fetch(
                    "/notifications/delete-selected/",
                    {

                        method: "POST",

                        headers: {

                            "X-CSRFToken":
                                csrftoken,

                            "X-Requested-With":
                                "XMLHttpRequest"

                        },

                        body:
                            formData,

                        credentials:
                            "same-origin"

                    }
                )
                .then(function (response) {

                    if (!response.ok) {

                        throw new Error(
                            "Delete request failed."
                        );

                    }

                    return response.json();

                })
                .then(function (data) {

                    if (!data.success) {

                        alert(
                            data.message ||
                            "Unable to delete notifications."
                        );

                        return;

                    }


                    // Remove deleted cards
                    selected.forEach(
                        function (card) {

                            card.remove();

                        }
                    );


                    // Return to normal mode
                    exitSelectMode();


                    // Check empty state
                    checkEmptyState();


                    // Update navbar badge
                    updateNavbarCount();

                })
                .catch(function (error) {

                    console.error(
                        "Delete selected error:",
                        error
                    );


                    alert(
                        "Something went wrong."
                    );

                });

            }
        );

    }


    // =========================================================
    // CLEAR ALL
    // =========================================================

    if (clearAllBtn) {

        clearAllBtn.addEventListener(
            "click",
            function () {

                const cards =
                    getCards();


                // No notifications
                if (
                    cards.length === 0
                ) {

                    return;

                }


                // Confirmation
                const confirmed =
                    confirm(
                        "Are you sure you want to delete all notifications?"
                    );


                if (!confirmed) {
                    return;
                }


                // Send delete all request
                fetch(
                    "/notifications/delete-all/",
                    {

                        method: "POST",

                        headers: {

                            "X-CSRFToken":
                                csrftoken,

                            "X-Requested-With":
                                "XMLHttpRequest"

                        },

                        credentials:
                            "same-origin"

                    }
                )
                .then(function (response) {

                    if (!response.ok) {

                        throw new Error(
                            "Clear all request failed."
                        );

                    }

                    return response.json();

                })
                .then(function (data) {

                    if (!data.success) {

                        alert(
                            data.message ||
                            "Unable to clear notifications."
                        );

                        return;

                    }


                    // Remove all cards
                    cards.forEach(
                        function (card) {

                            card.remove();

                        }
                    );


                    // Return normal mode
                    exitSelectMode();


                    // Show empty state
                    checkEmptyState();


                    // Update navbar badge
                    updateNavbarCount();

                })
                .catch(function (error) {

                    console.error(
                        "Clear all error:",
                        error
                    );


                    alert(
                        "Something went wrong."
                    );

                });

            }
        );

    }


    // =========================================================
    // EMPTY STATE
    // =========================================================

    function checkEmptyState() {

        const cards =
            getCards();


        if (
            cards.length === 0 &&
            notificationList
        ) {

            notificationList.innerHTML = `

                <div
                    class="empty-notification"
                    id="emptyNotification"
                >

                    <i
                        class="fa-regular fa-bell-slash"
                    ></i>

                    <h3>
                        No notifications
                    </h3>

                    <p>
                        You're all caught up!
                    </p>

                </div>

            `;

        }

    }


    // =========================================================
    // UPDATE NAVBAR NOTIFICATION COUNT
    // =========================================================

    function updateNavbarCount() {

        // Use navbar function if available
        if (
            typeof window.loadNotificationCount ===
            "function"
        ) {

            window.loadNotificationCount();

            return;

        }


        // Fallback
        fetch(
            "/notifications/count/"
        )
        .then(function (response) {

            if (!response.ok) {

                throw new Error(
                    "Notification count request failed."
                );

            }

            return response.json();

        })
        .then(function (data) {

            const badge =
                document.getElementById(
                    "notificationBadge"
                );


            if (!badge) {
                return;
            }


            if (data.count > 0) {

                badge.textContent =
                    data.count;

                badge.style.display =
                    "flex";

            } else {

                badge.style.display =
                    "none";

            }

        })
        .catch(function (error) {

            console.error(
                "Notification count error:",
                error
            );

        });

    }


    // =========================================================
    // INITIALIZE ALL NOTIFICATION CARDS
    // =========================================================

    getCards().forEach(
        function (card) {

            attachCardEvents(card);

            attachCheckboxEvent(card);

        }
    );


    // =========================================================
    // INITIAL UI
    // =========================================================

    updateSelectionUI();

});