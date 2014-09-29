/*global jQuery, window, document, console, google, MarkerClusterer */
var Codeweek = window.Codeweek || {};

(function ($, Codeweek) {

	'use strict';

	var init = function (url) {

		$(function () {
			
			$.endlessPaginate({
				paginateOnScroll: false,
			});

			$('.search-form-element').on('change', function (e) {
				var container = $('#events-container');
				var search_counter_container = $('#search-counter-container');
				var data = $('#faceted-search-events').serialize();
				var url = $('#faceted-search-events').attr('action');

				if (is_modern_browser()) {
					$.get(url, data, function(fragment) {
						history.replaceState({}, document.title, '?' + data);
						container.empty();
						container.html(fragment);
						var no_results = $('body').data('all_results');
						var result_string = '';

						if (no_results > 0 ) {
							result_string = (no_results > 1 ? ' events match ' : ' event matches ');
							search_counter_container.html(no_results + result_string + 'your search criteria: ');
							search_counter_container.show();
						} else {
							search_counter_container.hide();
						}

					});
				} else {
					document.getElementById('faceted-search-events').submit();
				}

			});
		});
	};

	function is_modern_browser() {

		var ie_version = msieversion();

		if('querySelector' in document
		     && 'localStorage' in window
		     && 'addEventListener' in window
		     && ( ie_version==0 || ie_version > 9)) {
		     // bootstrap the javascript application
		 	return true;
		}

		return false;
	}

	function msieversion() {

		var ua = window.navigator.userAgent;
		var msie = ua.indexOf("MSIE ");

		if (msie > 0 || !!navigator.userAgent.match(/Trident.*rv\:11\./))      // If Internet Explorer, return version number
			return parseInt(ua.substring(msie + 5, ua.indexOf(".", msie)));
		return 0;
	}

	Codeweek.FacetedSearch = {};
	Codeweek.FacetedSearch.init = init;

}(jQuery, Codeweek));
