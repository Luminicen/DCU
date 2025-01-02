    document.addEventListener('DOMContentLoaded', function () {
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
    
        if ('IntersectionObserver' in window) {
            const previewSection = document.querySelector('.analysis-preview-container');
    
            const observer = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        console.log("Preview section is visible again");
    
                        // Obtener valores dinámicos cada vez que sea visible
                        const fileName = querySelectorValue('#file-input') || 'No se ha cargado archivo';
                        const analysisName = querySelectorValue('#analysis-name') || 'No se ha ingresado un nombre de análisis';
                        const description = querySelectorValue('#description') || 'No se ha completado una descripción';
                        const filters = getCheckedValues('usability-errors');
    
                        // Actualizar campos en la vista previa
                        if (fileNameElem) fileNameElem.innerText = fileName;
                        if (analysisNameElem) analysisNameElem.innerText = analysisName;
                        if (descriptionElem) descriptionElem.innerText = description;
                        if (filtersElem) {
                            filtersElem.innerText = filters.length > 0 ? filters.join(', ') : 'No se han seleccionado filtros';
                        }
                    }
                });
            }, { threshold: 0.5 }); // Ejecutar cuando al menos el 50% del elemento sea visible
    
            observer.observe(previewSection);
        } else {
            console.warn('IntersectionObserver no está soportado en este navegador.');
            // Fallback: Ejecutar inmediatamente si IntersectionObserver no está disponible
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
    
    
    