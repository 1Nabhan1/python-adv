function toggleDurationField(form) {
    const mediaTypeSelect = form.querySelector('select[name="media_type"]');
    const durationField = form.querySelector('input[name="duration"]');
    const durationLabel = form.querySelector('label[for="duration"]');
    const audioContainer = form.querySelector('.audio-status-container');

    if (mediaTypeSelect.value === 'image') {
        durationField.required = true;
        durationField.disabled = false;
        durationField.style.display = 'inline';
        durationLabel.style.display = 'inline';
        audioContainer.style.display = 'none'; // hide audio status for images
    } else {
        durationField.required = false;
        durationField.disabled = true;
        durationField.style.display = 'none';
        durationLabel.style.display = 'none';
        durationField.value = '';
        audioContainer.style.display = 'block'; // show audio status for videos
    }
}

window.addEventListener('DOMContentLoaded', function () {
    // Select all forms on the page (you can narrow it down using a class if needed)
    const forms = document.querySelectorAll('form');

    forms.forEach(function (form) {
        const mediaTypeSelect = form.querySelector('select[name="media_type"]');
        if (mediaTypeSelect) {
            toggleDurationField(form);  // Set initial visibility
            mediaTypeSelect.addEventListener('change', function () {
                toggleDurationField(form);  // Update visibility on change
            });
        }
    });
});
