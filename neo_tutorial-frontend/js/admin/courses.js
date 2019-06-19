angular.module('adminApp')
    .controller('CoursesListController', ['$scope', 'coursesList', function($scope, coursesList) {
        $scope.coursesList = coursesList.data;
    }])
    .controller('CoursesAddController',
        ['$scope', 'RequestService', 'API', '$state', 'specialitiesList', function($scope, RequestService, API, $state, specialitiesList) {

        $scope.specialitiesList = specialitiesList.data;

        $scope.request = {};

        $scope.parseTags = function(tags) {
            $scope.request.tags = tags.replace(/[,.]/, '_').split(/\s+/).reduce(function(a, b, c, d) {
                if (a.indexOf(b) === -1) {
                    a.push(b);
                }
                return a;
            }, []);
        };

        $scope.newSpeciality = '';
        $scope.createCourse = function() {
            var requestData = angular.copy($scope.request);
            requestData.speciality = requestData.speciality ? requestData.speciality.id : $scope.newSpeciality;
            $scope.formResponse = {};
            RequestService.upload({
                API_PATH: API.ADMIN_PATH,
                path: API.COURSES.PATH + API.COURSES.METHODS.CREATE,
                data: requestData,
                file: $scope.coverFile
            }).then(function(response) {
                $state.go('main.base.courses_view', {id: response.data.id});
            }, function(error) {
                switch (error.status) {
                    case 400:
                        $scope.formResponse = error.data;
                        break;
                }
            });
        };


        $scope.onFileSelect = function(file) {
            $scope.coverFile = file;
        };


    }])
    .controller('CoursesViewController', ['$scope', function($scope) {

    }]);


require('./courses/lessons');
require('./courses/materials');

