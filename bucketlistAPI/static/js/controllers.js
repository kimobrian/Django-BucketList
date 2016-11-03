var mainApp = angular.module('MainApp', ['restangular', 'ui.router', 'ngMessages','ngStorage'])

mainApp.controller('MainCtrl', ['$scope', '$localStorage', function($scope, $localStorage){
    // auth_token = $localStorage.auth_token
    // if(typeof auth_token == 'undefined'){
    //     alert('Not Logged In')
    // }
    
}])

mainApp.config(['$stateProvider', '$urlRouteProvider',function($stateProvider, $urlRouteProvider) {
    $urlRouteProvider.otherwise('/')    
    $stateProvider
    .state('home', {
        templateUrl: '/static/templates/dashboard/home.html',
        controller: 'MainCtrl'
    })
}])