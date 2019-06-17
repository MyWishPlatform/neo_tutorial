angular.module('adminApp')
    .controller('UsersListController', ['$scope', 'usersList', function($scope, usersList) {
        $scope.usersList = usersList.data;
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

                RequestService.post({
                    API_PATH: API.ADMIN_PATH,
                    path: API.USERS.PATH + API.USERS.METHODS.CREATE,
                    data: requestData
                }).then(function(response) {
                    $state.go('main.base.users_view', {id: response.data.id});
                }, function(error) {
                    console.log(error);
                });
            };

        }]
    )
    .controller('UsersViewController', [function() {

    }]);


