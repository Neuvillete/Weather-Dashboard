function showLoading() {
    document.getElementById("loadingIndicator").style.display = "flex";
}

function searchCity(city) {
    document.getElementById("city").value = city;
    document.getElementById("weatherForm").submit();
}
