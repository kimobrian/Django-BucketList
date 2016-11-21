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

app.filter('offset', function() {
  return function(input, start) {
    start = parseInt(start, 10);
    return input.slice(start);
  };
});


app.controller('DashboardCtrl', ['$scope', '$window', '$localStorage', 'LoginService', '$state', 'BucketLists', 'BucketlistItemService',

  function($scope, $window, $localStorage, LoginService, $state, BucketLists, BucketlistItemService) {
    var auth_token = $localStorage.authentication_token;
    $scope.win = $window;

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
    $scope.current_blist_index = 0

    BucketLists.getBucketLists(auth_token).then(function(res) {
      $scope.bucketlists = res[0]
      $scope.current_items = res[0][0].bucketlist_items
      $scope.current_selection = res[0][0].name + " ITEMS"
      $scope.current_bucket_list = res[0][0].id
    }, function(error) {
      console.log(error)
    })

    var user_details = LoginService.getUserDetails(auth_token)
    user_details.then(function(res) {
      $scope.logged_in_username = res.username
    }, function(error) {
      if (error.statusText == 'Unauthorized') {
        $state.go('index.login')
      }
    })

    $scope.logoutUser = function() {
      var logoutStatus = LoginService.logoutUser(auth_token)
      logoutStatus.then(function(response) {
        delete $localStorage.authentication_token
        $state.go('index.login', {}, reload = true)
        $scope.win.location.reload()
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
      $scope.current_blist_index = index
    }

    $scope.editBucketlist = function(blist_id, index) {
      angular.forEach($scope.listEditMode, function(value, key) {
        $scope.listEditMode[parseInt(key)] = false
      })
      $scope.listEditMode[index] = true
    }

    function updateUI(index) {
      BucketLists.getBucketLists(auth_token).then(function(res) {
        $scope.bucketlists = res[0]
        $scope.current_items = res[0][index].bucketlist_items
        $scope.current_selection = res[0][index].name + " ITEMS"
      }, function(error) {
        console.log(error)
      })
    }

    $scope.deleteBucketlist = function(blist_id, name) {
      var confirm = $scope.win.confirm('Click OK to delete, Cancel to stop: ' + name)
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
      }else{
      }
    }

    $scope.editBucketListSubmit = function(blist_id, name, index) {
      $scope.listEditMode[index] = false
      BucketLists.updateBucketlist(blist_id, auth_token, name, function(response) {
        try{
          if(response.data.name[0] == "Bucketlist name Exists"){
            alert("Bucketlist name already exists")
            $scope.bucketlists[index].name = name
            updateUI(index)
          }
        }catch(TypeError){

        }
      })
    }

    $scope.page = function(pag){
      alert(pag)
    }

    $scope.cancelBucketlist = function(index) {
      $scope.listEditMode[index] = false
      updateUI(index)
    }

    $scope.deleteItem = function(item_id, index, bucketlist_id, current_blist_index){
      var confirm = $scope.win.confirm("Do you want to delete this item ?")
      if(confirm){
        BucketlistItemService.deleteBucketListItem(bucketlist_id, item_id, auth_token, function(response){
          updateUI(current_blist_index)
        })
      }
    }

    $scope.editItem = function(item_id, index) {
      angular.forEach($scope.itemEditMode, function(value, key) {
        $scope.itemEditMode[key] = false
      })
      $scope.itemEditMode[index] = true
    }

    $scope.editItemSubmit = function(item_id, index, item_name, status, current_blist_index) {
      $scope.itemEditMode[index] = false
      $scope.current_blist_index = current_blist_index
      
      BucketlistItemService.updateBucketlistItem(auth_token, $scope.current_bucket_list, item_id, item_name, status, function(response) {
        try{
          if(response.data.item_name[0] == "Item name already exists"){
            alert("Item name already exists")
            updateUI(current_blist_index)
          }
        }catch(TypeError){
            updateUI(current_blist_index)
        }
      })
    }

    $scope.cancelBucketlistItem = function(index, item_name, current_blist_index) {
      $scope.itemEditMode[index] = false
      updateUI(current_blist_index)
    }

    $scope.createBucketlistItem = function(blist_id, index) {
      updateUI(index)
      $scope.current_bucket_list = blist_id
      $scope.current_blist_index = index
      angular.forEach($scope.itemAddMode, function(value, key) {
        $scope.itemAddMode[key] = false
      })
      $scope.itemAddMode[index] = true
    }

    $scope.cancelNewItem = function(index) {
      $scope.itemAddMode[index] = false
    }

    $scope.createNewList = function(list_name, current_index) {
      $scope.newItem = false
      var list_data = { "name": list_name }
      BucketLists.createBucketList(auth_token, list_data).then(function(response) {
        updateUI(current_index)
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
        BucketLists.getBucketLists(auth_token).then(function(res) {
          $scope.bucketlists = res[0]
          $scope.current_items = res[0][index].bucketlist_items
          $scope.current_selection = res[0][index].name + " ITEMS"
          $scope.itemAddMode[index] = false
        }, function(error) {
          console.log(error)
        })
      }, function(error) {
        if(error.data.item_name[0] == "Item name already exists"){
          alert("Item name already exists")
        }
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
