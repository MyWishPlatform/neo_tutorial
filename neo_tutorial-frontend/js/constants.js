angular.module('Constants', []).constant('API', {
    'PATH': '/api/',
    'ADMIN_PATH': '/administration/api/',
    'USERS': {
        'PATH': 'users/',
        'METHODS': {
            'CREATE': 'create/',
            'PREVIEW': 'preview/'
        }
    },

    'COURSES': {
        'PATH': 'courses/',
        'METHODS': {
            'CREATE': 'create/',
            'PREVIEW': 'preview/',
            'SPECIALITIES': 'specialities/',
            'UPDATE': 'update/'
        }
    }

});
