document.addEventListener("DOMContentLoaded", function () {
    const fontSizeSelect = document.getElementById("font-size-select");
    const rootElement = document.documentElement;

    // Verificar si hay un tamaño de fuente guardado en localStorage
    const savedFontSize = localStorage.getItem("fontSize");
    if (savedFontSize) {
        rootElement.style.fontSize = savedFontSize;
        fontSizeSelect.value = savedFontSize;
    }

    fontSizeSelect.addEventListener("change", function () {
        const selectedFontSize = fontSizeSelect.value;
        rootElement.style.fontSize = selectedFontSize;

        // Guardar la selección del tamaño de la fuente en localStorage
        localStorage.setItem("fontSize", selectedFontSize);
    });
});