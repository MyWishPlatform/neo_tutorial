'use strict';

var module = angular.module('adminApp', ['Constants', 'ui.router', 'Services', 'Directives']);

require('./admin/login');
require('./admin/users');
require('./admin/courses');


module.run(['$rootScope', '$state', function($rootScope, $state) {
    $rootScope.currentState = $state;
}]);


module.config(['$stateProvider', '$locationProvider', '$urlRouterProvider',
    function($stateProvider, $locationProvider, $urlRouterProvider) {

    $stateProvider.state('main', {
        abstract: true,
        // templateUrl: '/templates/common/main.html',
        template: '<div ui-view></div>',
        controller: ['$rootScope', '$scope', function($rootScope, $scope) {

        }]
    }).state('main.base', {
        url: '/',
        controller: function() {}
    }).state('main.base.users', {
        url: 'users',
        controller: 'UsersListController',
        template: require('!!html-loader!./../templates/admin/users/list.html'),
        adminPart: 'users',
        resolve: {
            usersList: ['API', 'RequestService', function(API, RequestService) {
                return RequestService.get({
                    'API_PATH': API.ADMIN_PATH,
                    'path': API.USERS.PATH
                });
            }]
        }
    }).state('main.base.users_create', {
        url: 'users/create',
        controller: 'UsersAddController',
        template: require('!!html-loader!./../templates/admin/users/add.html'),
        adminPart: 'users'
    }).state('main.base.users_view', {
        url: 'users/:id',
        controller: 'UsersViewController',
        template: require('!!html-loader!./../templates/admin/users/view.html'),
        adminPart: 'users',
        resolve: {
            userProfile: ['API', 'RequestService', '$stateParams', function(API, RequestService, $stateParams) {
                return RequestService.get({
                    'API_PATH': API.ADMIN_PATH,
                    'path': API.USERS.PATH + API.USERS.METHODS.PREVIEW,
                    'params': {
                        id: $stateParams.id
                    }
                });
            }]
        }
    }).state('main.base.courses', {
        url: 'courses',
        controller: 'CoursesListController',
        template: require('!!html-loader!./../templates/admin/courses/list.html'),
        adminPart: 'courses',
        resolve: {
            coursesList: ['API', 'RequestService', function(API, RequestService) {
                return RequestService.get({
                    'API_PATH': API.ADMIN_PATH,
                    'path': API.COURSES.PATH
                });
            }]
        }
    }).state('main.base.courses_create', {
        url: 'courses/create',
        controller: 'CoursesAddController',
        template: require('!!html-loader!./../templates/admin/courses/add.html'),
        adminPart: 'courses'
    }).state('main.base.glossary', {
        url: 'glossary',
        controller: 'UsersListController',
        template: require('!!html-loader!./../templates/admin/users/list.html'),
        adminPart: 'glossary'
    }).state('main.base.glossary.create', {
        url: 'glossary/create',
        controller: 'UsersAddController',
        template: '',
        adminPart: 'glossary'
    });


    $locationProvider.html5Mode({
        enabled: true,
        requireBase: false
    });
    $urlRouterProvider.otherwise('/');

}]);

