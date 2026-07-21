function previewImage(input) {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            const previewImg = document.getElementById('profilePreview');
            const previewIcon = document.getElementById('previewIcon');

            if (previewImg && previewIcon) {
                previewImg.src = e.target.result;
                previewImg.classList.remove('hidden');
                previewIcon.classList.add('hidden');
            }
        }

        reader.readAsDataURL(file);
    }
}