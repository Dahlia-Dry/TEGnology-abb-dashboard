import time
import boto3
import os
import pandas as pd

from botocore.config import Config as botoConfig
from decouple import config

def prepare_record(timestamp):
  record = {
    'Time': str(int(timestamp.timestamp() * 1000)),
    'MeasureValues': []
  }
  return record

def prepare_measure(measure_name, measure_value):
    measure = {
    'Name': measure_name,
    'Value': str(measure_value),
    'Type': 'DOUBLE'
    }
    return measure

def df_to_records(df,measure_cols):
    records = []
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    for i in range(len(df)):
        record = prepare_record(df['timestamp'].iloc[i])
        for col in measure_cols:
            record['MeasureValues'].append(prepare_measure(col,df[col].iloc[i]))
        records.append(record)
    print(len(records))
    return records 

def prepare_common_attributes():
    attr={
        'Dimensions': [
            {'Name': 'sensor', 'Value':'watteco_temp_2'},
        ],
        'MeasureName': 'sensor_reading',
        'MeasureValueType': 'MULTI'
    }
    return attr

def write(db_name,table_name):
    session=boto3.Session(aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
                                     region_name='eu-central-1')
    #df=pd.read_csv('watteco_temp2_backup_10-3.csv')
    df= pd.read_csv('abb_backup_10-3.csv')
    common_attributes=prepare_common_attributes()
    records = df_to_records(df,['flag','counter','temp1','temp2','current1','current2'])
    write_client = session.client('timestream-write', config=botoConfig(
    read_timeout=20, max_pool_connections=5000, retries={'max_attempts': 10}))
    for i in range(len(records)):
        try:
            result = write_client.write_records(DatabaseName=db_name,
                                                TableName=table_name,
                                                CommonAttributes=common_attributes,
                                                Records=[records[i]])
            status = result['ResponseMetadata']['HTTPStatusCode']
            print("Processed record %d. WriteRecords HTTPStatusCode: %s" %
                (i, status))
        except Exception as err:
            print("Error:", err)

class TimestreamDB(object):
    def __init__(self,db_name,db_table):
        self.db_name = db_name
        self.db_table=db_table
        self.timestream_region_name= 'eu-central-1'
        self.session = boto3.Session(aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
                                     region_name=self.timestream_region_name)
    def read(self,number):
        q = f"""SELECT * FROM "{self.db_name}"."{self.db_table}" ORDER BY time DESC LIMIT {number}"""
        #print(q)
        query_client = self.session.client('timestream-query')
        #print(query_client.query(QueryString=q))
        paginator = query_client.get_paginator('query')
        page_iterator=paginator.paginate(QueryString=q)
        rows = []
        for page in page_iterator:
            column_info = page['ColumnInfo']
            for row in page['Rows']:
                data = row['Data']
                row_output = {}
                for j in range(len(data)):
                    info = column_info[j]['Name']
                    datum = data[j]
                    row_output[info]=datum['ScalarValue']
                rows.append(row_output)
        return rows

if __name__ =="__main__":
    #tdb = TimestreamDB('tegnology_demo_sensors','abb')
    #print(tdb.read(10))
    write('tegnology_demo_sensors','abb')