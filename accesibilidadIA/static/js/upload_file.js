const fileInput = document.getElementById('file-input');
        const dropArea = document.getElementById('drop-area');
        const uploadText = document.getElementById('upload-text');

        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                uploadText.textContent = 'Archivo seleccionado: ' + file.name;
            } else {
                uploadText.textContent = 'Agregar archivo HTML';
            }
        });

        dropArea.addEventListener('click', () => {
            fileInput.click();
        });

        dropArea.addEventListener('dragover', (event) => {
            event.preventDefault();
            dropArea.classList.add('dragover');
        });

        dropArea.addEventListener('dragleave', () => {
            dropArea.classList.remove('dragover');
        });

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