'use strict'
var AWS = require('aws-sdk');
AWS.config.update({ region: process.env.REGION });
var cognitoidentityserviceprovider = new AWS.CognitoIdentityServiceProvider({ apiVersion: '2016-04-18' });
// ^ Hard to find that this is the way to import the library, but it was obvious in docs

exports.handler = function (event, context, callback) {
  var result = {}
  var body = JSON.parse(event.body)
  var params = {
    ClientId: process.env.CLIENT_ID, /* required */
    Password: body.input.password, /* required */
    Username: body.input.email, /* required */
    UserAttributes: [
      {
        Name: 'custom:role', /* required */
        Value: body.input.role
      }
      /* more items */
    ],
  };

  var confirmParams = {
    UserPoolId: process.env.USER_POOL_ID, /* required */
    Username: body.input.email, /* required */
  };

  cognitoidentityserviceprovider.signUp(params, function (err, data) {
    if (err) {
      console.log(err, err.stack);
      result['status'] = "failed";
      result['message'] = "failed to create user."
      result['error'] = err
      
      result = JSON.stringify(result)
        var response = {
          statusCode: 400,
          body: result,
          headers: {'Content-Type': 'application/json'}
      }
        callback(null, response);

     }
    else {
      console.log(data);   
      cognitoidentityserviceprovider.adminConfirmSignUp(confirmParams, function(err, data) {
        if (err) {
          console.log(err, err.stack);
          result['status'] = 'failed';
          result['message'] = "user confirmation failed"
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
        callback(null, response);
      });
    }
  });


}
