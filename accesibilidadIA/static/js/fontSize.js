document.addEventListener("DOMContentLoaded", function () {
    const fontSizeSelect = document.getElementById("font-size-select");
    const rootElement = document.documentElement;

    const savedFontSize = localStorage.getItem("fontSize");
    if (savedFontSize) {
        rootElement.style.fontSize = savedFontSize;
        fontSizeSelect.value = savedFontSize;
    }

    fontSizeSelect.addEventListener("change", function () {
        const selectedFontSize = fontSizeSelect.value;
        rootElement.style.fontSize = selectedFontSize;

        localStorage.setItem("fontSize", selectedFontSize);
    });
});