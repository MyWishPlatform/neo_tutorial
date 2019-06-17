angular.module('adminApp')
    .controller('UsersListController', ['$scope', 'usersList', function($scope, usersList) {
        $scope.usersList = usersList.data;
    }])
    .controller('UsersAddController', ['$scope', '$http', function($scope, $http) {

    }]);


