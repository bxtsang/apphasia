import requests
import psycopg2
import os
import json 

def lambda_handler(event, context):
    result = {}
    statusCode = 500

    try :
        con = psycopg2.connect (
            host = os.environ['host'],
            database= os.environ['database'],
            user= os.environ['user'],
            port = 5432,
            password= os.environ['password']
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
