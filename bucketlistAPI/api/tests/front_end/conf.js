exports.config = {
   seleniumAddress: 'http://localhost:4444/wd/hub',
    capabilities: {
    'browserName': 'chrome'
  },
  
  //Specify the name of the specs files.
  specs: ['bucketlist_spec.js'],
  
  //Options to be passed to Jasmine-node.
  jasmineNodeOpts: {
      rootElement: 'body',
      onComplete: null,
      isVerbose: false,
      showColors: true,
      includeStackTrace: true
  }
};