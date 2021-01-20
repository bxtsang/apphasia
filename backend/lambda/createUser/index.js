'use strict'
var AWS = require('aws-sdk');
var { default: axios } = require('axios');
var { resolve } = require('path');
const { env } = require('process');
AWS.config.update({ region: process.env.REGION });
var cognitoidentityserviceprovider = new AWS.CognitoIdentityServiceProvider({ apiVersion: '2016-04-18' });

const hasuraQuery = async (qlQuery, result) => {
  var body = {
    'query': qlQuery
  }

  try {
    const resp = await axios.post(process.env.HASURA_URI, JSON.stringify(body), {
      headers: {
        "x-hasura-admin-secret": process.env.HASURA_ADMIN_SECRET,
        "Content-Type": "application/json"
      },
    })
    console.log(resp.data)
    return {
      status: "success",
      message: "user successfully deleted from postgres db.",
      response: resp.data
    }
  } catch (err) {
    console.log(err)
    return {
      status: "failed",
      message: "failed to delete user from postgres db.",
      response: {"name": err.name, "message": err.message, "stack": err.stack}
    }
  }
}

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

  cognitoidentityserviceprovider.signUp(params, async function (err, data) {
    if (err) {
      console.log(err, err.stack);
      // result = JSON.parse(result);
      result['status'] = "failed";
      result['message'] = `failed to create user.`
      result['error'] = err

      if (err.message != "An account with the given email already exists.") {
        var tempQuery = `mutation {
          delete_staffs (
            where: {
              id: {
                _eq: ${body.input.user_id}
              }
            }
          ) {
            affected_rows
            returning {
              id
            }
          }
        }`

        const resp = await hasuraQuery(tempQuery, result)
        let message2 = resp.message
        let response2 = resp.response
        let status2 = resp.status
        result['hasura_status'] = status2
        result['hasura_message'] = message2
        result['hasura_response'] = response2
      }

      result = JSON.stringify(result)
      var response = {
        statusCode: 400,
        body: result,
        headers: { 'Content-Type': 'application/json' }
      }
      callback(null, response);
    }
    else {
          console.log(data);
          result['status'] = "success";   // successful response
          result['message'] = "user created successfully!"

        result = JSON.stringify(result)
        var response = {
          statusCode: 200,
          body: result,
          headers: { 'Content-Type': 'application/json' }
        }
        callback(null, response);
      }
  });


}
