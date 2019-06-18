angular.module('adminApp')
    .controller('LessonsListController', ['$scope', function($scope) {

    }])
    .controller('LessonsAddController', ['$scope', function($scope) {

        $scope.createLesson = function() {

        };

        $scope.parseYouTubeURL = function(url) {
            var ID = '';
            url = url.replace(/(>|<)/gi,'').split(/(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)/);
            if(url[2] !== undefined) {
                ID = url[2].split(/[^0-9a-z_\-]/i)[0];
            }
            else {
                ID = url[0];
            }
            console.log(ID);
        };

        $scope.activeTab = 'base';


        $scope.setActiveTab = function(tab) {
            if ($scope.activeTab === tab) {
                return;
            }
            $scope.activeTab = tab;
            if (tab === 'content') {
                setTimeout(function() {
                    var quill = new Quill('#lesson-editor', {
                        theme: 'snow',
                        modules: {
                            toolbar: '#toolbar-container'
                        }
                    });
                });
            }
        };


        var dataURLtoFile = function(dataurl, filename) {
            var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
                bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
            while(n--){
                u8arr[n] = bstr.charCodeAt(n);
            }
            return new File([u8arr], filename, {type:mime});
        };

        $scope.saveLessonContent = function() {
            var lessonContent = angular.element('#lesson-editor .ql-editor');

            var imgs = lessonContent.find('img');

            imgs.each(function(index) {
                console.log(dataURLtoFile($(this).attr('src'), 'image' + index));
            });

        };

    }])
    .controller('LessonsViewController', ['$scope', function($scope) {

    }]);