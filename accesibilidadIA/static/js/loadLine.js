function redirigir(event, analysis_id, file_name, error_name) {
    if (event) {
        event.preventDefault(); 
    }
    console.log("Función redirigir ejecutada");
    const loadingModal = document.getElementById('loading-modal');
    loadingModal.style.display = 'flex';
    loadingModal.setAttribute('aria-hidden', 'false');
    sessionStorage.setItem('triggerModal', 'true');
    window.location.href = `/analizador/error_result/${analysis_id}/${file_name}/${error_name}`;
}

function mergeLine(event, analysis_id, error_name) {
    if (event) {
        event.preventDefault(); 
    }
    console.log("Función mergeLine ejecutada");
    const loadingModal = document.getElementById('loading-modal');
    loadingModal.style.display = 'flex';
    loadingModal.setAttribute('aria-hidden', 'false');
    sessionStorage.setItem('triggerModal', 'true');
    window.location.href = `/analizador/update_html/${analysis_id}/${error_name}`;
}
    

function backToResults() {
    sessionStorage.removeItem('triggerModal'); 
    if (document.referrer) {
        window.history.back();
    } else {
        window.location.href = `/results`;
    }
}

window.addEventListener('DOMContentLoaded', () => {
    const loadingModal = document.getElementById('loading-modal');
    const triggerModal = sessionStorage.getItem('triggerModal');

    if (triggerModal === 'true' && window.location.pathname.includes('/update_html')) {
        loadingModal.style.display = 'flex';
        loadingModal.setAttribute('aria-hidden', 'false');
        sessionStorage.removeItem('triggerModal'); 
    } else {
        loadingModal.style.display = 'none';
        loadingModal.setAttribute('aria-hidden', 'true');
    }
});


window.addEventListener('popstate', () => {
    console.log("Popstate triggered");
    const loadingModal = document.getElementById('loading-modal');
    if (loadingModal) {
        loadingModal.style.display = 'none';
        loadingModal.setAttribute('aria-hidden', 'true');
    }
});
