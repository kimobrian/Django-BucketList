angular.module('BucketList', ['ngAnimate', 'ui.router', 'ngMessages', 'LoginPageService', 'ngStorage'])
.run(function($rootScope, $templateCache) {
   $rootScope.$on('$viewContentLoaded', function() {
      $templateCache.removeAll();
   });
})
.config(function($stateProvider, $urlRouterProvider) { 
    $stateProvider    
        .state('login', {
            url: '/login',
            templateUrl: '/static/templates/homepage/login.html',
            controller: 'LoginController'
        })
        
        .state('register', {
            url: '/register',
            templateUrl: '/static/templates/homepage/register.html',
            controller: 'RegisterController'
        })      
    $urlRouterProvider.otherwise('/login');
})

.controller('LoginController', ['$scope', 'LoginService', '$localStorage', '$location', function($scope, LoginService, $localStorage, $location){
    $scope.loginUser = function(){
        var data = {username: $scope.username, password: $scope.password}
        LoginService.loginUser(data).then(function(res){
            $localStorage.auth_token = res.auth_token
            console.log($localStorage.auth_token)
            LoginService.getUserDetails($localStorage.auth_token).then(function(response){
                $localStorage.details = response
                $location.path('/dashboard/')
            })
        }, function(error){
            console.log(error)
        })
    }
}])

.controller('RegisterController', ['$scope', 'HostService', function($scope, HostService){
    
}])

