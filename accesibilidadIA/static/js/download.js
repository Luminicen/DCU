document.addEventListener("DOMContentLoaded", function() {
    window.descargarContenido = function(filePath) {
        console.log("Intentando descargar desde media:", filePath);

        const url = `/analizador/descargar_contenido/${filePath}`;
        const enlace = document.createElement('a');
        enlace.href = url;
        enlace.click();
    };
});
