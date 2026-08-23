document.addEventListener("DOMContentLoaded", function() {
    var profilePicInput = document.getElementById("profilePicInput");
    if (profilePicInput) {
        profilePicInput.addEventListener("change", function() {
            if (this.files && this.files.length > 0) {
                this.form.submit();
            }
        });
    }

    var settingsBtn = document.getElementById("settingsBtn");
    var settingsMenu = document.getElementById("settingsMenu");

    if (settingsBtn && settingsMenu) {
        settingsBtn.addEventListener("click", function(event) {
            event.stopPropagation();
            var isOpen = settingsMenu.classList.toggle("show");
            settingsBtn.setAttribute("aria-expanded", isOpen);
        });

        settingsMenu.addEventListener("click", function(event) {
            event.stopPropagation();
        });

        document.addEventListener("click", function() {
            settingsMenu.classList.remove("show");
            settingsBtn.setAttribute("aria-expanded", "false");
        });
    }

    showPostSection("approved");
});

function showPostSection(section) {
    var approvedSection = document.getElementById("approvedPostsSection");
    var pendingSection = document.getElementById("pendingPostsSection");
    var soldSection = document.getElementById("soldPostsSection");
    var rejectedSection = document.getElementById("rejectedPostsSection");

    var approvedTab = document.getElementById("approvedTab");
    var pendingTab = document.getElementById("pendingTab");
    var soldTab = document.getElementById("soldTab");
    var rejectedTab = document.getElementById("rejectedTab");

    if (approvedSection) approvedSection.style.display = "none";
    if (pendingSection) pendingSection.style.display = "none";
    if (soldSection) soldSection.style.display = "none";
    if (rejectedSection) rejectedSection.style.display = "none";

    if (approvedTab) approvedTab.classList.remove("active");
    if (pendingTab) pendingTab.classList.remove("active");
    if (soldTab) soldTab.classList.remove("active");
    if (rejectedTab) rejectedTab.classList.remove("active");

    if (section === "approved" && approvedSection) {
        approvedSection.style.display = "block";
        if (approvedTab) approvedTab.classList.add("active");
    } else if (section === "pending" && pendingSection) {
        pendingSection.style.display = "block";
        if (pendingTab) pendingTab.classList.add("active");
    } else if (section === "sold" && soldSection) {
        soldSection.style.display = "block";
        if (soldTab) soldTab.classList.add("active");
    } else if (section === "rejected" && rejectedSection) {
        rejectedSection.style.display = "block";
        if (rejectedTab) rejectedTab.classList.add("active");
    }
}