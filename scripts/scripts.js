document.addEventListener('DOMContentLoaded', function() {
    const weatherForm = document.getElementById('weatherForm');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const searchHistoryList = document.getElementById('searchHistoryList');

    weatherForm.addEventListener('submit', function() {
        showLoading();
    });

    searchHistoryList.addEventListener('click', function(event) {
        if (event.target.tagName === 'LI') {
            const city = event.target.dataset.city;
            searchCity(city);
        }
    });

    function showLoading() {
        loadingIndicator.style.display = 'flex';
    }

    function searchCity(city) {
        document.getElementById('city').value = city;
        weatherForm.submit();
    }
});
