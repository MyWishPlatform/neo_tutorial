angular.module('authApp', []).run(['$rootScope', function($rootScope) {

}]).config(['$httpProvider', '$qProvider', '$compileProvider', function($httpProvider, $qProvider, $compileProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $qProvider.errorOnUnhandledRejections(false);
    $compileProvider.aHrefSanitizationWhitelist(/^\s*(mailto|otpauth|https?):/);
}]);


angular.module('authApp').controller('AdminAuthController', ['$scope', '$http', function($scope, $http) {
    $scope.request = {};
    $scope.sendAuthForm = function () {
        $http.post('/administration/login/', $scope.request).then(function(response) {
            console.log(response);
        });
        console.log($scope.request);
    };
    return false;

}]);


