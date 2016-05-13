'use strict';

/**
 * @ngdoc directive
 * @name interfaceApp.directive:inlineField
 * @description
 * # inlineField
 */
angular.module('interfaceApp')
  .directive('inlineField', function () {
    return {
      scope: {
        label: '=',
        type: '=',
        rightLabel: '=',
        leftLabel: '=',
        name: '='
      },
      template: '<div class="inline field">\
        <div class="ui right labeled input" ngClass="{right labeled: rightLabel, left labeled: leftLabel}">\
          <label>{{label}}</label>\
          <div ngIf="leftLabel" class="ui basic label">{{leftLabel}}</div>\
          <input name="{{name || "input"}}" type="{{type}}">\
          <div ngIf="rightLabel" class="ui basic label">{{rightLabel}}</div>\
        </div>\
      </div>',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        element.text('this is the inlineField directive');
      }
    };
  });
