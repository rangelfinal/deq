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
      template: '<div></div>',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        element.text('this is the phPlot directive');
      }
    };
  });
