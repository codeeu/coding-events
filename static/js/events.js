/*global jQuery, window, document, console, google, MarkerClusterer */

var Codeweek = window.Codeweek || {};

(function ($, Codeweek) {

    'use strict';
    var datetime_handler = function () {
        var start_date = $('#id_datepicker_start'),
            end_date = $('#id_datepicker_end'),
            now = new Date(),
            localdate = (
                now.getFullYear() + '-' +
                    (now.getMonth() + 1) + '-' +
                    now.getDate() + ' ' +
                    now.getHours() + ':' +
                    now.getMinutes()
            );

        start_date.datetimepicker({
            format: "yyyy-mm-dd hh:ii",
            autoclose: true,
            todayBtn: true,
            startDate: localdate,
            minuteStep: 10
        });
        end_date.datetimepicker({
            format: "yyyy-mm-dd hh:ii",
            autoclose: true,
            todayBtn: true,
            startDate: localdate,
            minuteStep: 10
        });
        end_date.on('changeDate', function (ev) {
            console.log(start_date.val());
            if (ev.date.valueOf() < start_date.valueOf()) {
                console.log('no can do');
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

    function updateAddress(new_position) {
        geocoder = new google.maps.Geocoder();
        geocoder.geocode({'latLng': new_position}, function (results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
                document.getElementById("autocomplete").value = results[0].formatted_address;
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

    function fillInAddress() {
        var i,
            component,
            choice,
            place = autocomplete.getPlace(),
            components = place.address_components,
            country = null,
            output = autocomplete.getPlace().geometry.location,
            outputLat = output.lat(),
            outputLng = output.lng(),
            locLatlng = new google.maps.LatLng(outputLat, outputLng);

        document.getElementById("id_geoposition_0").value = outputLat;
        document.getElementById("id_geoposition_1").value = outputLng;

        createMarker(locLatlng);
        for (i = 0; component = components[i]; i = i + 1) {
            if (component.types[0] === 'country') {
                country = component.short_name;
                choice = document.getElementById('id_country');
                selectItemByValue(choice, country);
            }
        }

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
            }
        });
    }


    function initialize(address) {
        var initialCenter = new google.maps.LatLng(46.0608144, 14.497165600000017);
        createMap(initialCenter, 4);
        auto_complete();
        getAddress(address);

    }

    var add = function (address) {

        $(function () {
            google.maps.event.addDomListener(window, 'load', function () {
                initialize(address);
            });

            datetime_handler();
        });

    };

    Codeweek.Event = {};
    Codeweek.Event.add = add;

}(jQuery, Codeweek));