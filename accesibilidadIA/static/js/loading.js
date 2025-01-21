
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('analysis-form');
    const loadingModal = document.getElementById('loading-modal');
    const submitBtn = document.getElementById('submitBtn');

    submitBtn.addEventListener('click', (event) => {
        event.preventDefault(); 
        loadingModal.style.display = 'flex'; 
        loadingModal.setAttribute('aria-hidden', 'false');
    });

    form.addEventListener('submit', (event) => {
        event.preventDefault(); 
    });
});
