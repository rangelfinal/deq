'use strict';

/**
 * @ngdoc directive
 * @name interfaceApp.directive:phPlot
 * @description
 * # phPlot
 */
angular.module('interfaceApp')
  .directive('phPlot', function () {
    return {
      template: '<canvas id="line" class="chart chart-line" chart-data="data"\
        chart-labels="labels" chart-legend="true" chart-series="series"\
        chart-click="onClick" >\
      </canvas> ',
      restrict: 'E',
      link: function postLink(scope, element) {
        element.text('this is the phPlot directive');
      }
    };
  });
