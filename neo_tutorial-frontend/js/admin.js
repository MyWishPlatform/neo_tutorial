'use strict';

require('./constants');
require('./services/request');
require('./directives');

var module = angular.module('adminApp', ['Constants', 'ui.router', 'Services', 'Directives','ngSanitize']);

require('./admin/login');
require('./admin/users');
require('./admin/courses');


module.run(['$rootScope', '$state', '$timeout', function($rootScope, $state, $timeout) {
    $rootScope.currentState = $state;
}]);


module.config(['$httpProvider', '$qProvider', function($httpProvider, $qProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $qProvider.errorOnUnhandledRejections(false);
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
        url: 'courses/create/:id?:lng&:course_id',
        controller: 'CoursesAddController',
        template: require('!!html-loader!./../templates/admin/courses/add.html'),
        adminPart: 'courses',
        resolve: {
            specialitiesList: ['API', 'RequestService', function(API, RequestService) {
                return RequestService.get({
                    'API_PATH': API.ADMIN_PATH,
                    'path': API.COURSES.PATH + API.COURSES.METHODS.SPECIALITIES
                });
            }],
            course: ['API', 'RequestService', '$stateParams', function(API, RequestService, $stateParams) {
                if (!$stateParams.id) {
                    return false;
                } else {
                    return RequestService.get({
                        'API_PATH': API.ADMIN_PATH,
                        'path': API.COURSES.PATH + API.COURSES.METHODS.PREVIEW + $stateParams.id + '/'
                    });
                }
            }]
        }
    }).state('main.base.courses_view', {
        url: 'courses/:course_id?:lng',
        controller: 'CoursesViewController',
        template: require('!!html-loader!./../templates/admin/courses/view.html'),
        adminPart: 'courses',
        resolve: {
            course: ['$stateParams', 'RequestService', 'API', '$state', '$timeout',
                function($stateParams, RequestService, API, $state, $timeout) {

                return RequestService.get({
                    'API_PATH': API.ADMIN_PATH,
                    'path': API.COURSES.PATH + API.COURSES.METHODS.GET_BY_COURSE_ID,
                    'params': {
                        course_id: $stateParams.course_id,
                        lng: $stateParams.lng
                    }
                }).then(function(result) {
                    return result;
                }, function(err) {
                    $timeout(function() {
                        $state.transitionTo('main.base.courses_create', {
                            course_id: $stateParams.course_id,
                            lng: $stateParams.lng,
                            id: null
                        }, {
                            location: 'replace'
                        });
                    });
                    return {};
                });
            }]
        }


    }).state('main.base.lessons', {
        url: 'courses/:courseId/lessons',
        controller: 'LessonsListController',
        template: require('!!html-loader!./../templates/admin/courses/lessons/list.html'),
        adminPart: 'courses',
        resolve: {
            course: ['$stateParams', 'RequestService', 'API', function($stateParams, RequestService, API) {
                return RequestService.get({
                    'API_PATH': API.ADMIN_PATH,
                    'path': API.COURSES.PATH + 'preview/' + $stateParams.courseId + '/',
                });
            }],
            lessonsList: ['API', 'RequestService', '$stateParams', function(API, RequestService, $stateParams) {
                return RequestService.get({
                    'API_PATH': API.ADMIN_PATH,
                    'path': API.LESSONS.PATH + API.LESSONS.METHODS.BY_COURSE_ID + $stateParams.courseId + '/'
                });
            }]
        }
    }).state('main.base.lessons_create', {
        url: 'courses/:courseId/lessons/create/:id',
        controller: 'LessonsAddController',
        template: require('!!html-loader!./../templates/admin/courses/lessons/add.html'),
        adminPart: 'courses',
        resolve: {
            course: ['$stateParams', 'RequestService', 'API', function($stateParams, RequestService, API) {
                return RequestService.get({
                    'API_PATH': API.ADMIN_PATH,
                    'path': API.COURSES.PATH + 'preview/' + $stateParams.courseId + '/',
                });
            }],
            lesson: ['API', 'RequestService', '$stateParams', function(API, RequestService, $stateParams) {
                if (!$stateParams.id) {
                    return false;
                } else {
                    return RequestService.get({
                        'API_PATH': API.ADMIN_PATH,
                        'path': API.LESSONS.PATH + $stateParams.id + '/'
                    });
                }
            }]
        }
    }).state('main.base.lessons_view', {
        url: 'courses/:courseId/lessons/:id',
        controller: 'LessonsViewController',
        template: require('!!html-loader!./../templates/admin/courses/lessons/add.html'),
        adminPart: 'courses'



    }).state('main.base.materials', {
        url: 'courses/:courseId/materials',
        controller: 'MaterialsListController',
        template: require('!!html-loader!./../templates/admin/courses/materials/list.html'),
        adminPart: 'courses'
    }).state('main.base.materials_create', {
        url: 'courses/:courseId/materials/create',
        controller: 'MaterialsAddController',
        template: require('!!html-loader!./../templates/admin/courses/materials/add.html'),
        adminPart: 'courses'
    }).state('main.base.materials_view', {
        url: 'courses/:courseId/materials/:id',
        controller: 'MaterialsViewController',
        template: require('!!html-loader!./../templates/admin/courses/materials/add.html'),
        adminPart: 'courses'
    })






        .state('main.base.glossary', {
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

