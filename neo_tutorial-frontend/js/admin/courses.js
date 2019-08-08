angular.module('adminApp')
    .controller('CoursesListController', ['$scope', 'coursesList', function($scope, coursesList) {
        $scope.coursesList = coursesList.data;
    }])
    .controller('CoursesAddController',
        ['$scope', 'RequestService', 'API', '$state', 'specialitiesList', 'course', function($scope, RequestService, API, $state, specialitiesList, course) {

        $scope.specialitiesList = specialitiesList.data;

        var courseModel = course ? course.data : false;

        if (!courseModel) {
            $scope.request = {
                course_id: $state.params.course_id,
                lng: $state.params.lng
            };
        } else {
            $scope.courseTags = courseModel.tags.join(' ');
            $scope.request = {
                id: courseModel.id,
                tags: courseModel.tags,
                name: courseModel.name,
                course_id: courseModel.course_id,
                lng: courseModel.lng,
                speciality: $scope.specialitiesList.filter(function(speciality) {
                    return speciality.name === courseModel.speciality.name
                })[0],
                description: courseModel.description,
                is_active: courseModel.is_active
            };
            $scope.coverImage = '/media/' + courseModel.image.image_name;
        }

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

            if (requestData.speciality) {
                requestData.speciality = requestData.speciality.id;
            } else {
                requestData.speciality = $scope.newSpeciality;
                requestData.new_speciality = '1';
            }

            $scope.formResponse = {};

            RequestService.upload({
                API_PATH: API.ADMIN_PATH,
                path: API.COURSES.PATH + (!requestData.id ? API.COURSES.METHODS.CREATE : API.COURSES.METHODS.UPDATE),
                data: requestData,
                file: $scope.coverFile
            }).then(function(response) {
                $state.go('main.base.courses_view', {
                    course_id: requestData.course_id,
                    lng: requestData.lng
                });
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
    .controller('CoursesViewController', ['$scope', 'course', 'RequestService', 'API',
        function($scope, course, RequestService, API) {
        $scope.course = course.data;

        $scope.toggleActivation = function(isActive) {
            var requestData = angular.copy($scope.course);

            if (isActive) {
                requestData.is_active = 1;
            } else {
                delete requestData.is_active;
            }

            delete requestData.image;
            requestData.speciality = requestData.speciality.id;

            RequestService.upload({
                API_PATH: API.ADMIN_PATH,
                path: API.COURSES.PATH + (!requestData.id ? API.COURSES.METHODS.CREATE : API.COURSES.METHODS.UPDATE),
                data: requestData
            }).then(function(response) {
                $scope.course.is_active = response.data.is_active;
            });
        };
    }]);



require('./courses/lessons');
require('./courses/materials');

