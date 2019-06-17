'use strict';

var module = angular.module('adminApp', ['Constants', 'ui.router']);

require('./admin/login');
require('./admin/users');
require('./admin/courses');

module.run();

module.config(['$stateProvider', '$locationProvider', '$urlRouterProvider', function($stateProvider, $locationProvider, $urlRouterProvider) {

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
        url: 'administration/users/',
        controller: 'UsersListController',
        template: require('!!html-loader!./../templates/admin/users/list.html')
    }).state('main.base.users.create', {
        url: 'administration/users/create/',
        controller: 'UsersAddController',
        template: ''
    }).state('main.base.courses', {
        url: 'administration/courses/',
        controller: 'UsersListController',
        template: require('!!html-loader!./../templates/admin/users/list.html')
    }).state('main.base.courses.create', {
        url: 'administration/courses/create/',
        controller: 'UsersAddController',
        template: ''
    }).state('main.base.glossary', {
        url: 'administration/glossary/',
        controller: 'UsersListController',
        template: require('!!html-loader!./../templates/admin/users/list.html')
    }).state('main.base.glossary.create', {
        url: 'administration/glossary/create/',
        controller: 'UsersAddController',
        template: ''
    });


    $locationProvider.html5Mode({
        enabled: true,
        requireBase: false
    });
    $urlRouterProvider.otherwise('/');

}]);

