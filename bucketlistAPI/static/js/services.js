var app = angular.module('LoginPageService', ['restangular'])

app.service('HostService', ['$location', function($location){
    this.getBaseUrl = function(){
        var host = $location.host()
        var protocol = $location.protocol()
        var port = $location.port()
        var url = protocol+"://"+host+":"+port
        return url
    }
}])

app.service('LoginService', ['Restangular','HostService', function(Restangular, HostService){
      this.baseUrl = HostService.getBaseUrl()
      Restangular.setBaseUrl(this.baseUrl)
      this.loginUser = function(data){
        var loginRoute = Restangular.all('/auth/login/')
        var login = loginRoute.post(data)
        return login
      }

      this.getUserDetails = function(token){
        var userDetailsRoute = Restangular.one('/auth/me/')
        var details = userDetailsRoute.get({},{"Authorization":"Token "+token})
        return details
      }

      this.logoutUser = function(token){
        Restangular.setDefaultHeaders({'Authorization': 'Token ' + token });
        var userDetailsRoute = Restangular.one('/auth/logout/')
        var logoutResponse = userDetailsRoute.post()
        return logoutResponse
      }
}])

app.service('RegistrationService', ['HostService','Restangular', function(HostService, Restangular){
    this.baseUrl = HostService.getBaseUrl()
    Restangular.setBaseUrl(this.baseUrl)
    this.registerUser = function(data){
        // Register User
        var regRoute = Restangular.all('/auth/register/')
        var register = regRoute.post(data)
        return register
    }
}])

app.service('BucketLists', ['Restangular', 'HostService', function(Restangular, HostService){
  this.baseUrl = HostService.getBaseUrl()
  Restangular.setBaseUrl(this.baseUrl)
  this.getBucketLists = function(token){
      Restangular.setDefaultHeaders({'Authorization': 'Token ' + token });
      var bucketlists = Restangular.all('/bucketlists/')
      return bucketlists.getList()
  }
}])
