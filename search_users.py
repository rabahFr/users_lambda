import psycopg2
import boto3
import json
from users import User


def getCredentials():
    credential = {}
    
    secret_name = "cb_db_secrets"
    region_name = "eu-west-3"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    
    secret = json.loads(get_secret_value_response['SecretString'])
    
    credential['username'] = secret['username']
    credential['password'] = secret['password']
    credential['host'] = secret['host']
    credential['db'] = secret['dbInstanceIdentifier']
    
    return credential

def search_users(username, email):
    credential = getCredentials()
    # SQL query to retrieve data from a table based on username or email
    select_query = "SELECT * FROM users WHERE username = %s OR email = %s"
    
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(user=credential['username'], password=credential['password'], host=credential['host'], database=credential['db'])
    
        # Create a cursor object to interact with the database
        cursor = conn.cursor()
    
        # Execute the SQL query with the search key as parameters
        cursor.execute(select_query, (username, email))
    
        list_rows = []
        rows = cursor.fetchall()
        for row in rows:
            user = User(row[0], row[1], row[2], row[3])  # Assuming the order of columns in the SELECT query
            list_rows.append(user.__dict__)
    
        return list_rows
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def lambda_handler(event, context):
    print(event)
    if 'body' in event:
        username = event['body'].get('username', None)
        email = event['body'].get('email', None)

        if username or email:	
            results = search_users(username, email)
            result = {
                "statusCode": 200,
                "headers": { 
                            "Access-Control-Allow-Origin": "*"
                },
                "body": (results)
            }
            return result
        else:
            return {
                "statusCode": 400,
                "headers": { "header": "headerValue" },
                "body": "Missing search_key parameter"
            }
    else:
        return {
            "statusCode": 400,
            "headers": { "header": "headerValue" },
            "body": "No search_key parameter found"
        }