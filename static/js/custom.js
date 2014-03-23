$(function () {

	var showCountries = document.getElementById('showcountries');

	showCountries.onclick = function () {
		var div = document.getElementById('allcountries');

		if (div.style.display !== 'none') {
			div.style.display = 'none';
		}
		else {
			div.style.display = 'block';
		}
	};

});