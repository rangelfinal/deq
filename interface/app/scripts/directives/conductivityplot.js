'use strict';

/**
 * @ngdoc directive
 * @name interfaceApp.directive:conductivityPlot
 * @description
 * # conductivityPlot
 */
angular.module('interfaceApp')
  .directive('conductivityPlot', function () {
    return {
      template: '<canvas id="line" class="chart chart-line" chart-data="data"\
        chart-labels="labels" chart-legend="true" chart-series="series"\
        chart-click="onClick" >\
      </canvas> ',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        element.text('this is the conductivityPlot directive');
      }
    };
  });
