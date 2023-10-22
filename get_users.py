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

def lambda_handler(event, context):
    credential = getCredentials()
    # SQL query to retrieve data from a table
    select_query = "SELECT * FROM users"
    
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(user=credential['username'], password=credential['password'], host=credential['host'], database=credential['db'])
    
        # Create a cursor object to interact with the database
        cursor = conn.cursor()
    
        # Execute the SQL query
        cursor.execute(select_query)
    
        user_objects = []
        rows = cursor.fetchall()
        for row in rows:
            # Create a Users object for each row
            user = User(row[0], row[1], row[2], row[3])  # Assuming the order of columns in the SELECT query
            user_objects.append(user.__dict__)  # Convert User object to a json
    
        result = {
            "isBase64Encoded": 'false',
            "statusCode": 200,
            "headers": { "header": "headerValue", "Access-Control-Allow-Origin":"*" },
            "body": ((user_objects))
        }
    
        return result
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()