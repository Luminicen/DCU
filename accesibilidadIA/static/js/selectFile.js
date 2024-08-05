document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('file-input');
    const dropArea = document.getElementById('drop-area');
    const uploadText = document.getElementById('upload-text');
    let currentFile = null;

    // Handle file input change
    fileInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            currentFile = file;
            uploadText.textContent = 'Archivo seleccionado: ' + file.name;
        } else {
            if (currentFile) {
                // If there was a previously selected file, revert the input to it
                const dt = new DataTransfer();
                dt.items.add(currentFile);
                fileInput.files = dt.files;
            } else {
                uploadText.textContent = 'Agregar archivo HTML';
            }
        }
    });

    // Handle drop area click
    dropArea.addEventListener('click', () => {
        fileInput.click();
    });

    // Handle drag over
    dropArea.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropArea.classList.add('dragover');
    });

    // Handle drag leave
    dropArea.addEventListener('dragleave', () => {
        dropArea.classList.remove('dragover');
    });

    // Handle file drop
    dropArea.addEventListener('drop', (event) => {
        event.preventDefault();
        dropArea.classList.remove('dragover');
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            const dt = new DataTransfer();
            dt.items.add(file);
            fileInput.files = dt.files;
            currentFile = file;
            uploadText.textContent = 'Archivo seleccionado: ' + file.name;
        }
    });

    // Restore the previously selected file if the input is cleared
    fileInput.addEventListener('click', function() {
        if (currentFile && fileInput.files.length === 0) {
            const dt = new DataTransfer();
            dt.items.add(currentFile);
            fileInput.files = dt.files;
        }
    });
});