/**
 * Created by DAVID on 04/25/2018.
 */
angular.module('myApp.controllers', []).controller('UserListController', function($scope, $state,  User, $auth) {


 var columnDefs = [ {headerName: "Sr No", width: 50, cellRenderer: function(params) {
            return params.node.id + 1;
            }},{

    headerName: "id",
    field: "id",
    width: 100
  }, {
    headerName: "email",
    field: "email",
    width: 300
  }, {
    headerName: "name",
    field: "name",
    width: 500
  }, {
    headerName: "is_enabled",
    field: "is_enabled"
  }];


  $scope.gridOptions = {
    columnDefs: columnDefs,
    rowData: null,
    enableSorting: true,
    enableColResize: true,
    rowSelection: 'single',

  };

  User.get(function(data) {
    $scope.users = data.users;
    $scope.gridOptions.rowData = $scope.users;
    $scope.gridOptions.api.onNewRows();
    $scope.gridOptions.api.sizeColumnsToFit();
  });

}).controller('LoginController', function($auth, $state, $window, $scope, toaster) {

	 $scope.login = function() {
            $scope.credentials = {
                username: $scope.username,
                password: $scope.password
            }

            // Use Satellizer's $auth.login method to verify the username and password
            $auth.login($scope.credentials).then(function(data) {

                // If login is successful, redirect to users list

				$state.go('users');
            })
            .catch(function(response){ // If login is unsuccessful, display relevant error message.


               toaster.pop({
                type: 'error',
                title: 'Login Error',
                body: response.data,
                showCloseButton: true,
                timeout: 0
                });
               });
        }



}).controller('LogoutCtrl', function($auth,  $location, toaster) { // Logout the user if they are authenticated.


	if (!$auth.isAuthenticated()) { return; }
     $auth.logout()
      .then(function() {

        toaster.pop({
                type: 'success',
                body: 'Logging out' ,
                showCloseButton: true,

                });
        $location.url('/');
      });



}).controller('NavCtrl', function($auth,  $scope) {

	//Display the Logout button for authenticated users only
	$scope.isAuthenticated = function() {
      return $auth.isAuthenticated();
    };



});



