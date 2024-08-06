document.addEventListener('DOMContentLoaded', function() {
    var submitBtn = document.getElementById('submitBtn');
    var form = document.getElementById('analysis-form');

    if (submitBtn && form) {
        submitBtn.addEventListener('click', function(event) {
            // Evitar el envío inmediato del formulario
            event.preventDefault();

            // Mostrar el indicador de carga
            document.querySelector('.loading').style.display = 'flex';
            document.querySelector('.loading-text').style.display = 'block';
            
            // Esperar un poco antes de enviar el formulario para mostrar el indicador
            setTimeout(function() {
                form.submit();
            }, 100); // Ajusta el tiempo según sea necesario
        });
    }
});
