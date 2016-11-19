var app = angular.module('BucketListApp', ['ui.router', 'ngStorage', 'ngMessages', 'LoginPageService', 'BucketlistOperationService'])

app.config(['$stateProvider', '$urlRouterProvider', 'RestangularProvider', function($stateProvider, $urlRouterProvider, RestangularProvider) {
  $urlRouterProvider.otherwise('/index')
  $stateProvider.state('index', {
    url: '/index',
    templateUrl: '/static/templates/login.html'
  })

  $stateProvider.state('index.login', {
    url: '/login',
    templateUrl: '/static/templates/homepage/login.html'
  })

  $stateProvider.state('index.register', {
    url: '/register',
    templateUrl: '/static/templates/homepage/register.html'
  })

  $stateProvider.state('dashboard', {
    url: '/dsh',
    controller: 'DashboardCtrl',
    templateUrl: '/static/templates/main.html'
  })
}])

app.controller('LoginCtrl', ['$state', function($state) {
  $state.go('index.login')
}])

app.controller('LoginController', ['$state', '$scope', 'LoginService', '$localStorage', function($state, $scope, LoginService, $localStorage) {
  $scope.error_invalid = false
  $scope.loginUser = function() {
    data = { "username": $scope.username, "password": $scope.password }
    LoginService.loginUser(data).then(function(response) {
      if (response.hasOwnProperty('auth_token')) {
        $localStorage.authentication_token = response.auth_token
        $state.go('dashboard')
      }
    }, function(error) {
      console.log(error)
      if (error.data['non_field_errors'][0] == 'Unable to login with provided credentials.') {
        $scope.error_invalid = true
      }
    })
  }
}])

app.filter('datefilter', function() {
  return function(input_date) {
    var output = ''
    var date = input_date.slice(0, 10);
    var time = input_date.slice(11, 16)
    output = date + " " + time
    return output
  }
})


app.controller('DashboardCtrl', ['$scope', '$window', '$localStorage', 'LoginService', '$state', 'BucketLists', 'BucketlistItemService',

  function($scope, $window, $localStorage, LoginService, $state, BucketLists, BucketlistItemService) {
    var auth_token = $localStorage.authentication_token;
    if (auth_token == null || auth_token == undefined || typeof auth_token == undefined) {
      $state.go('index.login')
    }

    $scope.listEditMode = []
    $scope.itemEditMode = []
    $scope.itemAddMode = []
    $scope.next = false
    $scope.previous = false
    $scope.message = false
    $scope.bucketlists = []
    $scope.newItem = true
    $scope.current_bucket_list = false

    var user_details = LoginService.getUserDetails(auth_token)
    user_details.then(function(res) {
      $scope.logged_in_username = res.username
    }, function(error) {
      if (error.statusText == 'Unauthorized') {
        $state.go('index.login')
      }
    })

    BucketLists.getBucketLists(auth_token).then(function(res) {
      $scope.bucketlists = res[0]
      $scope.current_items = res[0][0].bucketlist_items
      $scope.current_selection = res[0][0].name + " ITEMS"
      $scope.current_bucket_list = res[0][0].id
    }, function(error) {
      console.log(error)
    })

    $scope.logoutUser = function() {
      var logoutStatus = LoginService.logoutUser(auth_token)
      logoutStatus.then(function(response) {
        delete $localStorage.authentication_token
        $state.go('index.login', {}, reload = true)
        window.location.reload()
      }, function(error) {
        console.log('Error Logout')
        if (error.status == -1) {
          alert('Connection Failed, Check your internet connection')
        }
      })
    }
    $scope.getListItems = function(blist_id, name, index) {
      $scope.current_selection = name + " ITEMS"
      $scope.current_items = $scope.bucketlists[index].bucketlist_items
      $scope.current_bucket_list = blist_id
    }

    $scope.editItem = function(item_id) {
      alert("Edit Bucketlist Item: " + item_id)
    }

    $scope.editBucketlist = function(blist_id, index) {
      angular.forEach($scope.listEditMode, function(value, key) {
        $scope.listEditMode[parseInt(key)] = false
      })
      $scope.listEditMode[index] = true
    }

    $scope.deleteBucketlist = function(blist_id, name) {
      var confirm = $window.confirm('Click OK to delete, Cancel to stop: ' + name)
      if (confirm) {
        BucketLists.deleteBucketList(blist_id, auth_token, function(response) {
          BucketLists.getBucketLists(auth_token).then(function(res) {
            $scope.bucketlists = res[0]
            $scope.current_items = res[0][0].bucketlist_items
            $scope.current_selection = res[0][0].name + " ITEMS"
          }, function(error) {
            console.log(error)
          })
        })
      }
    }

    $scope.editBucketListSubmit = function(blist_id, name, index) {
      $scope.listEditMode[index] = false
      BucketLists.updateBucketlist(blist_id, auth_token, name, function(response) {
        BucketLists.getBucketLists(auth_token).then(function(res) {
          $scope.bucketlists = res[0]
          $scope.current_items = res[0][0].bucketlist_items
          $scope.current_selection = res[0][0].name + " ITEMS"
        }, function(error) {
          console.log(error)
        })
      })
    }

    $scope.cancelBucketlist = function(index) {
      $scope.listEditMode[index] = false
      BucketLists.getBucketLists(auth_token).then(function(res) {
        $scope.bucketlists = res[0]
        $scope.current_items = res[0][0].bucketlist_items
        $scope.current_selection = res[0][0].name + " ITEMS"
      }, function(error) {
        console.log(error)
      })
    }

    $scope.editItem = function(item_id, index) {
      angular.forEach($scope.itemEditMode, function(value, key) {
        $scope.itemEditMode[key] = false
      })
      $scope.itemEditMode[index] = true
    }

    $scope.editItemSubmit = function(item_id, index, item_name) {
      $scope.itemEditMode[index] = false
      BucketlistItemService.updateBucketlistItem(auth_token, $scope.current_bucket_list, item_id, item_name, function(response) {
        console.log(response)
      })
    }

    $scope.cancelBucketlistItem = function(index) {
      $scope.itemEditMode[index] = false
    }

    $scope.createBucketlistItem = function(blist_id, $index) {
      angular.forEach($scope.itemAddMode, function(value, key) {
        $scope.itemAddMode[key] = false
      })
      $scope.itemAddMode[$index] = true
    }
    $scope.cancelNewItem = function(index) {
      $scope.itemAddMode[index] = false
    }

    $scope.createNewList = function(list_name, $event) {
      $scope.newItem = false
      var list_data = { "name": list_name }
      BucketLists.createBucketList(auth_token, list_data).then(function(response) {
        BucketLists.getBucketLists(auth_token).then(function(res) {
          $scope.bucketlists = res[0]
          $scope.current_items = res[0][0].bucketlist_items
          $scope.current_selection = res[0][0].name + " ITEMS"
        }, function(error) {
          console.log(error)
        })
      }, function(error) {
        error_message = error.data.name[0]
        if (error_message == "Bucketlist name Exists") {
          alert('Bucketlist Name already exists')
        }
        console.log(error)
      })
      $scope.list_name = ''
    }

    $scope.createNewBucketlistItem = function(blist_id, item_name, index) {
      var item_data = { "item_name": item_name }
      BucketlistItemService.addBucketlistItem(auth_token, blist_id, item_data).then(function(response) {
        console.log(response)
        BucketLists.getBucketLists(auth_token).then(function(res) {
          $scope.bucketlists = res[0]
          $scope.current_items = res[0][index].bucketlist_items
          $scope.current_selection = res[0][index].name + " ITEMS"
          $scope.itemAddMode[index] = false
        }, function(error) {
          console.log(error)
        })
      }, function(error) {
        console.log(error)
      })
    }
  }
])

app.controller('RegistrationController', ['$scope', '$state', 'RegistrationService', function($scope, $state, RegistrationService) {
  $scope.pass = ''
  $scope.username_exists = false
  $scope.registerUser = function() {
    data = { "username": $scope.username, "email": $scope.email, "password": $scope.pass }
    RegistrationService.registerUser(data).then(function(response) {
      $state.go('index.login')
    }, function(errors) {
      console.log('Error Occurred Registering')
      var error_msg = errors.data['username'][0]
      if ('A user with that username already exists.' == error_msg) {
        $scope.username_exists = true
      }
      console.log(error_msg)
    })
  }
}])
