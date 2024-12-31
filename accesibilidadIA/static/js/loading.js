/* document.addEventListener("DOMContentLoaded", function() {
    var submitBtn = document.getElementById("submitBtn");
    var form = document.getElementById("analysis-form");

    if (submitBtn && form) {
        submitBtn.addEventListener("click", function(event) {
            event.preventDefault();

            document.querySelector(".loading").style.display = "flex";
            document.querySelector(".loading-text").style.display = "block";
            
            setTimeout(function() {
                form.submit();
            }, 100); 
        });
    }
}); */
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('analysis-form');
    const loadingModal = document.getElementById('loading-modal');

    // Mostrar el modal al enviar el formulario
    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Evita el envío real
        loadingModal.style.display = 'flex'; // Muestra el modal
        loadingModal.setAttribute('aria-hidden', 'false');

        // Simulación de procesamiento (reemplaza con lógica real)
        setTimeout(() => {
            loadingModal.style.display = 'none'; // Oculta el modal
            loadingModal.setAttribute('aria-hidden', 'true');
            alert('Análisis completado'); // Reemplaza con redirección o lógica real
        }, 5000);
    });
});
