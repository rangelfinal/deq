'use strict';

/**
 * @ngdoc directive
 * @name interfaceApp.directive:potentialPlot
 * @description
 * # potentialPlot
 */
angular.module('interfaceApp')
  .directive('potentialPlot', function () {
    return {
      template: '<canvas id="line" class="chart chart-line" chart-data="data"\
        chart-labels="labels" chart-legend="true" chart-series="series"\
        chart-click="onClick" >\
      </canvas> ',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        element.text('this is the potentialPlot directive');
      }
    };
  });
