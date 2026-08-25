document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.querySelector('input[type="file"][name="foto"]');
    if (!fileInput) return;
    fileInput.addEventListener('change', function () {
        if (this.files.length > 0) {
            this.closest('form').submit();
        }
    });
});
