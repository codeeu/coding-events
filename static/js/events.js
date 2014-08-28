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
            minDate: "2014-01-01",
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
			if (status === google.maps.GeocoderStatus.OK) {
				document.getElementById("autocomplete").value = results[0].formatted_address;
				// the last item in the geocoder for latLng results array is the country
				var country = results[results.length - 1].address_components[0].short_name
				updateCountrySelection(country);
			}
		});
	}

	function updateLatLng(lat, lng) {
		document.getElementById("id_geoposition_0").value = lat;
		document.getElementById("id_geoposition_1").value = lng;
	}

	function createMarker(markerLatLng) {
		marker = new google.maps.Marker({
			position: markerLatLng,
			animation: google.maps.Animation.DROP,
			title: "Event location",
			draggable: true
		});

		createMap(markerLatLng, 15);

		marker.setMap(map);

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
		var geoLatLng = autocomplete.getPlace().geometry.location;
	
		createMarker(geoLatLng);
		updateAddress(geoLatLng);
	}

	function auto_complete() {
		autocomplete = new google.maps.places.Autocomplete(
			(document.getElementById('autocomplete')),
			{
				types: ['geocode']
			}
		);

		google.maps.event.addListener(autocomplete, 'place_changed', function () {
			fillInAddress();
		});
	}


	function getAddress(address) {
		geocoder = new google.maps.Geocoder();

		geocoder.geocode({'address': address}, function (results, status) {
			if (status === google.maps.GeocoderStatus.OK) {
				var updated_location = results[0].geometry.location;
				createMarker(updated_location);
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