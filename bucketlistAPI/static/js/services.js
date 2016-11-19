var app = angular.module('LoginPageService', ['restangular'])

app.service('HostService', ['$location', function($location) {
  this.getBaseUrl = function() {
    var host = $location.host()
    var protocol = $location.protocol()
    var port = $location.port()
    var url = protocol + "://" + host + ":" + port
    return url
  }
}])


app.service('LoginService', ['Restangular', 'HostService', 'BucketLists', function(Restangular, HostService, BucketLists) {
  this.baseUrl = HostService.getBaseUrl()
  Restangular.setBaseUrl(this.baseUrl)
  this.loginUser = function(data) {
    var loginRoute = Restangular.all('/auth/login/')
    var login = loginRoute.post(data)
    return login
  }

  this.getUserDetails = function(token) {
    var userDetailsRoute = Restangular.one('/auth/me/')
    var details = userDetailsRoute.get({}, { "Authorization": "Token " + token })
    return details
  }

  this.logoutUser = function(token) {
    Restangular.setDefaultHeaders({ 'Authorization': 'Token ' + token });
    var userDetailsRoute = Restangular.one('/auth/logout/')
    var logoutResponse = userDetailsRoute.post()
    return logoutResponse
  }
}])

app.service('RegistrationService', ['HostService', 'Restangular', function(HostService, Restangular) {
  this.baseUrl = HostService.getBaseUrl()
  Restangular.setBaseUrl(this.baseUrl)
  this.registerUser = function(data) {
    // Register User
    var regRoute = Restangular.all('/auth/register/')
    var register = regRoute.post(data)
    return register
  }
}])

var app2 = angular.module('BucketlistOperationService', [])

app2.service('BucketLists', ['Restangular', 'HostService', function(Restangular, HostService) {
  this.baseUrl = HostService.getBaseUrl()
  Restangular.setBaseUrl(this.baseUrl)
  this.getBucketLists = function(auth_token) {
    Restangular.setDefaultHeaders({ 'Authorization': 'Token ' + auth_token });
    var bucketlistRouter = Restangular.all('/bucketlists/')
    var responsePromise = bucketlistRouter.getList()
    return responsePromise
  }

  this.createBucketList = function(auth_token, list_data) {
    Restangular.setDefaultHeaders({ 'Authorization': 'Token ' + auth_token });
    var createBucketlistRouter = Restangular.all('/bucketlists/')
    var createRequest = createBucketlistRouter.post(list_data)
    return createRequest
  }

  this.deleteBucketList = function(blist_id, auth_token, callback) {
    Restangular.setDefaultHeaders({ 'Authorization': 'Token ' + auth_token });
    var deleteBucketListRouter = Restangular.one('/bucketlists/', blist_id)
    deleteBucketListRouter.get().then(function(bucketlist) {
      return bucketlist.remove().then(function(res) {
        callback(res)
      })
    })
  }

  this.updateBucketlist = function(blist_id, auth_token, blist_name, callback) {
    Restangular.setDefaultHeaders({ 'Authorization': 'Token ' + auth_token });
    Restangular.setRequestSuffix('/');
    var updateBucketlistRouter = Restangular.one('/bucketlists/', blist_id)
    updateBucketlistRouter.get().then(function(bucketlist) {
      bucketlist.name = blist_name
      bucketlist.put().then(function(response) {
        callback(response)
      })
    }, function(error) {
      console.log('Error Occurred')
      console.log(error)
    })
  }

}])

app2.service('BucketlistItemService', ['Restangular', 'HostService', function(Restangular, HostService) {
  this.baseUrl = HostService.getBaseUrl()
  Restangular.setBaseUrl(this.baseUrl)
  this.addBucketlistItem = function(auth_token, bucketlist_id, item_data) {
    Restangular.setDefaultHeaders({ 'Authorization': 'Token ' + auth_token });
    var createBucketlistItemRouter = Restangular.all('/bucketlists/' + bucketlist_id + '/items/')
    var createItemRequest = createBucketlistItemRouter.post(item_data)
    return createItemRequest
  }

  this.updateBucketlistItem = function(auth_token, blist_id, item_id, item_name, callback) {
    Restangular.setDefaultHeaders({ 'Authorization': 'Token ' + auth_token });
    Restangular.setRequestSuffix('/');
    var updateBucketlistItemRouter = Restangular.one("bucketlists/" + blist_id + "/items/", item_id)
    updateBucketlistItemRouter.get().then(function(bucketlist_item) {
      bucketlist_item.item_name = item_name
      bucketlist_item.put().then(function(response) {
        callback(response)
      }, function(error) {
        console.log("Error Occurred")
        console.log(error)
      })
    })
  }
}])
