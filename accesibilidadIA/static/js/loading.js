
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('analysis-form');
    const loadingModal = document.getElementById('loading-modal');
    const submitBtn = document.getElementById('submitBtn');

    // Mostrar el modal solo al presionar "Iniciar análisis"
    submitBtn.addEventListener('click', (event) => {
        event.preventDefault(); // Evita el envío real del formulario por ahora
        loadingModal.style.display = 'flex'; // Muestra el modal
        loadingModal.setAttribute('aria-hidden', 'false');
    });

    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Evita el envío real si llega aquí por error
    });
});
