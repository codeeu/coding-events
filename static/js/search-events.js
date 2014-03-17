/*global jQuery, window, document, console, google, MarkerClusterer */

var Codeweek = window.Codeweek || {};

(function ($, Codeweek) {

    'use strict';

    var init = function (url) {


        $(function () {

            if ($.support.pjax) {
                $('.form-control').bind('change', function (e) {
                    var categories = $('input[name="category"]:checked').map(function (_, el) {
                        return $(el).val();
                    }).get();

                    $.pjax({url: url + '?search=' + $('#id_search').val() + '&country=' + $('#id_country').val() + '&category=' + categories.join(','), container: '#events-container'});

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