/*global jQuery, window, document, console, google, MarkerClusterer */

var Codeweek = window.Codeweek || {};

(function ($, Codeweek) {

	'use strict';

	var datetime_handler = function () {
		var start_date = $('#id_datepicker_start'),
			end_date = $('#id_datepicker_end'),
			get_date_range = function (input) {
				var value = input.val() ? input.val() : false,
					parsed_value = [];

				if (value) {
					parsed_value = /\d{4}-\d{2}-\d{2}/.exec(value);
				}
				if (parsed_value && parsed_value.length > 0) {
					return parsed_value[0];
				}
				return false;
			};

        start_date.datetimepicker({
            format: "Y-m-d H:i",
            formatDate: "Y-m-d",
            formatTime: "H:i",
            minDate: "2015-01-01",
            closeOnDateSelect: true,
            dayOfWeekStart:1,
            onShow: function () {
                this.setOptions({
                    maxDate: get_date_range(end_date)
                });
            }
        });
        end_date.datetimepicker({
            format: "Y-m-d H:i",
            formatDate: "Y-m-d",
            formatTime: "H:i",
            minDate: 0,
            closeOnDateSelect: true,
            dayOfWeekStart:1,
            onShow: function () {
                this.setOptions({
                    minDate: get_date_range(start_date),
                    value: start_date.val()
                });
            }
        });
    },

		placeSearch,
		autocomplete,
		map,
		marker,
		geocoder,
		address;

	function createMap(latLng, zoomVal) {
		var mapOptions = {
			scrollwheel: false,
			zoom: zoomVal,
			center: latLng
		};
		map = new google.maps.Map(document.getElementById('view-event-map'), mapOptions);
	}

	function updateCountrySelection(country) {
		var choice = document.getElementById('id_country');
		selectItemByValue(choice, country);		
	}

	function updateAddress(new_latLng) {
		geocoder = new google.maps.Geocoder();
		geocoder.geocode({'latLng': new_latLng}, function (results, status) {
			if ( status === google.maps.GeocoderStatus.OK ||
				 ( status === google.maps.GeocoderStatus.ZERO_RESULTS && results.length > 0 ) ) {
				document.getElementById("autocomplete").value = results[0].formatted_address;
				// the last item in the geocoder for latLng results array is the country
				var country = results.slice(-1)[0].address_components.slice(-1)[0].short_name;
				var frenchColonies = ['MQ', 'GF', 'GP'] // Martinique, French Guiana, Guadeloupe
				if (frenchColonies.indexOf(country) >= 0) {
					country = 'FR';
				}
				updateCountrySelection(country);
			}
		});
	}

	function updateLatLng(lat, lng) {
		document.getElementById("id_geoposition_0").value = lat;
		document.getElementById("id_geoposition_1").value = lng;
	}

	function createMarker(markerLatLng, viewport) {
		if (!marker) {
			marker = new google.maps.Marker({
				position: markerLatLng,
				animation: google.maps.Animation.DROP,
				title: "Event location",
				draggable: true
			});
		} else {
			marker.setPosition(markerLatLng);
		}

		if (!map) {
			createMap(markerLatLng, 15);
		}

		marker.setMap(map);

		if (viewport) {
			map.fitBounds(viewport);
		}

		google.maps.event.addListener(marker, 'dragend', function (event) {
			updateLatLng(this.getPosition().lat(), this.getPosition().lng());
			updateAddress(marker.getPosition());
		});
	}

	function selectItemByValue(elmnt, value) {
		var i;
		for (i = 0; i < elmnt.options.length; i = i + 1) {
			if (elmnt.options[i].value === value) {
				elmnt.selectedIndex = i;
			}
		}
	}

	function listenForPastedAddress() {
		var address_field = document.getElementById('autocomplete');
		address_field.addEventListener('focusout',function () {
			var address_value = address_field.value;
			if (address_value) {
				getAddress(address_value);
			}
		}, true);
	}

	function fillInAddress() {
		// geoLatLng contains the Google Maps geocoded latitude, longitude
		var geometry = autocomplete.getPlace().geometry;
		if (!geometry) return;
		var geoLatLng = geometry.location;

		createMarker(geoLatLng, geometry.viewport);
		updateLatLng(geoLatLng.lat(), geoLatLng.lng());
		updateAddress(geoLatLng);
	}

	function auto_complete() {
		var autocompleteField = document.getElementById('autocomplete');

		autocomplete = new google.maps.places.Autocomplete(
			autocompleteField,
			{
				types: ['geocode']
			}
		);

		google.maps.event.addListener(autocomplete, 'place_changed', function () {
			fillInAddress();
		});

		$(document).on('keydown', '#autocomplete', function(event) {
			if (event.keyCode === 13) {
				event.preventDefault();
				return false;
			}
		});
	}


	function getAddress(address) {
		if (!address) return;

		geocoder = new google.maps.Geocoder();

		geocoder.geocode({'address': address}, function (results, status) {
			if (status === google.maps.GeocoderStatus.OK) {
				var updated_location = results[0].geometry.location;
				createMarker(updated_location, results[0].geometry.viewport);
				updateLatLng(updated_location.lat(), updated_location.lng());
				updateAddress(updated_location);
			}
		});
	}


	function initialize(address) {
		var initialCenter = new google.maps.LatLng(46.0608144, 14.497165600000017);
		createMap(initialCenter, 4);
		auto_complete();
		getAddress(address);
		listenForPastedAddress();

		google.maps.event.addListener(map, 'click', function (event) {
			var position = event.latLng;
			if (!position) return;

			createMarker(position);
			updateLatLng(position.lat(), position.lng());
			updateAddress(position);
		});
	}

	var add = function (address) {

		$(function () {
			google.maps.event.addDomListener(window, 'load', function () {
				address = document.getElementById('autocomplete').value;
				initialize(address);
			});

			datetime_handler();
		});

	};

	Codeweek.Event = {};
	Codeweek.Event.add = add;

}(jQuery, Codeweek));