import pymysql
import pandas as pd
from decouple import config



conn =  pymysql.connect(host=config('AWS_SQL_ENDPOINT'), user=config('AWS_SQL_USER'), passwd=config('AWS_SQL_PASSWORD'), port=3306, database='sensors')
cur = conn.cursor()

def dump_df_example():
    df= pd.read_csv('temp2.csv',index_col=None)
    for i in range(len(df)):
        sql =  f"INSERT INTO watteco_temp_2 (`timestamp`,`temp1`,`temp2`) VALUES ('{df['timestamp'].iloc[i]}',{df['temp1'].iloc[i]},{df['temp2'].iloc[i]})"
        cur.execute(sql)
        conn.commit()

def save_backup_example():
    df = pd.read_sql('SELECT * FROM abb',con=conn)
    df.to_csv('abb_backup_10-3.csv')

def create_table_example():
    sql = 'CREATE TABLE abb(timestamp datetime, counter int, statusflag int, temp1 int, temp2 int, current1 int, current2 int)'
    cur.execute(sql)
    conn.commit()

def delete_table_example():
    sql = 'DROP TABLE abb'
    cur.execute(sql)
    conn.commit()

def fetch_data_example(n_points=10):
    sql ='SELECT * FROM abb ORDER BY timestamp DESC'
    cur.execute(sql)
    results = cur.fetchmany(n_points)
    print(results)

if __name__ == "__main__":
    #fetch_data_example()
    save_backup_example()
