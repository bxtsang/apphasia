'use strict'
const { rejects } = require('assert');
var AWS = require('aws-sdk');
var { default: axios } = require('axios');
var { resolve } = require('path');
const { env } = require('process');
var cognitoidentityserviceprovider = new AWS.CognitoIdentityServiceProvider({ apiVersion: '2016-04-18' });
const sm = new AWS.SecretsManager('aws-sdk')
const ssm = new AWS.SSM('aws-sdk')

const getParameter = async (ParameterName) => {
  return await new Promise ((resolve, reject) => {
    var params = {
      Name: ParameterName, /* required */
      WithDecryption: false
    };
    ssm.getParameter(params, function(err, data) {
      if (err) reject (err, err.stack); // an error occurred
      else resolve(data['Parameter']['Value']);           // successful response
    });
  })
}

AWS.config.update({ region: getParameter("REGION") });

const getSecrets = async (SecretId) => {
  return await new Promise ((resolve, reject) => {
    sm.getSecretValue({ SecretId }, (err, result) => {
      if (err) reject (err)
      else resolve(JSON.parse(result.SecretString)['HASURA_ADMIN_SECRET'])
    })
  })
}

const hasuraQuery = async (qlQuery, result) => {
  var body = {
    'query': qlQuery
  }
  var hasuraUri = await getParameter("HASURA_URI_PROD")

  try {
    const resp = await axios.post(hasuraUri, JSON.stringify(body), {
      headers: {
        "x-hasura-admin-secret": getSecrets("HASURA_ADMIN_SECRET"),
        "Content-Type": "application/json"
      },
    })
    console.log(resp.data)
    return {
      status: "sent",
      message: "query successfully sent to hasura. refer to hasura_result",
      response: resp.data
    }
  } catch (err) {
    console.log(err)
    return {
      status: "failed",
      message: "failed to send query to hasura",
      response: {"name": err.name, "message": err.message, "stack": err.stack}
    }
  }
}

exports.handler = async function (event, context, callback) {
  var clientId = await getParameter("COGNITO_CLIENT_ID")

  var result = {}
  var body = JSON.parse(event.body)
  var params = {
    ClientId: clientId, /* required */
    Password: body.input.password, /* required */
    Username: body.input.email, /* required */
    UserAttributes: [
      {
        Name: 'custom:role', /* required */
        Value: body.input.role
      },
      {
        Name: 'custom:hasura_id', /* required */
        Value: body.input.user_id.toString()
      }
      /* more items */
    ],
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
