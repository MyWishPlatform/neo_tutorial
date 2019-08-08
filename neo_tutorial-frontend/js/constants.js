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
            'UPDATE': 'update/',
            'GET_BY_COURSE_ID': 'by_course_id/'
        }
    },
    'LESSONS': {
        'PATH': 'lessons/',
        'METHODS': {
            'BY_COURSE_ID': 'by_course_id/',
            'CREATE': 'create/',
            'UPLOAD_IMAGES': 'upload_images/',
            'UPDATE': 'update/',
            'SAVE_ORDER': 'save_order/'
        }
    }

});
