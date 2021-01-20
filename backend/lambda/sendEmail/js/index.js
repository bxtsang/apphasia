'use strict'
var AWS = require('aws-sdk');
AWS.config.update({ region: process.env.REGION });
var cognitoidentityserviceprovider = new AWS.CognitoIdentityServiceProvider({ apiVersion: '2016-04-18' });
// ^ Hard to find that this is the way to import the library, but it was obvious in docs

exports.handler = function (event, context, callback) {
  var result = {}
  var body = JSON.parse(event.body)

  var params = {
    AccessToken: body.input.access_token, /* required */
    AttributeName: "email", /* required */
    Code: body.input.code /* required */
  };

  cognitoidentityserviceprovider.verifyUserAttribute(params, async function(err, data) {
    if (err) {
      console.log(err, err.stack);
      result['status'] = "failed"
      result['message'] = "failed to verify attribute."
      result['error'] = err // an error occurred
      
      if (err.message = "Invalid code provided, please request a code again.") {
        var params2 = {
          ClientId: process.env.CLIENT_ID, /* required */
          Username: body.input.email, /* required */
        };
        
        cognitoidentityserviceprovider.resendConfirmationCode(params2, function(err, data) {
          if (err) {
            console.log(err, err.stack); // an error occurred
            result['status2'] = "failed"
            result['message2'] = "failed to resend verification code."
            result['error'] = err
          } 
          else {
            console.log(data);           // successful response
            result['status2'] = "success"
            result['message2'] = "sucessfully resent verification code!"
          }   
        });
      }

      result = JSON.stringify(result)
      var response = {
        statusCode: 400,
        body: result,
        headers: { 'Content-Type': 'application/json' }
      }
      callback(null, response);    // successful response
    }
      else {
        console.log(data);           // successful response
        result['status'] = "sucess"
        result['message'] = "successfully verified attribute!"

        result = JSON.stringify(result)
        var response = {
          statusCode: 200,
          body: result,
          headers: { 'Content-Type': 'application/json' }
        }
        callback(null, response);    // successful response
      }
  });
}
