describe('Bucketlist Application Front End Tests', function() {
  beforeEach(function() {
    browser.get('http://127.0.0.1:8000/');
  });

  it('Check current page state and title', function(){
    expect(browser.getCurrentUrl()).toEqual('http://127.0.0.1:8000/#/index/login');
    expect(browser.getTitle()).toEqual('Djangular BucketList');
  })

  it('Check Invalid username password combination', function() {
    element(by.model("username")).sendKeys('username1')
    element(by.model("password")).sendKeys('passcode')
    element(by.id('loginBtn')).click()
    var error_msg = element(by.id('invalid_error')).getText()
    expect(error_msg).toEqual("Invalid Login Details")
  });

  it('Check valid username password combination', function() {
    element(by.model("username")).sendKeys('brian')
    element(by.model("password")).sendKeys('brian123')
    element(by.id('loginBtn')).click().then(function(){
      expect(browser.getCurrentUrl()).toEqual('http://127.0.0.1:8000/#/dsh');
    })
  });

  it('Check creation of new bucketlist', function(){
      element(by.model("username")).sendKeys('test_user')
      element(by.model("password")).sendKeys('testuser123')
      element(by.id('loginBtn')).click().then(function(){
        var random_bucketlist = Math.random().toString(36).substring(7);
        element(by.model('list_name')).sendKeys(random_bucketlist)
        element(by.id("create_list")).click().then(function(){
          browser.waitForAngular().then(function(){
              expect(element(by.tagName('body')).getText()).toContain(random_bucketlist.toUpperCase());
          })
      })    
    })
  }) 

  it('Checks creation of a new bucketlist item', function(){
    element(by.model("username")).sendKeys('test_user')
    element(by.model("password")).sendKeys('testuser123')
    element(by.id('loginBtn')).click().then(function(){
        var random_bucketlist = Math.random().toString(36).substring(7);
        element(by.model('list_name')).sendKeys(random_bucketlist)
        element(by.id("create_list")).click().then(function(){
          browser.waitForAngular().then(function(){
              element(by.id("addItemto0")).click()
              var random_bucketlist_item = Math.random().toString(36).substring(7);
              element(by.id("blistitem0")).sendKeys(random_bucketlist_item)
              element(by.id("submitItem0")).click().then(function(){
                browser.waitForAngular().then(function(){
                    expect(element(by.tagName('body')).getText()).toContain(random_bucketlist_item);
                })
              })
          })
      })    
    })
  })
});


