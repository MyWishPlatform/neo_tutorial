angular.module('adminApp')
    .controller('CoursesListController', ['$scope', 'coursesList', function($scope, coursesList) {
        $scope.coursesList = coursesList.data;
    }])
    .controller('UsersAddController', ['$scope', '$http', function($scope, $http) {

    }]);


