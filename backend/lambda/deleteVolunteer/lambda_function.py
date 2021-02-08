import requests
import psycopg2
import os
import json
import boto3


def lambda_handler(event, context):
    result = {}
    statusCode = 500
    print(str(0))

    try :
        secret = get_secret()
        con = psycopg2.connect (
            host =  secret['host'],
            database= secret['dbname'],
            user= secret['username'],
            port = secret['port'],
            password= secret['password']
        )

        cur = con.cursor()
        query = "DELETE FROM volunteers WHERE rejected_date IS NOT NULL AND status ='Rejected' AND EXTRACT(DAY FROM (current_date at time zone 'UTC') - rejected_date) >= 30 RETURNING *"
        cur.execute(query)
        con.commit()

        message = cur.fetchall()
        statusCode = 200
        result['status'] = 'success'
        result['message'] = str(message)
        print(message)
        con.close()

    except Exception as e:
        print(e)
        statusCode = 400
        result['status'] = "failed"
        result['message'] = str(e)

    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(result)
    }

def get_secret():
    clientSecret = boto3.client('secretsmanager')
    secret_name = "aphasiaDB"

    response = clientSecret.get_secret_value(
        SecretId = secret_name
    )

    return json.loads(response['SecretString'])