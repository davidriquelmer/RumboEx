/**
 * Created by DAVID on 04/25/2018.
 */
angular.module('myApp', ['ui.router', 'ngResource', 'myApp.controllers', 'myApp.services', "angularGrid" , 'satellizer','toaster', 'ngAnimate']);

angular.module('myApp').config(function($stateProvider, $urlRouterProvider, $authProvider) {

	  // Satellizer configuration that specifies which API
            // route the JWT should be retrieved from
            $authProvider.loginUrl = '/api/login';
            $urlRouterProvider.otherwise('/');

  $stateProvider. state('login', {
	url: '/login',
	templateUrl: 'partials/login.html',
	controller: 'LoginController',
    resolve: {
          skipIfLoggedIn: skipIfLoggedIn
        }

  }).state('users', { // state for showing all users
    url: '/',
    templateUrl: 'partials/users.html',
    controller: 'UserListController',
    resolve: { //resolve only for authenticated users
          loginRequired: loginRequired
        }
  }).state('logout', {
        url: '/logout',
        template: null,
        controller: 'LogoutCtrl'
      });


  //If a user is already logged in, the Login window if requested need not be displayed.
   function skipIfLoggedIn($q, $auth) {
      var deferred = $q.defer();
      if ($auth.isAuthenticated()) {
        deferred.reject();
      } else {
        deferred.resolve();
      }
      return deferred.promise;
    }

   //Redirect unauthenticated users to the login state
   function loginRequired($q, $location, $auth, $state) {
      var deferred = $q.defer();
      if ($auth.isAuthenticated()) {
        deferred.resolve();
      } else {
        $location.path('/login');
      }
      return deferred.promise;
    }

});