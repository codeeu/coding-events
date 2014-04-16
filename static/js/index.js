/*global jQuery, window, document, console, google, MarkerClusterer */

var Codeweek = window.Codeweek || {};

(function ($, Codeweek) {

    'use strict';

    var i,
        map,
        markers = {},
        place,
        placeinfowindow = null;


    function createMap(events, lat, lng, zoomVal) {
        var markerData = JSON.parse(events),
            markerData_len = markerData.length,
            markerClusterOptions = {gridSize: 30, maxZoom: 10},
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
        placeinfowindow = new google.maps.InfoWindow({
            content: "loading..."
        });

        for (i = 0; i <= markerData_len; i = i + 1) {
            var markdata = markerData[i];
            if (markdata && typeof markdata === 'object') {

                var markTitle = markerData[i].fields.title,
                    map_position = markerData[i].fields.geoposition.split(","),
                    markLat = map_position[0],
                    markLng = map_position[1],
                    map_event_id = markerData[i].pk,
                    map_event_slug = markerData[i].fields.slug,
                    markUrl = "/view/" + map_event_id + "/" + map_event_slug,
                    markDesc = markerData[i].fields.description,
                    markImg = markerData[i].fields.picture;

                markers[map_event_id] = createMarker(markTitle, markLat, markLng, markUrl, markDesc, markImg);
            }
        }

        google.maps.event.addListener(map, 'zoom_changed', function () {
            if (map.getZoom() > 15) {
                map.setZoom(15);
            }
        });

        return new MarkerClusterer(map, markers, markerClusterOptions);
    }

    function createMarker(markTitle, markLat, markLng, markUrl, markDesc, markImg) {
        var myLatLng = new google.maps.LatLng(parseFloat(markLat), parseFloat(markLng)),
            marker = new google.maps.Marker({
                position: myLatLng,
                map: map,
                title: markTitle
            });

        google.maps.event.addListener(marker, 'click', function () {
            placeinfowindow.close();

            var infoWindowContent = placeinfowindow.getContent(),
                buble_content = '',
                image = '';

            if (markImg !== "") {
                image += '<img src="' + Codeweek.Index.media_url + markImg + '" class="img-polaroid marker-buble-img">';
            }

            if (markDesc.length > 15) {
                markDesc = markDesc.substring(0, 150) + '... ';
            }

            buble_content += '<div><h4><a href="' + markUrl + '" class="map-marker">' + markTitle + '</a></h4><div>' +
                              image +
                              '<p style="overflow:hidden;">' + markDesc +
                              '&nbsp;<a href="' + markUrl + '" class="map-marker"><span>More...</span></a></p>';


            placeinfowindow.setContent(buble_content);
            placeinfowindow.open(this.map, this);
        });

        return marker;
    }

    function setAutocomplete() {

        var input = /** @type {HTMLInputElement} */(
                document.getElementById('search-input')
                ),
            options = {
                types: ['(regions)'],
                bounds: new google.maps.Circle({
                    center: new google.maps.LatLng(54.977614, 15.292969),
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
                if (map.map.getZoom() < 5) {
                    map.map.setZoom(4);
                }
            }
        });
    }

    function initialize(events, lon, lan) {
        map = createMap(events, lon, lan, 4);
        //setAutocomplete();
        if (location.hash !== '') {
            var country = $('#' + location.hash.replace('#', '').replace('!', ''));
            if (country.length) {
                zoomCountry(country[0].innerText);
            }
        } else if (location.pathname !== "/") {
            var current_country = document.getElementById('country').innerHTML;
            zoomCountry(current_country);
        }
    }


	var init = function (events, lon, lan) {

		$(function () {
			// Initialize map on front page
			google.maps.event.addDomListener(window, 'load', function () {
				initialize(events, lon, lan);
			});

			$(".country-link").click(function (event) {
				event.preventDefault();
				var that = this,
					country_code = $(that).attr('id'),
					country_name = $(that).attr('data-name'),
					search_button = $('#search-events-link').find('a'),
					search_button_location = search_button.attr('href'),
					new_location = search_button_location.replace(/([A-Z]{2})/, country_code);

				zoomCountry(country_name);
				document.location.hash = "!" + country_code;
				search_button.attr('href', new_location);
				$('#country').html(country_name);
			});

			$("#zoomEU").click(function (event) {
				event.preventDefault();
				var search_button = $('#search-events-link').find('a'),
					search_button_location = search_button.attr('href'),
					new_location = search_button_location.replace(/([A-Z]{2})/, 'EU');

				zoomCountry('Europe');
				document.location.hash = '';
				search_button.attr('href', new_location);
				$('#country').html('Europe');
			});
		});
	};

	Codeweek.Index = {};
	Codeweek.Index.init = init;

}(jQuery, Codeweek));

