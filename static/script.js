// static/script.js

$(document).ready(function(){
    // Initialize Materialize components if you're using any
    M.AutoInit();

    // Hide the error message initially
    $('#error-message').hide();

    // Show/hide the error message based on the presence of an error
    {% if error %}
        $('#error-message').text("{{ error }}");
        $('#error-message').show();
    {% endif %}
});
