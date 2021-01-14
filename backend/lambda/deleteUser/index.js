'use strict'
var AWS = require('aws-sdk');
AWS.config.update({ region: process.env.REGION });
var cognitoidentityserviceprovider = new AWS.CognitoIdentityServiceProvider({ apiVersion: '2016-04-18' });
// ^ Hard to find that this is the way to import the library, but it was obvious in docs

exports.handler = function (event, context, callback) {
  var result = {}

  var params = {
    UserPoolId: process.env.USER_POOL_ID, /* required */
    Username: event.username, /* required */
  };

  cognitoidentityserviceprovider.adminDeleteUser(params, function(err, data) {
    if (err) {
      console.log(err, err.stack);
      result['status'] = "failed";
      result['message'] = "failed to delete user."
      result['error'] = err

      result = JSON.stringify(result)
      var response = {
        statusCode: 400,
        body: result,
        headers: {'Content-Type': 'application/json'}
    }
      callback(null, response);
     } // an error occurred
    else {
      console.log(data); 
          result['status'] = "success";   // successful response
          result['message'] = "user created successfully!"
        }   
        
        result = JSON.stringify(result)
        var response = {
          statusCode: 200,
          body: result,
          headers: {'Content-Type': 'application/json'}
      }
        callback(null, response);    // successful response
  });


}
