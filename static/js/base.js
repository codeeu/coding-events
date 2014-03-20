/*global jQuery, window, document, console, google, MarkerClusterer */

var Codeweek = window.Codeweek || {};

(function ($, Codeweek) {

    'use strict';

    var init = function () {

        $(function () {

            // Initializing cookie consent
            $.cookieCuttr();

        });
    };

    Codeweek.Base = {};
    Codeweek.Base.init = init;

}(jQuery, Codeweek));

