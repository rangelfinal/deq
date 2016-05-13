'use strict';

describe('Controller: GraphCtrl', function () {

  // load the controller's module
  beforeEach(module('interfaceApp'));

  var GraphCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    GraphCtrl = $controller('GraphCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(GraphCtrl.awesomeThings.length).toBe(3);
  });
});
