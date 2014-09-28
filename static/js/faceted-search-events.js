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

				$.get(url, data, function(fragment) {
					History.replaceState({}, document.title, url+'?'+data);
					container.empty();
					container.html(fragment);
					var no_results = $('body').data('all_results');
					var result_string = '';

					if (no_results > 0 ) {
						result_string = (no_results > 1 ? ' events match ' : ' event matches ');
						search_counter_container.html(no_results + result_string + 'your search criteria: ');
						$('#all-search-results').show();
					} else {
						$('#all-search-results').hide();
					}

				});
			});
		});
	};

	Codeweek.FacetedSearch = {};
	Codeweek.FacetedSearch.init = init;

}(jQuery, Codeweek));
