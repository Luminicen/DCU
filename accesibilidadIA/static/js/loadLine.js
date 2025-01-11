function redirigir(analysis_id, file_name, error_name) {
    const loadingModal = document.getElementById('loading-modal');
    console.log("On loading view")
    event.preventDefault(); 
    loadingModal.style.display = 'flex'; 
    loadingModal.setAttribute('aria-hidden', 'false');
    window.location.href = `/analizador/error_result/${analysis_id}/${file_name}/${error_name}`;
}

function mergeLine(analysis_id, error_name) {
    const loadingModal = document.getElementById('loading-modal');
    console.log("On loading view")
    event.preventDefault(); 
    loadingModal.style.display = 'flex'; 
    loadingModal.setAttribute('aria-hidden', 'false');
    window.location.href = `/analizador/update_html/${analysis_id}/${error_name}`;
}

function backToResults() {
    if (document.referrer) {
        window.history.back();
    } else {
        window.location.href = `/results`;
    }
}
