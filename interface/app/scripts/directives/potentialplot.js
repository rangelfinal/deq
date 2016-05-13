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
      template: '<div></div>',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        element.text('this is the potentialPlot directive');
      }
    };
  });
