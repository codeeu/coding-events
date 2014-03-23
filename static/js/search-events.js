/*global jQuery, window, document, console, google, MarkerClusterer */

var Codeweek = window.Codeweek || {};

(function ($, Codeweek) {

    'use strict';

    var init = function (url) {


        $(function () {

            if ($.support.pjax) {
                $('.form-control').bind('change', function (e) {
                    var url_params = '',
                        search = $('#id_search').val(),
                        theme = $('input[name="theme"]:checked').map(function (_, el) {
                            return $(el).val();
                        }).get(),
                        audience = $('input[name="audience"]:checked').map(function (_, el) {
                            return $(el).val();
                        }).get();

                    if (search !== 'undefined' || search !== "") {

                    }

                    $.pjax({
                        url: url + '?search=' + $('#id_search').val() + '&country=' + $('#id_country').val() + '&category=' + categories.join(','),
                        container: '#events-container'
                    });

                    $(document).on('pjax:send', function () {
                        console.log('sending');
                    });

                    $(document).on('pjax:success', function () {
                        console.log('was ok');
                    });

                });
            }
        });
    };

    Codeweek.Search = {};
    Codeweek.Search.init = init;

}(jQuery, Codeweek));