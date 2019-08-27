angular.module('adminApp')
    .controller('UsersListController', ['$scope', 'usersList', function($scope, usersList) {
        $scope.usersList = angular.copy(usersList.data);

        $scope.sort = {};

        var applySort = function() {
            switch($scope.sort.name) {
                case 'lessons':
                    $scope.usersList.sort(function(user1, user2) {
                        return $scope.sort.asc ?
                            (user1.stats.completed_lessons_count > user2.stats.completed_lessons_count) ? 1 : -1 :
                            (user1.stats.completed_lessons_count <= user2.stats.completed_lessons_count) ? 1 : -1;
                    });
                    break;
                case 'courses-started':
                    $scope.usersList.sort(function(user1, user2) {
                        return $scope.sort.asc ?
                            (user1.stats.started_courses_count > user2.stats.started_courses_count) ? 1 : -1 :
                            (user1.stats.started_courses_count <= user2.stats.started_courses_count) ? 1 : -1;
                    });
                    break;
                case 'courses-completed':
                    $scope.usersList.sort(function(user1, user2) {
                        return $scope.sort.asc ?
                            (user1.stats.completed_courses_count > user2.stats.completed_courses_count) ? 1 : -1 :
                            (user1.stats.completed_courses_count <= user2.stats.completed_courses_count) ? 1 : -1;
                    });
                    break;
                default:
                    $scope.usersList = angular.copy(usersList.data);
            }
        };

        $scope.sortBy = function(name) {
            if ($scope.sort.name !== name) {
                $scope.sort.name = name;
                $scope.sort.asc = false;
            } else {
                if ($scope.sort.asc) {
                    $scope.sort = {};
                } else {
                    $scope.sort.asc = true;
                }
            }
            applySort();
        }

    }])

    .controller('UsersAddController', [
        '$scope', '$http', 'RequestService', 'API', '$state',
        function($scope, $http, RequestService, API, $state) {

            $scope.request = {};
            $scope.formRequest = {};

            $scope.rolesList = [
                {
                    'label': 'User',
                    'value': 0,
                    'data': {
                        'is_administrator': false,
                        'is_manager': false,
                    }
                }, {
                    'label': 'Manager',
                    'value': 1,
                    'data': {
                        'is_administrator': false,
                        'is_manager': true,
                    }
                }, {
                    'label': 'Administrator',
                    'value': 2,
                    'data': {
                        'is_administrator': true,
                        'is_manager': true,
                    }
                }
            ];


            $scope.userRole = $scope.rolesList[0];

            $scope.createUser = function() {

                var requestData = angular.extend($scope.request, $scope.userRole.data);

                $scope.formRequest.errors = undefined;

                RequestService.post({
                    API_PATH: API.ADMIN_PATH,
                    path: API.USERS.PATH + API.USERS.METHODS.CREATE,
                    data: requestData
                }).then(function(response) {
                    $state.go('main.base.users_view', {id: response.data.id});
                }, function(error) {
                    switch (error.status) {
                        case 400:
                            $scope.formRequest.errors = {
                                username: error.data
                            };
                            break;
                    }
                });
            };

        }]
    )
    .controller('UsersViewController', ['userProfile', '$scope', function(userProfile, $scope) {
        $scope.user = userProfile.data;
        console.log($scope.user);
    }]);


