/*global jQuery, window, document, console, google, MarkerClusterer */

var Codeweek = window.Codeweek || {};

(function ($, Codeweek) {

	'use strict';

	var i,
		map,
		markers = {},
		place,
		placeinfowindow = null,
		overlapSpiderifier = null;

	function createMap(events, lat, lng, zoomVal) {
		var markerClusterOptions = {gridSize: 30, maxZoom: 10},
			map = new google.maps.Map(document.getElementById('events-map'), {
				scrollwheel: false,
				zoom: zoomVal,
				center: new google.maps.LatLng(lat, lng),
				mapTypeControl: false,
				panControl: false,
				zoomControl: true,
				zoomControlOptions: {
					style: google.maps.ZoomControlStyle.LARGE,
					position: google.maps.ControlPosition.RIGHT_BOTTOM
				},
				scaleControl: true,
				streetViewControl: false,
				streetViewControlOptions: {
					position: google.maps.ControlPosition.RIGHT_BOTTOM
				}
			});
		overlapSpiderifier = new OverlappingMarkerSpiderfier(map,
			{markersWontMove: true, markersWontHide: true, keepSpiderfied: true, circleSpiralSwitchover: 5});
		placeinfowindow = new google.maps.InfoWindow({
			content: "loading..."
		});

		overlapSpiderifier.addListener('click', function(marker) {
			placeinfowindow.close();

			var infoWindowContent = '',
				buble_content = '',
				image = '';

			if (marker.image !== "") {
				image += '<img src="' + Codeweek.Index.media_url + marker.image + '" class="img-polaroid marker-buble-img">';
			}

			buble_content = '<div><h4><a href="' + marker.url + '" class="map-marker">' + marker.title + '</a></h4><div>' +
							  image +
							  '<p style="overflow:hidden;">' + marker.description +
							  '&nbsp;<a class="btn btn-sm" href="' + marker.url + '" class="map-marker"><span>More...</span></a></p>';

			placeinfowindow.setContent(buble_content);
			placeinfowindow.open(map, marker);
		});

		for (i = 0; i <= events.length; i = i + 1) {
			if (events[i] && typeof events[i] === 'object') {

				var markTitle = events[i].title,
					map_position = events[i].geoposition.split(","),
					markLat = map_position[0],
					markLng = map_position[1],
					map_event_id = events[i].id,
					map_event_slug = events[i].slug,
					markUrl = "/view/" + map_event_id + "/" + map_event_slug,
					markDesc = events[i].description_short,
					markImg = events[i].picture;

				markers[map_event_id] = createMarker(markTitle, markLat, markLng, markUrl, markDesc, markImg);
			}
		}

		google.maps.event.addListener(map, 'zoom_changed', function () {
			if (map.getZoom() > 15) {
				map.setZoom(15);
			} else if (map.getZoom() < 3) {
				map.setZoom(3);
			}
		});

		return new MarkerClusterer(map, markers, markerClusterOptions);
	}

	function createMarker(markTitle, markLat, markLng, markUrl, markDesc, markImg) {
		var myLatLng = new google.maps.LatLng(parseFloat(markLat), parseFloat(markLng)),
			marker = new google.maps.Marker({
				position: myLatLng,
				map: map,
				title: markTitle,
				description: markDesc,
				image: markImg,
				url: markUrl
			});
		overlapSpiderifier.addMarker(marker);

		return marker;
	}

	function setAutocomplete() {

		var input = /** @type {HTMLInputElement} */(
				document.getElementById('search-input')
				),
			options = {
				types: ['(regions)'],
				bounds: new google.maps.Circle({
					center: new google.maps.LatLng(54.977614, 13.292969),
					radius: 2700
				}).getBounds()
			},
			event_list_container = /** @type {HTMLInputElement} */(
				document.getElementById('search-events-link')
				),
			autocomplete = new google.maps.places.Autocomplete(input, options),
			infowindow = new google.maps.InfoWindow();

		autocomplete.bindTo('bounds', map);

		google.maps.event.addListener(autocomplete, 'place_changed', function () {
			infowindow.close();
			place = autocomplete.getPlace();
			if (!place.geometry) {
				return;
			}
			// If the place has a geometry, then present it on a map.
			if (place.geometry.viewport) {
				map.map.fitBounds(place.geometry.viewport);
			} else {
				map.map.setCenter(place.geometry.location);
				map.map.setZoom(17);  // Why 17? Because it looks good.
			}

			var country_code = '',
				country_name = '';
			if (place.address_components) {
				var address = place.address_components;
				for (var j = 0; j <= address.length; j++) {
					if (address[j] && address[j].types[0] === 'country') {
						country_code = address[j].short_name;
						country_name = address[j].long_name;
					}
				}

			}
			infowindow.open(map.map);
			infowindow.close();

		});
	}

	function zoomCountry(country_name) {
		var zoomgeocoder = new google.maps.Geocoder();
		zoomgeocoder.geocode({'address': country_name}, function (results, status) {
			if (status === google.maps.GeocoderStatus.OK) {
				map.map.fitBounds(results[0].geometry.viewport);
				map.map.setCenter(results[0].geometry.location);
				if (map.map.getZoom() < 3) {
					map.map.setZoom(3);
				}
			}
		});
	}

	function setSearchParams(country_code, country_name) {
		var search_button = $('#search-events-link').find('a'),
			search_button_location = search_button.attr('href'),
			new_location = search_button_location.replace(/=[A-Z]{0,2}/, "=" + country_code);

			search_button.attr('href', new_location);
			$('#country').html(country_name);
	}


	function initialize(events, lon, lan) {
		map = createMap(events, lon, lan, 3);
		//setAutocomplete();
		if (location.hash !== '') {
			var country_code = location.hash.replace('#', '').replace('!', '');
			var country = $('#' + country_code);
			if (country.length) {
				var country_name = country[0].innerText;

				zoomCountry(country_name);
				setSearchParams(country_code, country_name);
			}
		} else if (location.pathname !== "/") {
			var current_country = document.getElementById('country').innerHTML;
			zoomCountry(current_country);
		}
	}


	var init = function (past, lon, lan) {

		$(function () {
			// Initialize map on front page
			google.maps.event.addDomListener(window, 'load', function () {
				var ajaxURL = "/api/event/list/?format=json";
				if (past == "yes")
					ajaxURL = ajaxURL + "&past=yes"

				$.ajax({
					type: "GET",
					url: ajaxURL,
					error: function(jqXHR, textStatus, errorThrown) {
						// TODO: Add some error handling for real
						$('#events-map').html('<div id="api-error"><img src="/static/img/blame-the-dog.jpg"><p><strong>A dog broke our API. Catz will fix it soon. Always blame the dog!</strong></p></div>');
					},
					success: function(data, textStatus, jqXHR) {
						initialize(data, lon, lan);
					}
				});
			});

			$(".country-link").click(function (event) {
				event.preventDefault();
				var that = this,
					country_code = $(that).attr('id'),
					country_name = $(that).attr('data-name');

				zoomCountry(country_name);
				setSearchParams(country_code, country_name);
				document.location.hash = "!" + country_code;
			});

			$("#past-link").click(function (event) {	
				var newUrl = $(this).attr('href') + document.location.hash;
				$(this).attr('href', newUrl);
			});

			$("#zoomEU").click(function (event) {
				event.preventDefault();

				zoomCountry('Europe');
				setSearchParams('', 'Europe');
				document.location.hash = '';
			});
		});
	};

	Codeweek.Index = {};
	Codeweek.Index.init = init;

}(jQuery, Codeweek));

