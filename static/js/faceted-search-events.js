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
				var all_results = $('#all-search-results');
				var data = $('#faceted-search-events').serialize();
				var url = $('#faceted-search-events').attr('action');

				$.get(url, data, function(fragment) {
					History.replaceState({}, document.title, url+'?'+data);
					container.empty();
					container.html(fragment);
					var no_results = $('body').data('all_results');
					
					if (no_results > 0 ) {
						all_results.text(no_results);
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
