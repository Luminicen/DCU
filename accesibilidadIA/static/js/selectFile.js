document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('file-input');
    const dropArea = document.getElementById('drop-area');
    const uploadText = document.getElementById('upload-text');

    // Handle file input change
    fileInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            uploadText.textContent = 'Archivo seleccionado: ' + file.name;
        } else {
            uploadText.textContent = 'Agregar archivo HTML';
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
            fileInput.files = files;
            const file = files[0];
            uploadText.textContent = 'Archivo seleccionado: ' + file.name;
        }
    });
});
