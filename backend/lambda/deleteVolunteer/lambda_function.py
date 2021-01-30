import requests
import psycopg2
import os

def lambda_handler(event, context):
    result = ""

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

        result = cur.fetchall()
        print(result)
        con.close()
        
    except Exception as e:
        print(e)
        result = e
        
    return str(result)
