angular.module('adminApp')
    .controller('LessonsListController', ['$scope', 'lessonsList', 'course', 'RequestService', 'API',
        function($scope, lessonsList, course, RequestService, API) {

        $scope.lessonsList = lessonsList.data.sort(function(lesson1, lesson2) {
            return lesson1.order > lesson2.order ? 1 : -1;
        });
        $scope.course = course.data;


        var saveSorting = function() {
            return RequestService.post({
                API_PATH: API.ADMIN_PATH,
                path: API.LESSONS.PATH + API.LESSONS.METHODS.SAVE_ORDER,
                data: {
                    course_id: $scope.course.id,
                    lesson_order: $scope.lessonsList.reduce(function(val, item) {
                        val.push(item.id);
                        return val;
                    }, [])
                }
            }).then(function(images) {

            });
        };

        $scope.toUp = function(lesson) {
            var indexItem = $scope.lessonsList.indexOf(lesson);
            var fromRight = $scope.lessonsList.length - indexItem - 1;
            $scope.lessonsList =
                $scope.lessonsList.slice(0, indexItem - 1).concat(
                    [lesson],
                    [$scope.lessonsList[indexItem - 1]],
                    fromRight ? $scope.lessonsList.slice(-fromRight) : []
                );
            saveSorting();
        };
        $scope.toBottom = function(lesson) {
            var indexItem = $scope.lessonsList.indexOf(lesson);
            var fromRight = $scope.lessonsList.length - indexItem - 2;
            $scope.lessonsList =
                $scope.lessonsList.slice(0, indexItem).concat(
                    [$scope.lessonsList[indexItem + 1]],
                    [lesson],
                    fromRight ? $scope.lessonsList.slice(-fromRight) : []
                );
            saveSorting();
        };

    }])
    .controller('LessonsAddController', ['$scope', 'RequestService', 'API', 'course', 'lesson', function($scope, RequestService, API, course, lesson) {
        $scope.course = course.data;
        if (lesson) {
            $scope.request = lesson.data;
            if ($scope.request.video_id) {
                $scope.videoURL = 'https://www.youtube.com/watch?v=' + $scope.request.video_id;
            }
        } else {
            $scope.request = {
                course_id: $scope.course.id
            }
        }



        $scope.activeTab = 'base';

        $scope.parseYouTubeURL = function(url) {
            var ID = '';
            url = url.replace(/(>|<)/gi,'').split(/(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)/);
            if(url[2] !== undefined) {
                ID = url[2].split(/[^0-9a-z_\-]/i)[0];
            }
            else {
                ID = url[0];
            }
            $scope.request.video_id = ID;
        };


        var quill;
        $scope.setActiveTab = function(tab) {
            if ($scope.activeTab === tab) {
                return;
            }
            $scope.activeTab = tab;
            if ((tab === 'content') && !quill) {
                setTimeout(function() {
                    quill = new Quill('#lesson-editor', {
                        theme: 'snow',
                        modules: {
                            toolbar: '#toolbar-container'
                        }
                    });
                });
            }
        };


        var dataURLtoFile = function(dataurl, filename) {
            var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/);

            if (!(arr && arr[1] && mime)) {
                return false;
            }

            var bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
            while(n--){
                u8arr[n] = bstr.charCodeAt(n);
            }
            return new File([u8arr], filename, {type: mime[1]});
        };




        var createLesson = function() {
            return RequestService.post({
                API_PATH: API.ADMIN_PATH,
                path: API.LESSONS.PATH + API.LESSONS.METHODS.CREATE,
                data: $scope.request
            }).then(function(result) {
                $scope.request.id = result.data.id;
                return $scope.request;
            });
        };

        var lessonContent;
        var updateLesson = function() {
            return RequestService.post({
                API_PATH: API.ADMIN_PATH,
                path: API.LESSONS.PATH + API.LESSONS.METHODS.UPDATE,
                data: angular.extend({}, $scope.request, {
                    content: lessonContent.html()
                })
            }).then(function(result) {
                $scope.request.id = result.data.id;
                return $scope.request;
            });
        };

        $scope.saveLesson = function() {

            var files = [], imgs, newImgs;

            lessonContent = angular.element('#lesson-editor .ql-editor');
            imgs = lessonContent.find('img');
            newImgs = imgs;
            imgs.each(function(index) {
                var jImg = $(this);
                var imgFile = dataURLtoFile(jImg.attr('src'));
                if (!imgFile) {
                    newImgs = newImgs.not(jImg);
                } else {
                    files.push(imgFile);
                }
            });

            var uploadFiles = function() {
                return RequestService.upload({
                    API_PATH: API.ADMIN_PATH,
                    path: API.LESSONS.PATH + API.LESSONS.METHODS.UPLOAD_IMAGES,
                    data: {
                        lesson_id: $scope.request.id
                    },
                    files: files
                }).then(function(images) {
                    newImgs.each(function(index) {
                        $(this).attr('src', images.data[index]['image_url'])
                    });
                    return images;
                });
            };

            var updateAllContent = function() {
                if (files.length) {
                    uploadFiles().then(function() {
                        updateLesson();
                    });
                } else {
                    updateLesson();
                }
            };

            if (!$scope.request.id) {
                createLesson().then(function () {
                    updateAllContent();
                });
            } else {
                updateAllContent();
            }
        };
    }])
    .controller('LessonsViewController', ['$scope', function($scope) {

    }]);