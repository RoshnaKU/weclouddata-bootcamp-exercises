#!/usr/bin python3
"""
This is the main file for the lambda project. It will be used in EC2 IAM role situation
"""
import sqlalchemy as db
import pandas as pd
import subprocess
import toml
import os
from dotenv import load_dotenv
import boto3

def mysql_connect(host, user, password, database, port,schema):
    """
    Connect to the database
    """
    engine = db.create_engine(f'mysql+mysqlconnector://{user}:{password}@{database}.{host}:{port}/{schema}')
    return engine

if __name__=="__main__": 
    app_config = toml.load('config_file.toml')

    host=app_config['db']['host']
    port=app_config['db']['port']
    database=app_config['db']['database']
    schema=app_config['db']['schema']

    bucket=app_config['s3']['bucket']
    key=app_config['s3']['folder']

    load_dotenv()
    user=os.getenv('user')
    password=os.getenv('password')
    print(user,password)


    sql="""
    select customerID, sum(sales) sum_sales
    from orders
    group by 1
    order by 2 desc
    limit 10;
    """
    #engine = mysql_connect(host, user, password, database, port,schema)
    engine = db.create_engine(f'mysql+mysqlconnector://{user}:{password}@{database}.{host}:{port}/{schema}')
    print(engine)
    df = pd.read_sql(sql, con = engine)
    print('df created')
    #print('df issssssssssss' , df)
    df[["customerID"]].head()
    df[["customerID"]].to_json('cus_id.json')

    
    
    ACCESS_KEY=os.getenv('AWS_KEY')
    SECRET_KEY=os.getenv('AWS_SECRET')
    #s3_client = boto3.client('s3',aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    subprocess.call(['aws','s3','cp','cus_id.json', f's3://{bucket}/{key}/cus_id.json'])
    #client = s3_client.put_object(Bucket=bucket,Key=key)

    print('copied to s3')
