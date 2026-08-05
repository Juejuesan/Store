/* ==========================================
   MESSAGE BOX
==========================================*/

const overlay = document.getElementById("messageOverlay");
const closeBtn = document.getElementById("closeMessage");

if (overlay && closeBtn) {

    closeBtn.addEventListener("click", function () {

        // Fade out animation
        overlay.style.opacity = "0";

        setTimeout(function () {

            overlay.remove();

        }, 300);

    });

}