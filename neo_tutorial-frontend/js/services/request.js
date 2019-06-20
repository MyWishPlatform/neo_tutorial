angular.module('Services', ['Constants']);
angular.module('Services').service('RequestService', ['$http', 'API', function($http, API) {

    return {
        get: function (params) {
            var url = params.API_PATH || API.PATH;
            url += params.path || '';

            var httpParams = {};
            httpParams.params = params.params || params.query;

            return $http.get(url, httpParams)
        },
        post: function (params) {

            var url = params.API_PATH || API.PATH;
            url += params.path || '';

            var requestOptions = {
                method: params.method || 'POST',
                url: url,
                data: params.data,
                params: params.params
            };
            if (params.headers) {
                requestOptions.headers = params.headers;
            }
            if (params.transformRequest) {
                requestOptions.transformRequest = params.transformRequest;
            }

            return $http(requestOptions);
        },
        upload: function(params) {

            var fd = new FormData();

            for (var k in params.data) {
                if (!angular.isArray(params.data[k])) {
                    fd.append(k, params.data[k]);
                } else {
                    fd.append(k, JSON.stringify(params.data[k]));
                }
            }

            if (params.file) {
                fd.append("image", params.file);
            }

            var url = params.API_PATH || API.PATH;
            url += params.path || '';

            var requestOptions = {
                headers: {'Content-Type': undefined},
                // transformRequest: angular.identity
            };

            return $http.post(url, fd, requestOptions);
        }
    }
}]);
