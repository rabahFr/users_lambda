# CB Silver - Users ingestor

The goal of this project is to allow the deployment of AWS Lambda functions for use as a back end.

The project contains the psycopg2 library required to query Postgresql DB, as it's not native to AWS Lambda.

Every Lamba should be packaged into a single zip archive containing:
1. pyscopg2 library
2. the microservice
3. the "users.py" class