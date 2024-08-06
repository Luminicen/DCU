document.addEventListener('DOMContentLoaded', (event) => {
    // Obtener los elementos de entrada y de vista previa
    const analysisNameInput = document.getElementById('analysis-name');
    const descriptionInput = document.getElementById('description');
    const fileInput = document.getElementById('file-input');
    const analysisNamePreview = document.getElementById('analysis-name-preview');
    const descriptionPreview = document.getElementById('description-preview');
    const fileNamePreview = document.getElementById('file-name-preview');

    // Función para actualizar la vista previa
    function updatePreview() {
        analysisNamePreview.value = analysisNameInput.value;
        descriptionPreview.value = descriptionInput.value;
    }

    // Añadir event listeners a los campos de entrada
    analysisNameInput.addEventListener('input', updatePreview);
    descriptionInput.addEventListener('input', updatePreview);

    // Event listener para actualizar el nombre del archivo
    fileInput.addEventListener('change', () => {
        const fileName = fileInput.files[0] ? fileInput.files[0].name : 'No se seleccionó archivo';
        fileNamePreview.value = fileName;
    });

    // Inicializar la vista previa con los valores actuales
    updatePreview();
});