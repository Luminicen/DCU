descargarContenido = function (fileName) {
        if (!fileName) {
            console.error("El nombre del archivo es inválido.");
            return;
        }

        fileName = String(fileName).split('/')[String(fileName).split('/').length - 1];
        const url = `/descargar/${fileName}`;

        const enlace = document.createElement('a');
        enlace.href = url;
        enlace.download = fileName;

        document.body.appendChild(enlace);
        enlace.click();
        document.body.removeChild(enlace);
    }
