/*global jQuery, window, document, console, google, MarkerClusterer */
var Codeweek = window.Codeweek || {};

(function ($, Codeweek) {

	'use strict';

	var init = function (url) {

		$(function () {
			
			$.endlessPaginate({
				paginateOnScroll: true,
				paginateOnScrollMargin: 20
			});

			$('.search-form-element').on('change', function (e) {
				var container = $('#events-container');
				var data = $('#faceted-search-events').serialize();
				var url = $('#faceted-search-events').attr('action');

				$.post(url, data, function(fragment) {
					container.empty();
					container.html(fragment);
				});
			});
		});
	};

	Codeweek.FacetedSearch = {};
	Codeweek.FacetedSearch.init = init;

}(jQuery, Codeweek));
