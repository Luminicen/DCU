    document.addEventListener('DOMContentLoaded', () => {
        const querySelectorValue = (selector) => {
            const element = document.querySelector(selector);
            return element ? element.value.trim() : null;
        };
    
        const getCheckedValues = (name) => {
            const checkboxes = document.querySelectorAll(`input[name="${name}"]:checked`);
            return Array.from(checkboxes).map(cb => cb.value);
        };
    
        const fileNameElem = document.getElementById('file-name-preview');
        const analysisNameElem = document.getElementById('analysis-name-preview');
        const descriptionElem = document.getElementById('description-preview');
        const filtersElem = document.getElementById('filters-preview');
        const loadingModal = document.getElementById('loading-modal');
        const form = document.getElementById('analysis-form');
        const startButton = document.getElementById('submitBtn'); 
    
        
        if ('IntersectionObserver' in window) {
            const previewSection = document.querySelector('.analysis-preview-container');
    
            const observer = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        
                        const fileName = querySelectorValue('#file-input') || 'No se ha cargado archivo';
                        const analysisName = querySelectorValue('#analysis-name') || 'No se ha ingresado un nombre de análisis';
                        const description = querySelectorValue('#description') || 'No se ha completado una descripción';
                        const filters = getCheckedValues('usability-errors');
    
                        
                        if (fileNameElem) fileNameElem.innerText = fileName;
                        if (analysisNameElem) analysisNameElem.innerText = analysisName;
                        if (descriptionElem) descriptionElem.innerText = description;
                        if (filtersElem) {
                            filtersElem.innerText = filters.length > 0 ? filters.join(', ') : 'No se han seleccionado filtros';
                        }
                    }
                });
            }, { threshold: 0.5 });
    
            observer.observe(previewSection);
        } else {
            console.warn('IntersectionObserver no está soportado en este navegador.');
        }
    

        startButton.addEventListener('click', (event) => {
            event.preventDefault(); 
            loadingModal.style.display = 'flex'; 
            loadingModal.setAttribute('aria-hidden', 'false');
    
        });
    });
    
    