/*global jQuery, window, document, console, google, MarkerClusterer */

var Codeweek = window.Codeweek || {};

(function ($, Codeweek) {

    'use strict';

    var map,
        markers = {};

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

        for (var i = 0; i <= markerData_len; i++) {
            var markdata = markerData[i];
            if (markdata && typeof markdata === 'object') {

                var markTitle = markerData[i].fields.title,
                    map_position = markerData[i].fields.geoposition.split(","),
                    markLat = map_position[0],
                    markLng = map_position[1],
                    map_event_id = markerData[i].pk,
                    map_event_slug = markerData[i].fields.slug,
                    markUrl = "/view/" + map_event_id + "/" + map_event_slug;

                markers[map_event_id] = createMarker(markTitle, markLat, markLng, markUrl);
            }
        }

        return new MarkerClusterer(map, markers, markerClusterOptions);
    }

    function createMarker(markTitle, markLat, markLng, markUrl) {
        var myLatLng = new google.maps.LatLng(parseFloat(markLat), parseFloat(markLng));
        var marker = new google.maps.Marker({
            position: myLatLng,
            map: map,
            title: markTitle
        });
        google.maps.event.addListener(marker, 'click', function () {
            document.getElementById("clicked-marker").innerHTML = "<a href=\"" + markUrl + "\">" + markTitle + "</a>";
        });
        /*google.maps.event.addListener(marker, 'click', function() {
         window.location.href = markUrl;
         });*/
        return marker;
    }

    function setAutocomplete() {
        var input = /** @type {HTMLInputElement} */(
            document.getElementById('search-event'));
        var autocomplete = new google.maps.places.Autocomplete(input);
        autocomplete.bindTo('bounds', map);
        var infowindow = new google.maps.InfoWindow();
        google.maps.event.addListener(autocomplete, 'place_changed', function () {
            infowindow.close();
            var place = autocomplete.getPlace();
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

            var address = '';
            if (place.address_components) {
                address = [
                    (place.address_components[0] && place.address_components[0].short_name || ''),
                    (place.address_components[1] && place.address_components[1].short_name || ''),
                    (place.address_components[2] && place.address_components[2].short_name || '')
                ].join(' ');
            }
            infowindow.open(map.map);
            infowindow.close();
        });
    }


    function initialize(events, lon, lan) {
			map = createMap(events, lon, lan, 4);
			setAutocomplete();

    }

    var init = function (events, lon, lan) {


        $(function () {

            google.maps.event.addDomListener(window, 'load', function () {
                initialize(events, lon, lan);
            });

        });
    };

    Codeweek.Index = {};
    Codeweek.Index.init = init;

}(jQuery, Codeweek));