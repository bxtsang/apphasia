'use strict'
var AWS = require('aws-sdk');
AWS.config.update({ region: process.env.REGION });
var cognitoidentityserviceprovider = new AWS.CognitoIdentityServiceProvider({ apiVersion: '2016-04-18' });
// ^ Hard to find that this is the way to import the library, but it was obvious in docs

exports.handler = function (event, context, callback) {
  var result = {}

  var params = {
    UserAttributes: [ /* required */
      {
        Name: 'custom:role',
        Value: event.role
      },
      {
        Name: 'email',
        Value: event.new_email
      }
      /* more items */
    ],
    UserPoolId: process.env.USER_POOL_ID, /* required */
    Username: event.email, /* required */
  };
  cognitoidentityserviceprovider.adminUpdateUserAttributes(params, function(err, data) {
    if (err) {
      console.log(err, err.stack); // an error occurred
      result['status'] = "failed";
      result['message'] = "failed to update user."
      result['error'] = err
      
      result = JSON.stringify(result)
        var response = {
          statusCode: 400,
          body: result,
          headers: {'Content-Type': 'application/json'}
      }
        callback(null, response);

    } else {
      console.log(data);           // successful response
      result['status'] = "success";
      result['message'] = "user updated successfully!"
      
      result = JSON.stringify(result)
        var response = {
          statusCode: 200,
          body: result,
          headers: {'Content-Type': 'application/json'}
      }
        callback(null, response);

    }
  });


}
