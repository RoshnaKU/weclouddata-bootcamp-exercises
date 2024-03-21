  import os
import requests
import snowflake.connector as sf

def lambda_handler(event, context):
    s3_url='https://de-materials-tpcds.s3.ca-central-1.amazonaws.com/inventory.csv'
    dest_folder='/tmp'
    file_name = 'inventory.csv'
    local_file_path = '/tmp/inventory.csv'
    
    #Snowflake connections
    user=######
    password=######
    account=######
    database='TPCDS'
    warehouse='COMPUTE_WH'
    schema='RAW'
    role='accountadmin'

    
    #Download Data from API endpoint (S3 bucket)
    response = requests.get(s3_url)
    response.raise_for_status()
    
    #saving the downloaded data in /tmp folder
    with open(local_file_path,'w') as file:
        file.write(response.content)
        
    with open(local_file_path,'r') as f:
        content=f.read()
        print('File content is: ')
        print(content)
    
    #establish snowflake connection
    conn = sf.connect(user = user, password = password, \
            account = account, warehouse=warehouse, \
            database=database, schema=schema, role=role)
    cursor=conn.cursor()
    
    # Use schema
    cursor.execute(f'USE SCHEMA {schema}')
    
    #CREATE FILE FORMAT
    
    cursor.execute("CREATE OR REPLACE FILE FORMAT CSV_COMMA TYPE='CSV' FIELD_DELIMITER=','; ")
    
    
    #CREATE STAGE
    
    cursor.execute("CREATE OR REPLACE STAGE inv_stage FILE_FORMAT=CSV_COMMA")
    
    #COPY file to stage from S3
    cursor.execute(f"PUT 'file://{local_file_path}' @inv_stage")
    
    #LIST the stage
    cursor.execute("LIST @inv_stage")
    
    #truncate table before load
    
    cursor.execute(f"TRUNCATE TABLE {schema}.inventory")
    
    #load data from stage to table
    
    cursor.execute(f"COPY INTO {schema}.inventory FROM @inv_stage/{file_name} FILE_FORMAT=CSV_COMMA ON_ERROR=CONTINUE;")
                
    print("File uploaded successfully")
    
    return {
        'statusCode': 200,
        'body': 'File downloaded and uploaded to Snowflake successfully.'
    }
