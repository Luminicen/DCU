document.addEventListener("DOMContentLoaded", function() {
    // Tu código se ejecutará cuando el DOM esté completamente cargado

    function descargarContenido(fileName) {
        fileName = String(fileName).split('/')[0];
        const url = `/descargar/${fileName}`;

        const enlace = document.createElement('a');
        enlace.href = url;
        enlace.download = fileName;

        enlace.click();
    }

    function descargarContenido2(fileName, fileContent) {
        const blob = new Blob([fileContent], { type: 'text/html' });

        const url = URL.createObjectURL(blob);

        const enlace = document.createElement('a');
        enlace.href = url;
        enlace.download = fileName + '.html';

        enlace.click();

        URL.revokeObjectURL(url);
    }


});
