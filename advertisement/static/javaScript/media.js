
function toggleDurationField() {
    const mediaType = document.querySelector('select[name="media_type"]').value;
    const durationField = document.getElementById('duration');
    const durationLabel = document.getElementById('duration-label');

    if (mediaType === 'image') {
        durationField.required = true;
        durationField.disabled = false;
        durationField.style.display = 'inline';  // Shows the duration field
        durationLabel.style.display = 'inline';  // Shows the label
    } else {
        durationField.required = false;
        durationField.disabled = true;
        durationField.style.display = 'none';  // Hides the duration field
        durationLabel.style.display = 'none';  // Hides the label
        durationField.value = '';  // Clears the field if hidden
    }
}

window.addEventListener('DOMContentLoaded', function () {
    toggleDurationField();  // Set initial state based on selected media type
    document.querySelector('select[name="media_type"]').addEventListener('change', toggleDurationField);  // Toggle when media type changes
});
