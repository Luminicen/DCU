document.addEventListener('DOMContentLoaded', function() {
    var submitBtn = document.getElementById('submitBtn');
    var form = document.getElementById('analysis-form');

    if (submitBtn && form) {
        submitBtn.addEventListener('click', function(event) {
            event.preventDefault();

            document.querySelector('.loading').style.display = 'flex';
            document.querySelector('.loading-text').style.display = 'block';
            
            setTimeout(function() {
                form.submit();
            }, 100); 
        });
    }
});
