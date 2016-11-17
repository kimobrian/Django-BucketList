var app = angular.module('BucketListApp', ['ui.router', 'ngStorage', 'ngMessages', 'LoginPageService'])

app.config(['$stateProvider','$urlRouterProvider',function($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/index')
    $stateProvider.state('index', {
        url:'/index',
        templateUrl: '/static/templates/login.html'
    })

    $stateProvider.state('index.login', {
        url:'/login',
        templateUrl: '/static/templates/homepage/login.html'
    })

    $stateProvider.state('index.register', {
        url:'/register',
        templateUrl: '/static/templates/homepage/register.html'
    })

    $stateProvider.state('dashboard', {
        url:'/dsh',
        templateUrl: '/static/templates/main.html'
    })
}])

app.controller('LoginCtrl', ['$state', function($state){
    $state.go('index.login')
}])

app.controller('LoginController', ['$state','$scope','LoginService', '$localStorage', function($state, $scope, LoginService, $localStorage){
    $scope.error_invalid = false
    $scope.loginUser = function(){
        data = {"username": $scope.username, "password": $scope.password}
        LoginService.loginUser(data).then(function(response){
            if(response.hasOwnProperty('auth_token')){
                $localStorage.authentication_token = response.auth_token
                $state.go('dashboard')
            }
        }, function(error){
            console.log(error)
            if(error.data['non_field_errors'][0] == 'Unable to login with provided credentials.'){
                $scope.error_invalid = true
            }
        })
    }
}])

app.controller('DashboardCtrl', ['$scope','$localStorage', 'LoginService','$state', 'BucketLists', function($scope, $localStorage, LoginService, $state, BucketLists){
    var auth_token = $localStorage.authentication_token;

    if(auth_token == null || auth_token == undefined || typeof auth_token == undefined){
        $state.go('index.login')
    } 

    bucket_lists = BucketLists.getBucketLists(auth_token).$object
    // bucket_lists.then(function(res){
    //     console.log(res)
    // })
    //     console.log(res)
    // }, function(errors){
    //     console.log(errors)
    // })
    var user_details = LoginService.getUserDetails(auth_token)
    user_details.then(function(res){
        $scope.logged_in_username = res.username
    }, function(error){
        console.log('Unauthorized Access')
        if(error.statusText == 'Unauthorized'){
            $state.go('index.login')
        }
    })

    $scope.logoutUser = function(){
        var logoutStatus = LoginService.logoutUser(auth_token)
        logoutStatus.then(function(response){
            delete $localStorage.authentication_token
            $state.go('index.login', {}, reload=true)
            window.location.reload()
        }, function(error){
            console.log('Error Logout')
            if(error.status == -1){
                alert('Connection Failed, Check your internet connection')
            }
        })
    } 
}])

app.controller('RegistrationController', ['$scope', '$state', 'RegistrationService',  function($scope, $state, RegistrationService){
    $scope.pass =''
    $scope.username_exists = false
    $scope.registerUser = function(){
        data = {"username":$scope.username, "email": $scope.email, "password": $scope.pass}
        RegistrationService.registerUser(data).then(function(response){
            $state.go('index.login')
        }, function(errors){
            console.log('Error Occurred Registering')
            var error_msg = errors.data['username'][0]
            if('A user with that username already exists.' == error_msg){
                    $scope.username_exists = true
            }
            console.log(error_msg)
        })
    }
}])

