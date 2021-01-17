'use strict'
var AWS = require('aws-sdk');
var { default: axios } = require('axios');
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
      response: err
    }
  }
}

exports.handler = function (event, context, callback) {
  var result = {}
  var body = JSON.parse(event.body)
  var params = {
    UserPoolId: process.env.USER_POOL_ID, /* required */
    Username: body.input.email, /* required */
  };

  cognitoidentityserviceprovider.adminDeleteUser(params, async function (err, data) {
    if (err) {
      console.log(err, err.stack);
      result['status'] = "failed";
      result['message'] = "failed to delete user."
      result['error'] = err

      result = JSON.stringify(result)
      var response = {
        statusCode: 400,
        body: result,
        headers: { 'Content-Type': 'application/json' }
      }
      callback(null, response);
    } // an error occurred
    else {
      console.log(data);
      result['status'] = "success";   // successful response
      result['message'] = "user deleted successfully!"

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
