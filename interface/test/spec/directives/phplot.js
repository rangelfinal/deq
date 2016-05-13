'use strict';

describe('Directive: phPlot', function () {

  // load the directive's module
  beforeEach(module('interfaceApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<ph-plot></ph-plot>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the phPlot directive');
  }));
});
