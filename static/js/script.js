// script.js

document.addEventListener('DOMContentLoaded', function () {
    var locationInput = document.querySelector('input[name="location"]');
    var suggestionsContainer = document.createElement('div');
    suggestionsContainer.id = 'location-suggestions';
    suggestionsContainer.style.position = 'absolute';
    suggestionsContainer.style.zIndex = '1000';
    suggestionsContainer.style.border = '1px solid #ccc';
    suggestionsContainer.style.backgroundColor = '#fff';
    suggestionsContainer.style.display = 'none';
    suggestionsContainer.style.maxHeight = '200px';
    suggestionsContainer.style.overflowY = 'auto';

    locationInput.parentNode.appendChild(suggestionsContainer);

    locationInput.addEventListener('input', function () {
        var query = locationInput.value.trim();

        fetch('/autocomplete/?query=' + query)
    .then(response => response.json())
    .then(data => {
        console.log('Autocomplete Data:', data);

        // Verify if data.data is an array and has length
        if (Array.isArray(data.data) && data.data.length > 0) {
            suggestionsContainer.innerHTML = '';
            data.data.forEach(location => {
                var option = document.createElement('div');
                option.innerHTML = location.fields.name + ', ' + location.fields.country;
                option.style.padding = '8px';
                option.style.cursor = 'pointer';
                option.addEventListener('click', function () {
                    locationInput.value = location.fields.name + ', ' + location.fields.country;
                    suggestionsContainer.style.display = 'none';
                });
                suggestionsContainer.appendChild(option);
            });
            suggestionsContainer.style.display = 'block';
        } else {
            suggestionsContainer.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error fetching location suggestions:', error);
    });

    });

    // Close the suggestions dropdown when clicking outside
    document.addEventListener('click', function (event) {
        var suggestionsContainer = document.getElementById('location-suggestions');
        if (event.target !== suggestionsContainer && !suggestionsContainer.contains(event.target)) {
            suggestionsContainer.style.display = 'none';
        }
    });
});
