/* document.addEventListener('DOMContentLoaded', (event) => {
    const analysisNameInput = document.getElementById('analysis-name');
    const descriptionInput = document.getElementById('description');
    const fileInput = document.getElementById('file-input');
    const analysisNamePreview = document.getElementById('analysis-name-preview');
    const descriptionPreview = document.getElementById('description-preview');
    const fileNamePreview = document.getElementById('file-name-preview');

    function updatePreview() {
        analysisNamePreview.value = analysisNameInput.value;
        descriptionPreview.value = descriptionInput.value;
    }

    analysisNameInput.addEventListener('input', updatePreview);
    descriptionInput.addEventListener('input', updatePreview);

    fileInput.addEventListener('change', () => {
        const fileName = fileInput.files[0] ? fileInput.files[0].name : 'No se seleccionó archivo';
        fileNamePreview.value = fileName;
    });

    updatePreview();
}); */