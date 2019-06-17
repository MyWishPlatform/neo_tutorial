angular.module('adminApp')
    .controller('CoursesListController', ['$scope', 'coursesList', function($scope, coursesList) {
        $scope.coursesList = coursesList.data;
    }])
    .controller('CoursesAddController', ['$scope', '$http', function($scope, $http) {

    }]);


