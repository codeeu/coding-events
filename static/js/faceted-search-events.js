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

				if (!Modernizr.history) {
					document.getElementById('faceted-search-events').submit();
				} else {
					$("#events-container").html("<img id='loading-gif' src='/static/img/loading.gif'/>");
					$('#events-container').load(url + " #events-container", data);
				}
			});
		});
	};

	Codeweek.FacetedSearch = {};
	Codeweek.FacetedSearch.init = init;

}(jQuery, Codeweek));
