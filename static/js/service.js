/**
 * Created by DAVID on 04/25/2018.
 */
angular.module('myApp.services', []).factory('User', function($resource) {
  return $resource('api/users', {  }, {
    update: {
      method: 'PUT',
    }
    }, {
    stripTrailingSlashes: false
    });
});